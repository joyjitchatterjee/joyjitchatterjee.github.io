#!/usr/bin/env python3
"""Generate crawlable GitHub Pages HTML from validated, structured content."""
import argparse
import html
import hashlib
import json
import shutil
from pathlib import Path
from string import Template
from validate import validate_profile, validate_media, validate_showcase, validate_downloads
from showcase import render as render_home
from research_reach import load_reach, render_reach
from detail_views import record_anchor, render_details
from publication_downloads import render_downloads, render_code_resources
ROOT = Path(__file__).resolve().parents[1]
def e(value): return html.escape(str(value), quote=True)
def read(path): return json.loads((ROOT / path).read_text())
def record_source(item):
    source=next((x for x in read('content/sources.json') if x['id']==item['source']),{})
    return f'<a class="record-source" href="{e(source["url"])}">View source ↗</a>' if source.get('kind')=='public web' and source.get('url') else ''
def records(items,section_id):
    return ''.join(f'<article class="record" id="{record_anchor(section_id,x["title"])}"><div class="date">{e(x["date"])}</div><div><h3>{e(x["title"])}</h3><p class="organization">{e(x["organization"])}</p><p>{e(x["summary"])}</p>{render_details(x,"Read responsibilities, projects & technologies" if section_id=="experience" else "Read full details")}{record_source(x)}</div></article>' for x in items)
def publication_label(item):
    if item['source']=='glow-programme':return 'View workshop programme'
    return {'video':'Watch video','book':'View book'}.get(item['type'],'Read publication')
def pubs(items,downloads=()):
    files={x['publication_title']:x['file'] for x in downloads}
    rendered=[]
    for item in items:
        links=''
        if item['title'] in files:links+=f'<a class="publication-pdf" href="{e(files[item["title"]])}">Read PDF ↗</a> '
        if item['url']:links+=f'<a href="{e(item["url"])}">{publication_label(item)} ↗</a>'
        rendered.append(f'<article class="publication" data-kind="{e(item["type"])}"><p class="eyebrow">{e(item["type"])} · {e(item["date"])}</p><h3>{e(item["title"])}</h3><p>{e(item["venue"])}</p><p class="authors">{e(item["authors"])}</p><div class="publication-links">{links}</div>{render_details(item)}</article>')
    return ''.join(rendered)
def talks(items):
    rendered=[]
    for x in items:
        label='Previously scheduled' if x['status']=='past-scheduled' else x['status']
        rendered.append(f'<article class="record talk" id="{record_anchor("talks",x["title"])}"><div class="date">{e(x["date"])}<span class="status {e(x["status"])}">{e(label)}</span></div><div><h3>{e(x["title"])}</h3><p>{e(x["venue"])}</p>{render_details(x)}{record_source(x)}</div></article>')
    return ''.join(rendered)

def section(title,content,id):return f'<section id="{id}" class="section wrap"><div class="section-heading"><h2>{title}</h2></div>{content}</section>'
def build(output=ROOT):
    p=read('content/profile.json');m=read('content/media.json')
    validate_profile(p);validate_media(m)
    downloads=read('content/downloads.json');validate_downloads(downloads,p)
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    def page(filename,title,description,body):
        template=Template((ROOT/'templates/base.html').read_text())
        versions={key:hashlib.sha256((ROOT/path).read_bytes()).hexdigest()[:12] for key,path in [('style_version','assets/site.css'),('script_version','assets/site.js'),('experience_version','assets/experience.js')]}
        rendered=template.substitute(**versions,title=e(title),description=e(description),page=filename,body=body,name=e(p['name']),email=e(p['email']),linkedin=e(p['linkedin']),scholar=e(p['scholar']),github=e(p['github']),bluesky=e(p['bluesky']),updated=e(p['updated']))
        (output/filename).write_text(rendered)
    showcase=read('content/showcase.json')
    validate_showcase(showcase,p)
    home=render_home(p,m,showcase,lambda items:pubs(items,downloads))
    page('index.html',p['name']+' | AI Leadership, Products & Innovation',p['intro'],home)
    filters=''.join(f'<option value="{e(k)}">{e(k.capitalize())}</option>' for k in dict.fromkeys(x['type'] for x in p['publications']))
    research=f'''<section class="page-intro wrap"><p class="eyebrow">Research & writing</p><h1>Ideas, investigations<br>& contributions.</h1><p class="lede">Explore journal articles, conference and workshop papers, books and writing across AI, energy and engineering.</p><div class="actions"><a class="button" href="#downloads">Read & share papers ↓</a><a class="text-link" href="{e(p['scholar'])}">Google Scholar ↗</a></div></section><section class="wrap research-metrics-page">{render_reach(load_reach())}</section>{render_downloads(downloads,p)}<section class="wrap section compact"><div class="filters"><div><label for="search">Search publications</label><input id="search" type="search" placeholder="Title, author or venue"></div><div><label for="kind">Publication type</label><select id="kind"><option value="all">All types</option>{filters}</select></div></div><p id="result-count" role="status" aria-live="polite">{len(p['publications'])} publications</p><div id="publications">{pubs(p['publications'],downloads)}</div><p id="empty-results" hidden>No publications match. Try another search or choose all types.</p></section>'''
    research+=render_code_resources(showcase['repositories'])
    page('research.html','Research & writing | '+p['name'],'Publications, books and writing by '+p['name'],research)
    profile=f'<section class="page-intro wrap"><p class="eyebrow">Background & credentials</p><h1>A career connecting<br>research and industry.</h1><p class="lede">{e(p["about"])}</p><div class="actions"><button class="button secondary" id="expand-details" type="button" aria-pressed="false">Expand all details</button><button class="button" id="print-profile" type="button">Print / save as PDF</button><a class="text-link" href="research.html">Publications →</a></div><p class="profile-guide">Explore the summaries below, open any entry for its full detail, or expand all entries. Printing includes the detailed content.</p><nav class="section-links" aria-label="Profile sections"><a href="#experience">Experience</a><a href="#appointments">Appointments</a><a href="#education">Education</a><a href="#reviews">Academic service</a><a href="#talks">Talks</a><a href="#awards">Awards</a><a href="#certifications">Certifications</a><a href="#cpd">Professional development</a><a href="#press">Media</a><a href="#extramural">Mentoring</a><a href="#skills">Technical skills</a><a href="#patents">Patent applications</a><a href="#scholarships">Funding</a><a href="#memberships">Memberships</a></nav></section>'
    profile += '<div class="wrap online-profiles">' + ''.join(f'<a href="{e(x["url"])}">{e(x["title"])} ↗</a>' for x in showcase['profiles']) + '</div>'
    for key,title in [('experience','Experience'),('appointments','Visiting appointments'),('education','Education'),('talks','Talks & appearances'),('awards','Awards & recognition'),('certifications','Professional certifications')]:profile+=section(title,talks(p[key]) if key=='talks' else records(p[key],key),key)
    for extra in p['additional']:
        profile+=section(e(extra['title']),records(extra['items'],extra['id']),extra['id'])
    page('profile.html','Profile | '+p['name'],'Career, education, talks and credentials of '+p['name'],profile)
    if output.resolve()!=ROOT.resolve():
        shutil.copytree(ROOT/'assets',output/'assets',dirs_exist_ok=True)
    (output/'.nojekyll').touch()
    print(f'Built 3 pages in {output}')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT);args=parser.parse_args();build(args.output)
