"""Visual enterprise case studies with executive summaries and optional depth."""
import html
from detail_views import record_anchor, render_details
from validate import profile_record
from spotlight import image_link

def e(value): return html.escape(str(value), quote=True)

def render_cases(cases, profile, media):
    cards = ''
    jump = ''
    for i, case in enumerate(cases):
        ref = case['record']
        record = profile_record(profile, ref)
        # Data-scale evidence belongs in the full career record, not the homepage.
        home_record = {**record, 'details': [g for g in record.get('details', []) if g['heading'] != 'Data scale and decision-support workflow']}
        url = 'profile.html#'+record_anchor(ref['section'].removeprefix('additional.'), ref['title'])
        v = case['visual']
        steps = ''.join(f'<li><span class="approach-dot">{n+1:02}</span><span>{e(step)}</span></li>' for n, step in enumerate(v['steps']))
        visual = f'<div class="story-visual"><p class="eyebrow">Product & delivery approach</p><ol class="approach-map">{steps}</ol><div class="story-metric"><strong>{e(v["value"])}</strong><span>{e(v["label"])}</span></div></div>'
        highlights = ''.join(f'<div class="story-highlight"><h4>{e(x["label"])}</h4><p>{e(x["text"])}</p></div>' for x in case['highlights'])
        photo = ''
        if case.get('media_id'):
            m = media[case['media_id']]
            photo = '<figure class="story-evidence">'+image_link(m, 'View presentation photograph ↗')+'<figcaption>'+e(m['caption'])+'</figcaption></figure>'
        detail = f'<details class="story-depth"><summary>Explore contribution, context & evidence <span aria-hidden="true">↗</span></summary><div class="story-depth-body">{highlights}{render_details(home_record,"Full responsibilities & project detail")}{photo}<a class="text-link" href="{e(case["url"])}">{e(case["label"])} ↗</a></div></details>'
        basis = '<p class="story-basis">Financial business cases reflect opportunities assessed in evaluation.</p>' if case['id'] != 'enterprise-ai' else ''
        cards += f'<article class="enterprise-story story-{e(case["id"])}" id="{e(case["id"])}"><div class="story-copy"><p class="eyebrow"><span class="story-index">0{i+1}</span> {e(case["kicker"])}</p><h3>{e(case["title"])}</h3><p class="story-summary">{e(case["summary"])}</p><p class="story-contribution">{e(case["contribution"])}</p><p class="story-outcome">{e(case["outcome"])}</p>{basis}<a class="text-link" href="{e(url)}">Full career record →</a></div>{visual}{detail}</article>'
        label = {'enterprise-ai':'Strategy & delivery','procurement-ai':'Negotiation intelligence','rd-product':'R&D innovation','manufacturing':'Manufacturing'}[case['id']]
        jump += f'<a href="#{e(case["id"])}"><span>0{i+1}</span>{label} ↗</a>'
    return '<nav class="case-navigation" aria-label="Explore enterprise work">'+jump+'</nav><div class="enterprise-stories">'+cards+'</div>'
