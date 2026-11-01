#!/usr/bin/env python3
"""Check generated HTML for broken local paths, anchors and inaccessible images."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import sys
class Document(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.titles=0;self.h1=0;self.feed(text)
    def handle_data(self,data):
        if '\u2014' in data:raise ValueError('Website text must not contain em dashes')
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='title':self.titles+=1
        if tag=='h1':self.h1+=1
        if tag=='img' and not a.get('alt'):raise ValueError('Image missing alt text')
        for field in ['href','src']:
            if a.get(field):self.links.append(a[field])
        if any(k.startswith('on') for k in a):raise ValueError('Unexpected inline event handler')
def check_site(root):
    root=Path(root)
    pages={name:Document((root/name).read_text()) for name in ['index.html','research.html','profile.html']}
    for name,doc in pages.items():
        if doc.h1!=1 or doc.titles!=1:raise ValueError(name+': needs exactly one h1 and title')
        if len(doc.ids)!=len(set(doc.ids)):raise ValueError(name+': duplicate IDs')
        for link in doc.links:
            u=urlsplit(link)
            if u.scheme:
                if u.scheme not in ['https','mailto']:raise ValueError('Unsafe link scheme: '+link)
                continue
            if u.netloc:raise ValueError('Protocol-relative URL: '+link)
            target=unquote(u.path) or name
            resolved=(root/target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():raise ValueError(name+': broken local path '+link)
            if u.fragment and target in pages and u.fragment not in pages[target].ids:raise ValueError(name+': missing anchor '+link)
    print('3 pages checked: local paths, anchors, headings, image alternatives and URL schemes')
if __name__=='__main__':check_site(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
