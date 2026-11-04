"""A CV refresh must not silently detach curated evidence from career records."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from spotlight import load_spotlight
from publication_access import load_access

class EvidenceReferenceTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ROOT/'content/profile.json').read_text())

    def test_removed_featured_award_requires_editorial_reconciliation(self):
        selected = load_spotlight(self.profile)['awards'][0]['title']
        self.profile['awards'] = [x for x in self.profile['awards'] if x['title'] != selected]
        with self.assertRaisesRegex(ValueError, 'Missing or ambiguous'):
            load_spotlight(self.profile)

    def test_removed_publication_cannot_leave_an_orphan_fulltext_link(self):
        selected = load_access(self.profile)[0]['publication_title']
        self.profile['publications'] = [x for x in self.profile['publications'] if x['title'] != selected]
        with self.assertRaisesRegex(ValueError, 'Missing or ambiguous'):
            load_access(self.profile)
