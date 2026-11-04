#!/usr/bin/env python3
"""Small dependency-free validator for the repository's JSON schema subset."""
import hashlib
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
def check(value,schema,path='$'):
    types={'object':dict,'array':list,'string':str,'integer':int}
    if not isinstance(value,types[schema['type']]):raise ValueError(f'{path}: expected {schema["type"]}')
    if isinstance(value,dict):
        expected=set(schema['required'])
        invalid=(expected-set(value)) | (set(value)-set(schema['properties']))
        if invalid:raise ValueError(f'{path}: wrong keys: {invalid}')
        for k,v in value.items():check(v,schema['properties'][k],path+'.'+k)
    elif isinstance(value,list):
        if len(value)>schema.get('maxItems',1000):raise ValueError(f'{path}: too many items')
        for i,v in enumerate(value):check(v,schema['items'],f'{path}[{i}]')
    elif isinstance(value,str):
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
    for k in ['linkedin','scholar','github','bluesky']:web_url(profile[k])
    known={s['id'] for s in json.loads((ROOT/'content/sources.json').read_text())}|set(extra_sources)
    def walk(x):
        if isinstance(x,dict):
            if 'source' in x and x['source'] not in known:raise ValueError('Unknown source: '+x['source'])
            if 'title' in x and not x['title'].strip():raise ValueError('Empty title')
            if x.get('url'):web_url(x['url'])
            if 'details' in x:
                headings=[group['heading'].strip().casefold() for group in x['details']]
                if len(headings)!=len(set(headings)) or any(not h for h in headings):raise ValueError('Duplicate or blank detail headings')
                for group in x['details']:
                    if not group['points'] or any(not point.strip() for point in group['points']):raise ValueError('Empty detail group')
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
    validate_coverage(profile)
    return profile

def validate_media(media):
    known={x['id'] for x in json.loads((ROOT/'content/sources.json').read_text())}
    ids=set()
    for item in media:
        if item['id'] in ids:raise ValueError('Duplicate media ID')
        ids.add(item['id'])
        if not item.get('alt','').strip():raise ValueError('Image needs alt text')
        if item.get('source_kind')=='user-provided':
            if item.get('source') not in known:raise ValueError('Unknown local media source')
            if not item.get('source_file','').strip() or item['source_file'].startswith('/') or '..' in item['source_file']:raise ValueError('Invalid source filename')
            if not re.fullmatch(r'[a-f0-9]{64}',item.get('original_sha256','')):raise ValueError('Local media needs original SHA-256')
        else:
            web_url(item['source_url'])
            web_url(item['source_image_url'])
        dt.date.fromisoformat(item['accessed'])
        if 'gallery' in item and type(item['gallery']) is not bool:raise ValueError('Invalid gallery setting')
        for dimension in ['width','height']:
            if type(item.get(dimension)) is not int or not 0<item[dimension]<=20000:raise ValueError('Invalid image dimensions')
        path=(ROOT/item['image']).resolve()
        if not path.is_relative_to(ROOT/'assets/images') or not path.is_file():raise ValueError('Invalid local image path')
    return media
def profile_record(profile,reference):
    section=reference['section']
    if section.startswith('additional.'):
        items=next((x['items'] for x in profile['additional'] if x['id']==section.split('.',1)[1]),[])
    else:
        items=profile.get(section,[])
    matches=[x for x in items if isinstance(x,dict) and x.get('title')==reference['title']]
    if len(matches)!=1:raise ValueError('Missing or ambiguous protected record: '+reference['title'])
    return matches[0]

def validate_coverage(profile):
    for item in json.loads((ROOT/'content/coverage.json').read_text()):
        profile_record(profile,item['record'])
        if item['surface'] not in ['index.html','profile.html','research.html']:raise ValueError('Invalid coverage surface')

