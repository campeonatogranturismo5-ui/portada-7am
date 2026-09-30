import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build import build
from check_site import check
from pipeline import ROOT, read, write

class BuildTests(unittest.TestCase):
    def test_legacy_links_and_escaping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            shutil.copytree(ROOT/'web',root/'web')
            write(root/'data/config.json',read(ROOT/'data/config.json'))
            legacy=read(ROOT/'data/legacy-news.json')
            section=next(iter(legacy['sections']))
            legacy['sections'][section]['pool'][0]['title']='<script>alert(1)</script>'
            write(root/'data/legacy-news.json',legacy)
            build(root);check(root)
            aliases=read(root/'dist/legacy-aliases.json')
            oldid=legacy['sections'][section]['pool'][0]['id']
            page=root/'dist/noticias'/aliases[oldid]/'index.html'
            self.assertTrue(page.exists())
            body=page.read_text(encoding='utf-8')
            self.assertIn('&lt;script&gt;',body)
            self.assertNotIn('<script>alert(1)</script>',body)
            build(root)
            self.assertEqual(aliases,read(root/'dist/legacy-aliases.json'))

if __name__=='__main__':unittest.main()
