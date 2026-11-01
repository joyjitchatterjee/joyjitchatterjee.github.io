import copy
import datetime as dt
import importlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate import validate_profile,validate_media
from refresh_cv import extract,removals
from build import e

class ContentTests(unittest.TestCase):
    def setUp(self):self.profile=json.loads((ROOT/'content/profile.json').read_text())
    def test_valid_current_content(self):
        validate_profile(self.profile);validate_media(json.loads((ROOT/'content/media.json').read_text()))
    def test_unsafe_publication_link_rejected(self):
        self.profile['publications'][0]['url']='javascript:alert(1)'
        with self.assertRaises(ValueError):validate_profile(self.profile)
    def test_duplicate_record_rejected(self):
        self.profile['talks'].append(self.profile['talks'][0])
        with self.assertRaises(ValueError):validate_profile(self.profile)
    def test_future_event_not_completed(self):
        self.profile['talks'][0].update(date='10 Nov 2099',status='completed')
        with self.assertRaises(ValueError):validate_profile(self.profile)
    def test_past_announcement_is_not_upcoming(self):
        self.profile['talks'][0].update(date='10 Nov 2000',status='upcoming')
        with self.assertRaises(ValueError):validate_profile(self.profile)
    def test_unknown_evidence_rejected(self):
        self.profile['publications'][0]['source']='made-up'
        with self.assertRaises(ValueError):validate_profile(self.profile)
    def test_html_is_escaped(self):
        self.assertEqual(e('<script>alert("x")</script>'),'&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;')
    def test_removals_cover_additional_records(self):
        old=copy.deepcopy(self.profile);self.profile['additional'][0]['items'].pop()
        self.assertTrue(removals(old,self.profile))
    def test_docx_extraction(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'my CV.docx'
            xml='<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>'+('Professional experience and research. '*8)+'</w:t></w:r></w:p></w:body></w:document>'
            with zipfile.ZipFile(path,'w') as archive:archive.writestr('word/document.xml',xml)
            self.assertIn('Professional experience',extract(path))
    def test_empty_document_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'cv.txt';path.write_text('')
            with self.assertRaises(ValueError):extract(path)

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'site';self.root.mkdir()
        for name in ['scripts','content','assets','templates']:shutil.copytree(ROOT/name,self.root/name)
        for name in ['index.html','research.html','profile.html']:shutil.copy(ROOT/name,self.root/name)
        self.cv=self.root/'sample CV.txt';self.cv.write_text('Dr. Joyjit Chatterjee\nLead Data Scientist at EPAM Systems.\n'+('Research in explainable AI and knowledge graphs. '*6))
        self.invoke(str(self.cv),'--prepare-only')
        self.run=next((self.root/'.cv-refresh').iterdir())
        self.metadata=json.loads((self.run/'metadata.json').read_text())
        self.result={'profile':json.loads((self.root/'content/profile.json').read_text()),'notes':['Refreshed from the supplied CV.'],'unresolved':[]}
        self.result['profile']['updated']=self.metadata['date']
        for talk in self.result['profile']['talks']:
            if talk['status']=='upcoming':
                try:event=dt.datetime.strptime(talk['date'],'%d %b %Y').date()
                except ValueError:continue
                if event<dt.date.fromisoformat(self.metadata['date']):talk['status']='past-scheduled'
        self.result['profile']['about']+=' Research interests include trustworthy AI.'
        self.result['profile']['experience'][0]['source']=self.metadata['sources'][0]['id']
        self.candidate=self.run/'candidate.json'
    def tearDown(self):self.temp.cleanup()
    def invoke(self,*args,ok=True):
        r=subprocess.run([sys.executable,str(self.root/'scripts/refresh_cv.py'),*args],capture_output=True,text=True)
        self.assertEqual(r.returncode==0,ok,r.stdout+r.stderr);return r
    def apply(self,ok=True):
        self.candidate.write_text(json.dumps(self.result))
        return self.invoke('--run',str(self.run),'--candidate',str(self.candidate),'--apply',ok=ok)
    def test_apply_builds_and_records_sources(self):
        self.apply()
        self.assertIn('Research interests include trustworthy AI.',(self.root/'profile.html').read_text())
        self.assertTrue((self.run/'report.md').exists())
        self.assertIn(self.metadata['sources'][0]['id'],(self.root/'content/sources.json').read_text())
    def test_unresolved_leaves_content_untouched(self):
        before=(self.root/'content/profile.json').read_bytes();self.result['unresolved']=['Conflicting dates.'];self.apply(ok=False)
        self.assertEqual(before,(self.root/'content/profile.json').read_bytes())
    def test_stale_baseline_rejected(self):
        path=self.root/'content/profile.json';path.write_text(path.read_text()+'\n');before=path.read_bytes();self.apply(ok=False)
        self.assertEqual(before,path.read_bytes())
    def test_history_loss_rejected(self):
        self.result['profile']['publications'].pop();self.apply(ok=False)
    def test_build_failure_rolls_back(self):
        before={p:(self.root/p).read_bytes() for p in ['content/profile.json','content/sources.json','index.html']}
        (self.root/'templates/base.html').write_text('$unknown_variable')
        self.apply(ok=False)
        for path,value in before.items():self.assertEqual(value,(self.root/path).read_bytes())
if __name__=='__main__':unittest.main()
