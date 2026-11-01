#!/usr/bin/env python3
"""Generate crawlable GitHub Pages HTML from validated, structured content."""
import argparse
import html
import json
import shutil
from pathlib import Path
from string import Template
from validate import validate_profile, validate_media
ROOT = Path(__file__).resolve().parents[1]
def e(value): return html.escape(str(value), quote=True)
def read(path): return json.loads((ROOT / path).read_text())
def records(items):
    return ''.join(f'<article class="record"><div class="date">{e(x["date"])}</div><div><h3>{e(x["title"])}</h3><p class="organization">{e(x["organization"])}</p><p>{e(x["summary"])}</p></div></article>' for x in items)
def pubs(items):
    return ''.join(f'<article class="publication" data-kind="{e(x["type"])}"><p class="eyebrow">{e(x["type"])} · {e(x["date"])}</p><h3>{e(x["title"])}</h3><p>{e(x["venue"])}</p><p class="authors">{e(x["authors"])}</p>'+ (f'<a href="{e(x["url"])}">Read publication ↗</a>' if x['url'] else '')+'</article>' for x in items)
def talks(items):
    return ''.join(f'<article class="record talk"><div class="date">{e(x["date"])}<span class="status {e(x["status"].replace('past-scheduled', 'Previously scheduled'))}">{e(x["status"].replace('past-scheduled', 'Previously scheduled'))}</span></div><div><h3>{e(x["title"])}</h3><p>{e(x["venue"])}</p></div></article>' for x in items)
