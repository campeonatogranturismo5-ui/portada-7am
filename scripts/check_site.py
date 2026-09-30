"""Check generated local links, article metadata and accidental key disclosure."""
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from pipeline import ROOT

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.meta={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('a','link','script'):
            self.links.append(a.get('href',a.get('src','')))
        if tag=='meta': self.meta[a.get('name',a.get('property'))]=a.get('content')

def check(root=ROOT):
    out=root/'dist'
    pages=list(out.rglob('*.html'))
    assert pages, 'No hay HTML'
    for page in pages:
        text=page.read_text(encoding='utf-8'); parser=Links();parser.feed(text)
        assert parser.meta.get('description') and parser.meta.get('og:title'),f'Metadatos ausentes: {page}'
        for url in parser.links:
            if urlsplit(url).netloc: continue
            path=unquote(urlsplit(url).path)
            if not path.startswith('/') or path.startswith('//'): continue
            target=out/path.lstrip('/')
            assert target.is_file() or (target/'index.html').is_file(),f'Enlace roto: {page} → {path}'
    for file in out.rglob('*'):
        if file.is_file():
            text=file.read_text(encoding='utf-8')
            assert not re.search(r'AIza[\w-]{30,}|gh[pousr]_[\w]{25,}',text),'Posible secreto expuesto'
    print('Verificados HTML, metadatos, enlaces internos y secretos:',len(pages),'páginas')
if __name__=='__main__': check()