def validate_showcase(showcase,profile):
    check(showcase,json.loads((ROOT/'content/showcase.schema.json').read_text()))
    known={x['id'] for x in json.loads((ROOT/'content/sources.json').read_text())}
    media_ids={x['id'] for x in json.loads((ROOT/'content/media.json').read_text())}
    ids=[]
    def walk(item):
        if isinstance(item,list):
            for x in item:walk(x)
        elif isinstance(item,dict):
            if 'media_id' in item and item['media_id'] not in media_ids:raise ValueError('Unknown showcase media')
            if 'source' in item and item['source'] not in known:raise ValueError('Unknown showcase source')
            if 'record' in item:profile_record(profile,item['record'])
            if 'id' in item:
                if not re.fullmatch(r'[a-z][a-z0-9-]*',item['id']):raise ValueError('Invalid showcase ID')
                ids.append(item['id'])
            if 'url' in item:
                url=item['url']
                if url.startswith('https://'):web_url(url)
                elif not re.fullmatch(r'(profile|research)\.html#[a-z][a-z0-9-]*',url):raise ValueError('Unsafe showcase URL: '+url)
            if 'image' in item and item['image']['path']:
                im=item['image'];web_url(im['source_url']);dt.date.fromisoformat(im['accessed'])
                path=(ROOT/im['path']).resolve()
                if not path.is_relative_to(ROOT/'assets/images') or not path.is_file():raise ValueError('Missing showcase image')
                if not im['alt'].strip() or any(type(im[k]) is not int or not 0<im[k]<=20000 for k in ['width','height']):raise ValueError('Invalid showcase image metadata')
            for x in item.values():walk(x)
    walk(showcase)
    if len(set(ids))!=len(ids):raise ValueError('Duplicate showcase IDs')
    for title in showcase['featured_publications']:profile_record(profile,{'section':'publications','title':title})
    for title in showcase['featured_certifications']:profile_record(profile,{'section':'certifications','title':title})
    return showcase

def validate_downloads(downloads,profile):
    if not isinstance(downloads,list):raise ValueError('Downloads must be a list')
    ids=[]
    fields={'id','publication_title','file','preview','preview_width','preview_height','summary','pages','bytes','sha256','source_url','licence','added'}
    for item in downloads:
        if not isinstance(item,dict) or set(item)!=fields:raise ValueError('Invalid download metadata')
        if not re.fullmatch(r'[a-z][a-z0-9-]*',item['id']):raise ValueError('Invalid download ID')
        ids.append(item['id'])
        profile_record(profile,{'section':'publications','title':item['publication_title']})
        web_url(item['source_url']);dt.date.fromisoformat(item['added'])
        for key in ['pages','bytes','preview_width','preview_height']:
            if type(item[key]) is not int or item[key]<=0:raise ValueError('Invalid PDF size or dimensions')
        pdf=(ROOT/item['file']).resolve()
        if not pdf.is_relative_to(ROOT/'assets/papers') or pdf.suffix!='.pdf' or not pdf.is_file():raise ValueError('Invalid local PDF path')
        data=pdf.read_bytes()
        if not data.startswith(b'%PDF-') or len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:raise ValueError('PDF integrity mismatch')
        preview=(ROOT/item['preview']).resolve()
        if not preview.is_relative_to(ROOT/'assets/images') or not preview.is_file():raise ValueError('Missing paper preview')
        for key in ['summary','licence']:
            if not isinstance(item[key],str) or not item[key].strip():raise ValueError('Missing PDF description or licence')
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate download IDs')
    return downloads

if __name__=='__main__':
    profile=validate_profile(json.loads((ROOT/'content/profile.json').read_text()))
    validate_media(json.loads((ROOT/'content/media.json').read_text()))
    validate_showcase(json.loads((ROOT/'content/showcase.json').read_text()),profile)
    validate_downloads(json.loads((ROOT/'content/downloads.json').read_text()),profile)
    print('Content, protected credentials, image provenance and PDF downloads validated')