def section(title,content,id):return f'<section id="{id}" class="section wrap"><div class="section-heading"><h2>{title}</h2></div>{content}</section>'
def build(output=ROOT):
    p=read('content/profile.json');m=read('content/media.json')
    validate_profile(p);validate_media(m)
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    def page(filename,title,description,body):
        template=Template((ROOT/'templates/base.html').read_text())
        rendered=template.substitute(title=e(title),description=e(description),page=filename,body=body,name=e(p['name']),email=e(p['email']),linkedin=e(p['linkedin']),scholar=e(p['scholar']),github=e(p['github']),updated=e(p['updated']))
        (output/filename).write_text(rendered)
    chips=''.join(f'<span>{e(x)}</span>' for x in p['focus'])
    impacts=''.join(f'<article><strong>{e(x["value"])}</strong><h3>{e(x["label"])}</h3><p>{e(x["detail"])}</p></article>' for x in p['impact'])
    photos=''.join(f'<figure class="story"><a href="{e(x["source_url"])}"><img src="{e(x["image"])}" alt="{e(x["alt"])}" width="800" height="811" loading="lazy"></a><figcaption><p class="eyebrow">In the room · {e(x["date"])}</p><h3>{e(x["title"])}</h3><p>{e(x["caption"])}</p><a href="{e(x["source_url"])}">View the LinkedIn post ↗</a></figcaption></figure>' for x in m)
    awards=''.join(f'<article><p class="date">{e(x["date"])}</p><h3>{e(x["title"])}</h3><p>{e(x["summary"])}</p></article>' for x in [p['awards'][0],p['awards'][1],p['awards'][3]]) if len(p['awards'])>=4 else records(p['awards'])
    home=f'''<section class="hero wrap" id="about"><div class="hero-copy"><p class="eyebrow">Scientist. Builder. Speaker.</p><p class="hero-name">{e(p['name'])}</p><h1>{e(p['headline'])}</h1><p class="lede">{e(p['intro'])}</p><div class="actions"><a class="button" href="#work">Explore my work <span>↗</span></a><a class="text-link" href="profile.html">Background & credentials →</a></div></div><div class="portrait-panel"><div class="portrait-frame"><img src="assets/images/portrait.jpg" alt="Portrait of {e(p['name'])}" width="400" height="400" fetchpriority="high"></div><div class="portrait-caption"><span class="small-square"></span><div><strong>{e(p['role'])}</strong><p>{e(p['location'])}</p></div></div><p class="portrait-note">Research depth.<br>Industry perspective.</p></div></section>
    <div class="recognition"><div class="wrap"><span>Forbes <b>30 Under 30 Europe</b></span><span>Green Talents <b>Awardee</b></span><span>PhD <b>Computer Science</b></span><span>Chartered Engineer <b>CEng (India)</b></span></div></div>
    <section class="section wrap" id="work"><div class="section-heading"><div><p class="eyebrow">01 / Applied AI</p><h2>From possibility<br>to practical value.</h2></div><p>Bringing AI into the decisions that matter: how we develop products, run factories and maintain energy infrastructure.</p></div><div class="impact-grid">{impacts}</div><div class="focus-list">{chips}</div><div class="career-preview">{records(p['experience'][:3])}</div><a class="text-link" href="profile.html#experience">Explore the full career →</a></section>
    <section class="research-section" id="research"><div class="section wrap"><div class="section-heading"><div><p class="eyebrow">02 / Research & writing</p><h2>Making AI useful.<br>Making it understandable.</h2></div><a class="text-link" href="research.html">All publications →</a></div><div class="selected-pubs">{pubs(p['publications'][:3])}</div><a class="text-link" href="{e(p['scholar'])}">Google Scholar ↗</a></div></section>
    <section class="section wrap" id="speaking"><div class="section-heading"><div><p class="eyebrow">03 / Speaking & exchange</p><h2>Ideas are better<br>when shared.</h2></div><p>Conversations across industry, universities and public forums — on trustworthy AI and the systems it can improve.</p></div>{photos}<div class="talk-preview">{talks(p['talks'][:4])}</div><a class="text-link" href="profile.html#talks">All talks & appearances →</a></section>
    <section class="recognition-section"><div class="section wrap"><p class="eyebrow">04 / Recognition</p><h2>Research with reach.</h2><div class="award-grid">{awards}</div></div></section>'''
    page('index.html',p['name']+' | Applied AI, Research & Speaking',p['intro'],home)
    filters=''.join(f'<option value="{e(k)}">{e(k.capitalize())}</option>' for k in dict.fromkeys(x['type'] for x in p['publications']))
    research=f'''<section class="page-intro wrap"><p class="eyebrow">Research & writing</p><h1>Ideas, investigations<br>& contributions.</h1><p class="lede">Explore journal articles, conference and workshop papers, books and writing across AI, energy and engineering.</p><p><a href="{e(p['scholar'])}">View Google Scholar ↗</a></p></section><section class="wrap section compact"><div class="filters"><div><label for="search">Search publications</label><input id="search" type="search" placeholder="Title, author or venue"></div><div><label for="kind">Publication type</label><select id="kind"><option value="all">All types</option>{filters}</select></div></div><p id="result-count" role="status" aria-live="polite">{len(p['publications'])} publications</p><div id="publications">{pubs(p['publications'])}</div><p id="empty-results" hidden>No publications match. Try another search or choose all types.</p></section>'''
    page('research.html','Research & writing | '+p['name'],'Publications, books and writing by '+p['name'],research)
    profile=f'<section class="page-intro wrap"><p class="eyebrow">Background & credentials</p><h1>A career connecting<br>research and industry.</h1><p class="lede">{e(p["about"])}</p><div class="actions"><button class="button" id="print-profile" type="button">Print / save as PDF</button><a class="text-link" href="research.html">Publications →</a></div><nav class="section-links" aria-label="Profile sections"><a href="#experience">Experience</a><a href="#appointments">Appointments</a><a href="#education">Education</a><a href="#talks">Talks</a><a href="#awards">Awards</a><a href="#certifications">Certifications</a></nav></section>'
    for key,title in [('experience','Experience'),('appointments','Visiting appointments'),('education','Education'),('talks','Talks & appearances'),('awards','Awards & recognition'),('certifications','Professional certifications')]:profile+=section(title,talks(p[key]) if key=='talks' else records(p[key]),key)
    for extra in p['additional']:
        profile+=section(e(extra['title']),records(extra['items']),extra['id'])
    page('profile.html','Profile | '+p['name'],'Career, education, talks and credentials of '+p['name'],profile)
    if output.resolve()!=ROOT.resolve():
        shutil.copytree(ROOT/'assets',output/'assets',dirs_exist_ok=True)
    (output/'.nojekyll').touch()
    print(f'Built 3 pages in {output}')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT);args=parser.parse_args();build(args.output)
