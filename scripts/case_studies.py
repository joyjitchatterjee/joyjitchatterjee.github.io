"""Visual enterprise case studies with executive summaries and optional depth."""
import html
from detail_views import record_anchor, render_details
from validate import profile_record
from spotlight import image_link

def e(value): return html.escape(str(value), quote=True)

def render_cases(cases, profile, media, downloads=()):
    papers = {x['id']: x for x in downloads}
    cards = ''
    for i, case in enumerate(cases):
        ref = case['record']
        record = profile_record(profile, ref)
        # Data-scale evidence belongs in the full career record, not the homepage.
        home_record = {**record, 'details': [g for g in record.get('details', []) if g['heading'] != 'Data scale and decision-support workflow']}
        url = 'profile.html#'+record_anchor(ref['section'].removeprefix('additional.'), ref['title'])
        v = case['visual']
        steps = ''.join(f'<li>{e(step)}</li>' for step in v['steps'])
        visual = f'<div class="story-metric"><strong>{e(v["value"])}</strong><span>{e(v["label"])}</span></div>'
        highlights = ''.join(f'<div class="story-highlight"><h4>{e(x["label"])}</h4><p>{e(x["text"])}</p></div>' for x in case['highlights'])
        photo = ''
        if case.get('media_id'):
            m = media[case['media_id']]
            photo = '<figure class="story-evidence">'+image_link(m, 'View presentation photograph ↗')+'<figcaption>'+e(m['caption'])+'</figcaption></figure>'
        paper = ''
        paper_detail = ''
        if case.get('download_id'):
            item = papers[case['download_id']]
            paper = f'<a class="story-paper-link" href="{e(item["file"])}"><img src="{e(item["preview"])}" width="{item["preview_width"]}" height="{item["preview_height"]}" loading="lazy" alt="Manufacturing AI paper preview"><span>Related paper · HAL preprint<strong>Trustworthy AI in factories · Read PDF ↗</strong></span></a>'
            paper_detail = f'<div class="story-highlight"><h4>{e(item["publication_title"])}</h4><p>{e(item["summary"])}</p><div class="story-paper-links"><a href="{e(item["file"])}" download>Download PDF</a><a href="research.html#download-{e(item["id"])}">Authors & publication details →</a></div></div>'
        detail = f'<details class="story-depth"><summary>Contribution & evidence <span aria-hidden="true">↗</span></summary><div class="story-depth-body"><p class="story-contribution">{e(case["contribution"])}</p><ul class="approach-map">{steps}</ul>{highlights}{paper_detail}{render_details(home_record,"Full responsibilities & project detail")}{photo}<a class="text-link" href="{e(url)}">Full career record →</a><a class="text-link" href="{e(case["url"])}">{e(case["label"])} ↗</a></div></details>'
        cards += f'<article class="enterprise-story story-{e(case["id"])}" id="{e(case["id"])}"><div class="story-copy"><p class="eyebrow">{e(case["kicker"])}</p>{visual}<h3>{e(case["title"])}</h3><p class="story-summary">{e(case["summary"])}</p><p class="story-outcome">{e(case["outcome"])}</p>{paper}</div>{detail}</article>'
    return '<div class="enterprise-stories">'+cards+'</div>'
