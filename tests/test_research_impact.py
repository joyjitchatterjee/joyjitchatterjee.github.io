import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from research_impact import load_impact


class ResearchImpactEvidenceTests(unittest.TestCase):
    def test_rejects_source_url_mismatch(self):
        profile = json.loads((ROOT / 'content/profile.json').read_text())
        data = load_impact(profile)
        data['entries'][0]['url'] = 'https://example.com/unrelated-claim'
        original = Path.read_text
        def reader(path, *args, **kwargs):
            return json.dumps(data) if path.name == 'research-impact.json' else original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', reader), self.assertRaisesRegex(ValueError, 'source does not match'):
            load_impact(profile)

    def test_rejects_missing_coauthored_work(self):
        profile = json.loads((ROOT / 'content/profile.json').read_text())
        profile['publications'] = []
        with self.assertRaisesRegex(ValueError, 'Unknown research impact publication'):
            load_impact(profile)
