"""Protect the restored visual homepage and visible event photographs."""
import html,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_site import check_site
class PortfolioNavigationTests(unittest.TestCase):
    def test_restored_navigation_and_compatibility_routes(self):
        check_site(ROOT)
        home=(ROOT/'index.html').read_text()
        for anchor in ['work','feedback','speaking','recognition','media','research','latest-events']:
            self.assertIn('id="'+anchor+'"',home)
        self.assertIn('href="index.html#work"',home)
        self.assertNotIn('id="legacy-routes"',home)
        for page,anchor in [('work','work'),('recognition','recognition'),('speaking','speaking')]:
            text=(ROOT/(page+'.html')).read_text()
            self.assertIn('id="restored-home" href="index.html#'+anchor+'"',text)
            self.assertIn('src="assets/restore-route.js"',text)
    def test_full_visual_evidence_stays_on_homepage(self):
        home=html.unescape((ROOT/'index.html').read_text())
        for item in json.loads((ROOT/'content/media.json').read_text()):
            if item['id']!='ktp-certificate' and item.get('gallery',True):
                self.assertIn('photo-'+item['id'],home)
        for item in json.loads((ROOT/'content/showcase.json').read_text())['appearances']:
            self.assertIn('id="'+item['id']+'"',home)
        for item in json.loads((ROOT/'content/leadership.json').read_text())['feedback']:
            self.assertIn(item['summary'],home)
        for item in json.loads((ROOT/'content/research-impact.json').read_text())['entries']:
            self.assertIn(item['summary'],home)
        for cls in ['book-feature','paper-visual','photo-gallery','credential-grid','appearance-grid','enterprise-stories']:
            self.assertIn('class="'+cls,home)
    def test_new_events_have_original_photos_and_full_post_links(self):
        home=(ROOT/'index.html').read_text()
        for name in ['barclays-panel-2026','innovation-awards-portrait','innovation-awards-2026']:
            self.assertIn('src="assets/images/'+name+'.jpg"',home)
        for post in ['3n24caf3iak25','3n2azgtu67c2z']:
            self.assertIn('href="https://bsky.app/profile/joyjitchat.bsky.social/post/'+post+'"',home)
        self.assertIn('href="#latest-events"',home)
