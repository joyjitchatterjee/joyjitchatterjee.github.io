"""Shared, accessible detail views for homepage summaries and the full profile."""
import html
import re
import unicodedata

def e(value):return html.escape(str(value),quote=True)

def record_anchor(section,title):
    text=unicodedata.normalize('NFKD',title).encode('ascii','ignore').decode().lower()
    return section.replace('.','-')+'-'+re.sub(r'[^a-z0-9]+','-',text).strip('-')

def render_details(item,label='Read full details'):
    groups=item.get('details',[])
    if not groups:return ''
    content=''.join(f'<section class="detail-group"><h4>{e(group["heading"])}</h4><ul>'+''.join(f'<li>{e(point)}</li>' for point in group['points'])+'</ul></section>' for group in groups)
    return f'<details class="cv-details" data-cv-details><summary>{e(label)}<span class="detail-count">{len(groups)} {"topic" if len(groups)==1 else "topics"}</span></summary><div class="detail-content">{content}</div></details>'
