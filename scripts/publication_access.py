"""Preserve independently audited full-text links across CV updates."""
import json
from pathlib import Path
from validate import profile_record, web_url

ROOT = Path(__file__).resolve().parents[1]
def load_access(profile):
    records = json.loads((ROOT/'content/publication-access.json').read_text())
    sources = {x['id'] for x in json.loads((ROOT/'content/sources.json').read_text())}
    seen = set()
    for item in records:
        title = item['publication_title']
        profile_record(profile, {'section':'publications', 'title':title})
        web_url(item['url'])
        if title in seen or item['source'] not in sources or item['label'] != 'Open full text':
            raise ValueError('Invalid publication access record')
        seen.add(title)
    return records
