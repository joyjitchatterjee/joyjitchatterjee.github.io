"""The shorter homepage must not lose evidence or strand shared links."""
import html
import json
import sys
import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_site import Document,check_site

class PortfolioNavigationTests(unittest.TestCase):
    def test_all_pages_and_legacy_destinations_resolve(self):
        check_site(ROOT)
        home=(ROOT/'index.html').read_text()
        raw=home.split('<script type="application/json" id="legacy-routes">')[1].split('</script>')[0]
        routes=json.loads(raw)
        self.assertEqual(routes['procurement-ai'],'work.html#procurement-ai')
        self.assertEqual(routes['impact-ucl'],'research.html#impact-ucl')
        for target in routes.values():
            page,anchor=target.split('#')
            self.assertIn(anchor,Document((ROOT/page).read_text()).ids)
        for page in ['work','recognition','speaking','research','profile']:
            text=(ROOT/(page+'.html')).read_text()
            self.assertIn(f'href="{page}.html" aria-current="page"',text)
            self.assertIn(f'href="{page}.html"',home)

    def test_all_gallery_media_feedback_and_research_survive_the_move(self):
        speaking=(ROOT/'speaking.html').read_text()
        recognition=(ROOT/'recognition.html').read_text()
        research=html.unescape((ROOT/'research.html').read_text())
        work=html.unescape((ROOT/'work.html').read_text())
        for item in json.loads((ROOT/'content/media.json').read_text()):
            if item['id']!='ktp-certificate' and item.get('gallery',True):
                self.assertIn('photo-'+item['id'],speaking)
        for item in json.loads((ROOT/'content/showcase.json').read_text())['appearances']:
            self.assertIn('id="'+item['id']+'"',speaking)
        for item in json.loads((ROOT/'content/leadership.json').read_text())['feedback']:
            self.assertIn(item['summary'],work)
            self.assertIn(item['role'],work)
        for item in json.loads((ROOT/'content/research-impact.json').read_text())['entries']:
            self.assertIn(item['summary'],research)
        self.assertIn('book-feature',research)
        self.assertIn('paper-visual',research)
        self.assertIn('innovation-awards-2026.jpg',recognition)

    def test_home_stays_a_concise_overview(self):
        home=(ROOT/'index.html').read_text()
        self.assertLess(home.count('<img '),7)
        self.assertLess(len(home),20000)
        for section in ['photo-gallery','appearance-grid','research-impact-grid','award-timeline']:
            self.assertNotIn('class="'+section+'"',home)
        for highlight in ['Forbes','ETH Zurich','Outstanding','Green Talents','Barclays','evaluated business case']:
            self.assertIn(highlight,home)
