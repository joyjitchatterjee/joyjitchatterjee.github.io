import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from research_reach import load_reach,render_reach

class ResearchReachTests(unittest.TestCase):
    def test_metrics_keep_platform_date_and_partial_year_context(self):
        data=load_reach();rendered=render_reach(data)
        self.assertIn('3 November 2026',rendered)
        self.assertIn('2026 is a partial year',rendered)
        self.assertIn('Google Scholar citations',rendered)
        self.assertIn('ResearchGate reads',rendered)
        self.assertIn('not unique readers',rendered)
        self.assertEqual(rendered.count('class="citation-year"'),len(data['scholar']['years']))

    def test_rejects_unverified_video_origin(self):
        data=load_reach();data['videos']['green-talents-film']['url']='https://example.com/untrusted.mp4'
        original=Path.read_text
        def reader(path,*a,**kw):
            return json.dumps(data) if path.name=='reach.json' else original(path,*a,**kw)
        with patch.object(Path,'read_text',reader),self.assertRaisesRegex(ValueError,'Unapproved video origin'):
            load_reach()
