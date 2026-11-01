#!/usr/bin/env python3
"""Small dependency-free validator for the repository's JSON schema subset."""
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
def check(value,schema,path='$'):
    types={'object':dict,'array':list,'string':str}
    if not isinstance(value,types[schema['type']]):raise ValueError(f'{path}: expected {schema["type"]}')
    if isinstance(value,dict):
        expected=set(schema['required'])
        if set(value)!=expected:raise ValueError(f'{path}: wrong keys: {set(value)^expected}')
        for k,v in value.items():check(v,schema['properties'][k],path+'.'+k)
    elif isinstance(value,list):
        if len(value)>schema.get('maxItems',1000):raise ValueError(f'{path}: too many items')
        for i,v in enumerate(value):check(v,schema['items'],f'{path}[{i}]')
    else:
        if len(value)>schema.get('maxLength',20000):raise ValueError(f'{path}: too long')
        if 'enum' in schema and value not in schema['enum']:raise ValueError(f'{path}: unsupported value {value}')
def web_url(url):
    u=urlsplit(url)
    if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError(f'Expected public HTTPS URL: {url}')
def validate_profile(profile,extra_sources=()):
    check(profile,json.loads((ROOT/'content/profile.schema.json').read_text()))
    dt.date.fromisoformat(profile['updated'])
    for k in ['name','role','headline','intro','about']:
        if not profile[k].strip():raise ValueError(f'{k} cannot be empty')
    if not re.fullmatch(r'[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+',profile['email']):raise ValueError('Invalid email')
    for k in ['linkedin','scholar','github']:web_url(profile[k])
    known={s['id'] for s in json.loads((ROOT/'content/sources.json').read_text())}|set(extra_sources)
    def walk(x):
        if isinstance(x,dict):
            if 'source' in x and x['source'] not in known:raise ValueError('Unknown source: '+x['source'])
            if 'title' in x and not x['title'].strip():raise ValueError('Empty title')
            if x.get('url'):web_url(x['url'])
            for v in x.values():walk(v)
        if isinstance(x,list):
            for v in x:walk(v)
    walk(profile)
    for key in ['experience','education','publications','talks','awards','certifications']:
        titles=[x['title'].casefold().strip() for x in profile[key]]
        if len(titles)!=len(set(titles)):raise ValueError('Duplicate titles in '+key)
    for x in profile['additional']:
        if not re.fullmatch(r'[a-z][a-z0-9-]*',x['id']):raise ValueError('Invalid section ID')
    ids=[x['id'] for x in profile['additional']]
    if len(set(ids))!=len(ids) or set(ids)&{'experience','education','appointments','talks','awards','certifications','contact','main'}:raise ValueError('Duplicate section IDs')
    months={m:i for i,m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],1)}
    asof=dt.date.fromisoformat(profile['updated'])
    for talk in profile['talks']:
        match=re.search(r'(?:(\d{1,2}) )?([A-Za-z]{3}) (\d{4})',talk['date'])
        if match and match[2] in months:
            date=dt.date(int(match[3]),months[match[2]],int(match[1] or 1))
            if talk['status']=='upcoming' and ((match[1] and date<asof) or (date.year,date.month)<(asof.year,asof.month)):raise ValueError('Past announcement needs completed/attended evidence or past-scheduled status: '+talk['title'])
            if date>asof and talk['status'] in ['completed','attended']:raise ValueError('Future event cannot be completed: '+talk['title'])
    return profile

def validate_media(media):
    for item in media:
        if not item.get('alt','').strip():raise ValueError('Image needs alt text')
        web_url(item['source_url'])
        path=(ROOT/item['image']).resolve()
        if not path.is_relative_to(ROOT/'assets/images') or not path.is_file():raise ValueError('Invalid local image path')
    return media
if __name__=='__main__':
    validate_profile(json.loads((ROOT/'content/profile.json').read_text()))
    validate_media(json.loads((ROOT/'content/media.json').read_text()))
    print('Content and image provenance validated')
