"""Independent uses and discussions of research, preserved outside CV imports."""
import datetime as dt
import html
import json
import re
from pathlib import Path
from validate import web_url

ROOT = Path(__file__).resolve().parents[1]


def load_impact(profile):
    data = json.loads((ROOT / 'content/research-impact.json').read_text())
    dt.date.fromisoformat(data['verified_on'])
    sources = {x['id']: x for x in json.loads((ROOT / 'content/sources.json').read_text())}
    publications = {x['title'] for x in profile['publications']}
    ids = set()
    for item in data['entries']:
        for field in ('id', 'organization', 'context', 'category', 'title', 'summary',
                      'source_title', 'url', 'evidence', 'publication_title', 'source'):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError('Missing research impact field: ' + field)
        if not re.fullmatch('[a-z][a-z0-9-]*', item['id']) or item['id'] in ids:
            raise ValueError('Invalid or duplicate research impact ID')
        ids.add(item['id'])
        web_url(item['url'])
        if item['source'] not in sources or sources[item['source']].get('url') != item['url']:
            raise ValueError('Research impact source does not match registry')
        if item['publication_title'] not in publications:
            raise ValueError('Unknown research impact publication')
    return data


def render_impact(data, profile):
    e = lambda value: html.escape(str(value), quote=True)
    pubs = {x['title']: x for x in profile['publications']}
    cards = []
    for item in data['entries']:
        work = pubs[item['publication_title']]
        cards.append(f'''<article class="research-impact-card" id="impact-{e(item['id'])}">
<p class="eyebrow">{e(item['category'])}</p><p class="impact-institution">{e(item['organization'])}</p>
<p class="impact-location">{e(item['context'])}</p><h3>{e(item['title'])}</h3><p>{e(item['summary'])}</p>
<a class="text-link" href="{e(item['url'])}">Read independent source ↗</a>
<details class="impact-evidence"><summary>Context & cited work</summary><p>{e(item['evidence'])}</p>
<p><strong>Source:</strong> {e(item['source_title'])}</p>
<p><strong>My co-authored work:</strong> <a href="{e(work['url'])}">{e(work['title'])}</a></p></details></article>''')
    return f'''<section class="research-impact-stories" id="research-in-practice" aria-labelledby="impact-heading">
<div class="research-impact-grid"><div class="impact-introduction"><p class="eyebrow">Beyond citation counts</p>
<h2 id="impact-heading">Where my research<br>has made an impact.</h2>
<p>From doctoral guidance in Norway to student learning at UCL and inclusive design in Singapore, my co-authored research is finding its way into new settings and conversations.</p>
<p>These independent references show where the work is being quoted, applied in research methods and discussed across education, industry and responsible AI.</p></div>{''.join(cards)}</div>
<p class="impact-closing">For me, research impact is also about who engages with an idea, where it travels and the conversations it helps move forward.</p></section>'''
