"""Anonymised stakeholder feedback and source-linked executive engagement."""
import html
import json
from pathlib import Path
from validate import profile_record
from detail_views import record_anchor

ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    'VP, IT&D Digital - Supply Chain, Reckitt',
    'VP, Business Development, EPAM',
    'Director, Project Management, EPAM',
    'IT&D Product Manager at Global CPG company',
    'Former senior colleague, EPAM',
    'Professor, Loughborough University',
}
def e(value): return html.escape(str(value), quote=True)

def validate_leadership(data, profile):
    sources = {x['id'] for x in json.loads((ROOT/'content/sources.json').read_text())}
    for item in data['feedback']:
        if set(item) != {'role', 'theme', 'summary', 'source'} or item['role'] not in ROLES:
            raise ValueError('Feedback must use approved anonymous role attribution')
        if not item['summary'].strip() or item['source'] not in sources:
            raise ValueError('Feedback needs a summary and known evidence source')
    for item in data['engagements']:
        profile_record(profile, item['record'])
        if item['source'] not in sources: raise ValueError('Unknown engagement source')
    return data

def load_leadership(profile):
    return validate_leadership(json.loads((ROOT/'content/leadership.json').read_text()), profile)

def render_engagements(data):
    cards = ''
    for item in data['engagements']:
        ref = item['record']
        url = 'profile.html#'+record_anchor(ref['section'].removeprefix('additional.'), ref['title'])
        cards += f'<article><p class="eyebrow">{e(item["role"])}</p><h3>{e(item["title"])}</h3><p>{e(item["text"])}</p><a class="text-link" href="{e(url)}">Explore the context →</a></article>'
    return f'<section class="executive-section wrap" id="executive-engagement"><div class="section-heading"><div><p class="eyebrow">Executive engagement & industry dialogue</p><h2>AI in the conversations<br>that shape business.</h2></div><a class="text-link" href="#speaking">International panels & talks ↓</a></div><div class="executive-grid">{cards}</div></section>'

def render_feedback(data, photo):
    cards = []
    for item in data['feedback']:
        cards.append(f'<article class="feedback-card"><p class="eyebrow">{e(item["theme"])}</p><p class="feedback-summary">{e(item["summary"])}</p><p class="feedback-role">{e(item["role"])}</p></article>')
    featured = ''.join(cards[:3])
    more = '<details class="section-more"><summary>Further perspectives on leadership & mentoring</summary><div class="feedback-grid">'+''.join(cards[3:])+'</div></details>'
    visual = f'<figure class="feedback-photo"><a href="{e(photo["image"])}" data-viewer="image" data-title="{e(photo["title"])}" data-caption="{e(photo["caption"])}"><img src="{e(photo["image"])}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy" alt="{e(photo["alt"])}"><span class="enlarge">View speaking photograph ↗</span></a><figcaption><span>Invited speaker · 2025</span><strong>Queen Mary University of London</strong><p>Generative AI, knowledge graphs and industrial decision support.</p></figcaption></figure>'
    return f'<section class="feedback-section" id="feedback"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">Stakeholder perspectives</p><h2>Trusted to deliver.</h2></div><p>Anonymised summaries of individual feedback from senior stakeholders and collaborators.</p></div><div class="feedback-editorial">{visual}<div><div class="feedback-grid">{featured}</div>{more}</div></div></div></section>'
