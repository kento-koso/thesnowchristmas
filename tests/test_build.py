"""Regression checks for dates, source-of-truth rules and cache invalidation."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from build import ROOT, asset_versions, event_values, substitute
from check import Page

class BuildTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/'config/event.json').read_text())
    def test_confirmed_event_and_exclusive_calendar_end(self):
        event=event_values(self.config)
        self.assertEqual((event['calendarStart'],event['calendarEnd']),('20261219','20261221'))
        self.assertEqual(event['dateJapanese'],'2026年12月19日（土）・20日（日）')
        self.assertEqual((event['startWeekday'],event['lastWeekday']),('SAT','SUN'))
    def test_calendar_month_rollover(self):
        event=event_values(dict(self.config,startDate='2026-01-30',lastDate='2026-01-31'))
        self.assertEqual(event['calendarEnd'],'20260201')
    def test_end_before_start_rejected(self):
        with self.assertRaises(ValueError):event_values(dict(self.config,lastDate='2026-12-18'))
    def test_cross_year_layout_requires_review(self):
        with self.assertRaises(ValueError):event_values(dict(self.config,lastDate='2027-01-01'))
    def test_unknown_template_token_rejected(self):
        with self.assertRaises(ValueError):substitute('{{event.typo}}',{'event.title':'Snow'})
    def test_shared_and_event_tokens(self):
        self.assertEqual(substitute('{{home}}#top / {{ event.year }}',{'home':'./','event.year':'2026'}),'./#top / 2026')
    def test_asset_revision_changes_only_with_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);asset=root/'main.js';asset.write_text('one')
            old=asset_versions('<script src="main.js?v=old"></script>',root)
            self.assertEqual(old,asset_versions(old,root))
            asset.write_text('two');self.assertNotEqual(old,asset_versions(old,root))
    def test_external_urls_unchanged(self):
        source='<script src="https://example.test/app.js?v=1"></script>'
        self.assertEqual(asset_versions(source),source)
    def test_missing_asset_fails_build(self):
        with self.assertRaises(ValueError):asset_versions('<script src="missing-file.js"></script>')
    def test_copy_baseline_ignores_formatting_and_scripts(self):
        self.assertEqual(Page('<body><p>雪が降る。</p><script>code</script><style>x{}</style><p>この街に。</p></body>').copy(),'雪が降る。この街に。')

if __name__=='__main__':unittest.main()
