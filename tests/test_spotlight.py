"""A CV refresh must not silently detach curated evidence from career records."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from spotlight import load_spotlight
from publication_access import load_access
from validate import validate_media, validate_showcase

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

    def test_personal_archive_requires_traceable_original(self):
        media = json.loads((ROOT/'content/media.json').read_text())
        item = next(x for x in media if x.get('source_kind') == 'user-provided')
        item.pop('original_sha256')
        with self.assertRaisesRegex(ValueError, 'original SHA-256'):
            validate_media(media)

    def test_personal_archive_cannot_publish_an_absolute_source_path(self):
        media = json.loads((ROOT/'content/media.json').read_text())
        item = next(x for x in media if x.get('source_kind') == 'user-provided')
        item['source_file'] = '/Users/private/Documents/photo.jpg'
        with self.assertRaisesRegex(ValueError, 'source filename'):
            validate_media(media)

    def test_case_image_reference_must_resolve(self):
        showcase = json.loads((ROOT/'content/showcase.json').read_text())
        showcase['cases'][0]['media_id'] = 'removed-photo'
        with self.assertRaisesRegex(ValueError, 'Unknown showcase media'):
            validate_showcase(showcase, self.profile)

    def test_case_paper_reference_must_resolve(self):
        showcase = json.loads((ROOT/'content/showcase.json').read_text())
        showcase['cases'][0]['download_id'] = 'removed-paper'
        with self.assertRaisesRegex(ValueError, 'Unknown showcase download'):
            validate_showcase(showcase, self.profile)
