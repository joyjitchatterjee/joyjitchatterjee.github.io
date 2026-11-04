"""Curated evidence, linked to the complete career records."""
import html
import json
from pathlib import Path
from detail_views import record_anchor, render_details
from validate import profile_record, web_url

ROOT = Path(__file__).resolve().parents[1]
def e(value): return html.escape(str(value), quote=True)

def load_spotlight(profile):
    data = json.loads((ROOT/'content/spotlight.json').read_text())
    sources = {x['id'] for x in json.loads((ROOT/'content/sources.json').read_text())}
    for quote in data['quotes']:
        if quote['source'] not in sources or not 0 < len(quote['text'].split()) <= 25:
            raise ValueError('Invalid quote provenance or length')
        web_url(quote['url'])
    for group in ['awards', 'forums', 'community']:
        for ref in data[group]: profile_record(profile, ref)
    media_ids = {x['id'] for x in json.loads((ROOT/'content/media.json').read_text())}
    for ref in data['awards'] + data['community'] + data.get('recognition_photos', []):
        if 'media_id' in ref and ref['media_id'] not in media_ids:
            raise ValueError('Unknown spotlight media')
    return data

def render_quotes(data):
    cards = ''.join(f'<figure class="evidence-quote"><figcaption><strong>{e(q["name"])}</strong><span>{e(q["context"])}</span></figcaption><blockquote>“{e(q["text"])}”</blockquote><a class="text-link" href="{e(q["url"])}">Read in context ↗</a></figure>' for q in data['quotes'])
    return '<aside class="evidence-quotes" aria-label="Recognition in their words">'+cards+'</aside>'

def record_link(ref):
    return 'profile.html#'+record_anchor(ref['section'].removeprefix('additional.'), ref['title'])

def image_link(item, label='Enlarge image ↗'):
    return f'<a class="evidence-image" href="{e(item["image"])}" data-viewer="image" data-title="{e(item["title"])}" data-caption="{e(item["caption"])}"><img src="{e(item["image"])}" width="{item["width"]}" height="{item["height"]}" alt="{e(item["alt"])}" loading="lazy"><span class="enlarge">{e(label)}</span></a>'

def render_awards(data, profile, certificate, media):
    cards = ''
    for ref in data['awards']:
        r = profile_record(profile, ref)
        visual = image_link(media[ref['media_id']], 'View award ↗') if ref.get('media_id') else ''
        cards += f'<li>{visual}<div class="award-copy"><span class="date">{e(r["date"])}</span><h4><a href="{record_link(ref)}">{e(r["title"])}</a></h4><p>{e(r["summary"])}</p><a class="text-link" href="{record_link(ref)}">Recognition details →</a></div></li>'
    c = certificate
    feature = f'''<article class="certificate-feature"><a href="{e(c['image'])}" data-viewer="image" data-title="{e(c['title'])}" data-caption="{e(c['caption'])}"><img src="{e(c['image'])}" width="{c['width']}" height="{c['height']}" alt="{e(c['alt'])}" loading="lazy"><span class="enlarge">View certificate ↗</span></a><div><p class="eyebrow">Reckitt × University of Hull</p><h3>Outstanding.<br>The highest KTP grade.</h3><p>The Knowledge Transfer Partnership received Innovate UK’s Certificate of Excellence with the highest grade, Outstanding. My work connected AI research with practical R&D and manufacturing challenges at Reckitt.</p><p class="metric-note">Project completed in 2023. Certificate shared in February 2024.</p><a class="text-link" href="{e(c['source_url'])}">View the recognition ↗</a></div></article>'''
    moments = ''
    for ref in data.get('recognition_photos', []):
        m = media[ref['media_id']]
        moments += f'<figure class="recognition-moment moment-{e(m["id"])}">{image_link(m)}<figcaption><p class="eyebrow">{e(m["date"])}</p><h3>{e(m["title"])}</h3><p>{e(m["caption"])}</p></figcaption></figure>'
    return '<div class="recognition-moments">'+moments+'</div>'+feature+'<details class="award-archive"><summary>Explore the full recognition record: awards, citations & academic distinctions</summary><div class="award-timeline"><h3>A wider record of recognition.</h3><ol>'+cards+'</ol><a class="text-link" href="profile.html#awards">All awards & recognition →</a></div></details>'

def render_forums(data, profile, media):
    cards = ''
    for ref in data['forums']:
        r = profile_record(profile, ref)
        cards += f'<article class="forum-card"><p class="eyebrow">{e(r["date"])}</p><h3>{e(r["title"])}</h3><p>{e(r["venue"])}</p>{render_details(r,"Event context & participants")}<a class="text-link" href="{record_link(ref)}">Full event record →</a></article>'
    community = ''
    for ref in data['community']:
        r = profile_record(profile, ref)
        visual = image_link(media[ref['media_id']], 'View programme ↗') if ref.get('media_id') else ''
        community += f'<article class="community-feature">{visual}<div class="community-copy"><p class="eyebrow">Research community leadership</p><h3>Co-organiser, AI4Renewables social at ICLR 2022</h3><p>{e(r["summary"])}</p><div class="actions"><a class="text-link" href="https://iclr.cc/media/iclr-2022/Slides/8733.pdf">Official conference programme ↗</a><a class="text-link" href="{record_link(ref)}">Community contributions →</a></div></div></article>'
    return community+'<div class="forum-grid">'+cards+'</div>'

def render_library(downloads, profile):
    publications = {x['title']:x for x in profile['publications']}
    cards = ''
    for item in downloads:
        p = publications[item['publication_title']]
        cards += f'<a class="library-paper" href="research.html#download-{e(item["id"])}"><img src="{e(item["preview"])}" width="{item["preview_width"]}" height="{item["preview_height"]}" loading="lazy" alt="First page of {e(item["publication_title"])}"><span class="eyebrow">{e(p["type"])} · {e(p["date"])}</span><h3>{e(item["publication_title"])}</h3><span class="text-link">Read, download & share ↗</span></a>'
    return '<div class="paper-library"><h3>Open papers. Ready to share.</h3><div class="library-grid">'+cards+'</div></div>'
