"""Dated, source-linked research metrics; kept separate from CV imports."""
import datetime as dt
import html
import json
from pathlib import Path
from validate import web_url
ROOT=Path(__file__).resolve().parents[1]
def e(v):return html.escape(str(v),quote=True)
def load_reach():
    data=json.loads((ROOT/'content/reach.json').read_text())
    asof=dt.date.fromisoformat(data['as_of'])
    known={x['id'] for x in json.loads((ROOT/'content/sources.json').read_text())}
    for name,keys in [('scholar',['citations','h_index','i10_index']),('researchgate',['reads'])]:
        item=data[name];web_url(item['url'])
        if item['source'] not in known:raise ValueError('Unknown metric source')
        for key in keys:
            if type(item[key]) is not int or item[key]<0:raise ValueError('Invalid research metric')
    years=data['scholar']['years']
    if not years or len({x['year'] for x in years})!=len(years):raise ValueError('Missing or duplicate citation years')
    for row in years:
        if type(row['year']) is not int or not 1900<=row['year']<=asof.year or type(row['citations']) is not int or row['citations']<0:raise ValueError('Invalid citation year')
    for item in data['videos'].values():
        if item['provider']=='youtube':
            import re
            if not re.fullmatch('[A-Za-z0-9_-]{11}',item['id']):raise ValueError('Invalid YouTube ID')
        elif item['provider']=='video':
            web_url(item['url'])
            if not item['url'].startswith('https://www.greentalents.de/Video/'):raise ValueError('Unapproved video origin')
        else:raise ValueError('Unknown video provider')
    for paper in data['cited_work']:
        web_url(paper['url'])
        if not paper['title'].strip() or type(paper['citations']) is not int or paper['citations']<0:raise ValueError('Invalid cited work')
    return data

def render_reach(data):
    s=data['scholar'];rg=data['researchgate'];date=dt.date.fromisoformat(data['as_of']);stamp=date.strftime('%d %B %Y').lstrip('0')
    maximum=max(1,max(x['citations'] for x in s['years']))
    bars=''.join(f'''<div class="citation-year"><span class="citation-count">{x['citations']}</span><span class="citation-track"><span class="citation-bar {'partial' if x['year']==date.year else ''}" style="height:{max(2,x['citations']/maximum*100):.2f}%"></span></span><span>{x['year']}{'*' if x['year']==date.year else ''}</span></div>''' for x in s['years'])
    papers=''.join(f'<li><a href="{e(x["url"])}">{e(x["title"])}</a><span>{x["citations"]} citations · {e(x["venue"])}</span></li>' for x in data['cited_work'])
    return f'''<div class="research-reach" id="research-impact"><div class="reach-copy"><p class="eyebrow">Research with reach</p><h3>Ideas others<br>build on.</h3><p>Explainable AI, industrial decision support and the energy transition.</p><a class="text-link" href="{e(s['url'])}">Explore Google Scholar ↗</a></div><div class="reach-data"><div class="scholar-metrics"><a href="{e(s['url'])}"><strong>{s['citations']:,}</strong><span>Google Scholar citations</span></a><a href="{e(s['url'])}"><strong>{s['h_index']}</strong><span>h-index</span></a><a href="{e(s['url'])}"><strong>{s['i10_index']}</strong><span>i10-index</span></a></div><figure class="citation-chart"><figcaption>Citations by year <span>Google Scholar</span></figcaption><div class="citation-bars">{bars}</div></figure><p class="metric-note">Snapshot: {stamp}. *{date.year} is a partial year.</p><details class="reach-method"><summary>Explore selected cited research</summary><ol class="cited-work">{papers}</ol><p>Google Scholar citation counts, observed {stamp}.</p></details><details class="reach-method"><summary>More reach & metric definitions</summary><p><a href="{e(rg['url'])}"><strong>{rg['reads']:,} ResearchGate reads</strong> ↗</a>, observed {stamp}. Reads include views of publication summaries, figures and full texts or downloads, not unique readers.</p><p>The h-index is the number of papers with at least that many citations. The i10-index counts papers with at least ten citations. Platforms have different coverage; their figures are not combined.</p></details></div></div>'''
