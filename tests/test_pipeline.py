import argparse
import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime,timezone,timedelta
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import pipeline as p

class PipelineTests(unittest.TestCase):
    def test_evidence_requires_original_source_words(self):
        item = {'sourceTitle': 'NASA plans lunar crops', 'excerpt': 'Partners study  growing crops.'}
        self.assertTrue(p.valid_evidence(['NASA plans lunar crops', 'Partners study growing crops.'], item))
        self.assertFalse(p.valid_evidence(['La NASA planea cultivos lunares'], item))
        self.assertFalse(p.valid_evidence(['NASA confirms lunar crops'], item))
        self.assertFalse(p.valid_evidence([], item))

    def test_canonical_identity(self):
        self.assertEqual(p.canonical('https://example.com/a?utm_source=x&id=7#top'),'https://example.com/a?id=7')
        with self.assertRaises(ValueError): p.canonical('javascript:alert(1)')

    def test_dates_reject_old_future_and_missing_zone(self):
        now=datetime.now(timezone.utc)
        for value in [(now-timedelta(days=3)).isoformat(),(now+timedelta(days=1)).isoformat(),'2026-09-30T07:00:00']:
            self.assertFalse(p.recent(value,now,48))

    def test_entity_attack_rejected(self):
        with self.assertRaises(ValueError): list(p.parse_feed(b'<!DOCTYPE rss><rss/>',{},datetime.now(timezone.utc)))

    def test_dst(self):
        self.assertEqual(datetime(2026,7,1,5,tzinfo=timezone.utc).astimezone(p.TZ).hour,7)
        self.assertEqual(datetime(2026,12,1,6,tzinfo=timezone.utc).astimezone(p.TZ).hour,7)

    def test_event_dedup_before_model(self):
        self.assertTrue(p.duplicate({'url':'https://a.com','sourceTitle':'NASA prepara cultivos lunares con Canadá y Alemania'}, {'url':'https://b.com','sourceTitle':'Canadá y Alemania: NASA prepara cultivos lunares'}))

    def fixture(self,root):
        now=datetime.now(timezone.utc)
        config={'sources':[{'name':'Fuente','url':'https://example.com/rss','section':'ciencia','lang':'en'}],'maxAgeHours':48,'model':'gemini-3.1-flash-lite'}
        p.write(root/'data/config.json',config)
        excerpt='NASA and its international partners plan a ground demonstrator to study growing crops on the Moon.'
        feed=f'<rss><channel><item><title>NASA plans lunar crop demonstrator</title><link>https://example.com/news</link><pubDate>{now.isoformat()}</pubDate><description>{excerpt}</description></item></channel></rss>'.encode()
        def fetcher(url,**kw): return (feed if 'rss' in url else b'public article',url)
        class Model:
            calls=0
            def __init__(self,*a): pass
            def call(self,instruction,data):
                Model.calls+=1
                if instruction==p.AUDIT: return {'faithful':True,'spanish':True,'duplicateId':None}
                return {'title':'La NASA prepara cultivos lunares','summary':'La NASA prevé estudiar cultivos para la Luna.','paragraphs':['La agencia y sus socios planean un demostrador en la Tierra.'],'bullets':['El proyecto está previsto.'],'eventKey':'nasa-cultivos-luna','evidence':['NASA and its international partners']}
        return fetcher,Model

    def test_second_run_uses_cache_and_failure_preserves_edition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fetcher,model=self.fixture(root)
            args=argparse.Namespace(scheduled=False,limit=1,collect_only=False)
            with patch.object(p.time,'sleep'):
                p.run(args,root,model,fetcher)
                before=(root/'data/current.json').read_bytes()
                p.run(args,root,model,fetcher)
                self.assertEqual(model.calls,2)
                # Force a new fingerprint and fail the model. Current edition must not change.
                current=(root/'data/current.json').read_bytes()
                def changed(url,**kw):
                    raw,final=fetcher(url,**kw)
                    return raw.replace(b'NASA plans',b'NASA now plans'),final
                class Failed:
                    def __init__(self,*a): pass
                    def call(self,*a): raise p.QuotaError('quota')
                with self.assertRaises(p.QuotaError): p.run(args,root,Failed,changed)
                self.assertEqual(current,(root/'data/current.json').read_bytes())

if __name__=='__main__': unittest.main()
