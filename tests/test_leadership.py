"""Protect anonymous feedback and the leadership-first editorial hierarchy."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from leadership import load_leadership, validate_leadership

class LeadershipTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ROOT/'content/profile.json').read_text())
        self.data = load_leadership(self.profile)

    def test_attribution_cannot_silently_add_a_personal_identity(self):
        self.data['feedback'][0]['name'] = 'Private reviewer'
        with self.assertRaisesRegex(ValueError, 'anonymous role'):
            validate_leadership(self.data, self.profile)

    def test_former_colleague_cannot_be_promoted_to_an_unverified_title(self):
        self.data['feedback'][3]['role'] = 'Head of Data Platform, EPAM'
        with self.assertRaisesRegex(ValueError, 'anonymous role'):
            validate_leadership(self.data, self.profile)

    def test_removed_executive_event_requires_editorial_reconciliation(self):
        title = self.data['engagements'][1]['record']['title']
        self.profile['talks'] = [x for x in self.profile['talks'] if x['title'] != title]
        with self.assertRaisesRegex(ValueError, 'Missing or ambiguous'):
            validate_leadership(self.data, self.profile)
