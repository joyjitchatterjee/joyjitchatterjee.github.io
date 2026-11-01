"""Public paper downloads preserved separately from CV imports."""
import html

def e(value):return html.escape(str(value),quote=True)
BASE='https://joyjitchatterjee.github.io/'

def render_downloads(downloads,profile):
    if not downloads:return ''
    publications={x['title']:x for x in profile['publications']}
    cards=[]
    for item in downloads:
        publication=publications[item['publication_title']]
        ident='download-'+item['id'];share_id='share-'+item['id']
        cards.append(f'''<article class="paper-download" id="{e(ident)}" aria-labelledby="{e(ident)}-title">
<a class="paper-preview" href="{e(item['file'])}"><img src="{e(item['preview'])}" width="{item['preview_width']}" height="{item['preview_height']}" alt="First page of {e(item['publication_title'])}" loading="lazy"></a>
<div class="paper-copy"><p class="eyebrow">{e(publication['venue'])} · {e(publication['date'])}</p><h3 id="{e(ident)}-title">{e(item['publication_title'])}</h3><p class="paper-authors">{e(publication['authors'])}</p><p>{e(item['summary'])}</p><p class="paper-meta">PDF · {item['pages']} pages · {item['bytes']/1_000_000:.1f} MB · {e(item['licence'])}</p><div class="actions"><a class="button" href="{e(item['file'])}">Read paper ↗</a><a class="text-link" href="{e(item['file'])}" download>Download PDF ↓</a><a class="text-link" href="{e(item['source_url'])}">Original source ↗</a></div>
<div class="paper-share"><label for="{e(share_id)}">Share this paper</label><div><input id="{e(share_id)}" type="text" readonly value="{e(BASE+item['file'])}" aria-label="Permanent PDF link for {e(item['publication_title'])}"><button type="button" data-copy-pdf="{e(share_id)}">Copy link</button></div><p id="{e(share_id)}-status" class="copy-status" role="status" aria-live="polite"></p></div></div></article>''')
    return '<section class="section wrap compact" id="downloads"><div class="section-heading"><div><p class="eyebrow">Papers to read & share</p><h2>Publication downloads.</h2></div><p>Read the full papers, save a copy or share a direct link.</p></div>'+''.join(cards)+'</section>'

def render_code_resources(repositories):
    links=''.join(f'<li><a href="{e(x["url"])}">{e(x["title"])}</a><p>{e(x["summary"])}</p></li>' for x in repositories)
    return '<div class="wrap research-resources"><details class="cv-details"><summary>Supporting code & datasets</summary><ul>'+links+'</ul></details></div>'
