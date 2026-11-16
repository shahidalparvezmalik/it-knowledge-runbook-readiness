import unittest
from datetime import date
from knowledge_readiness.cli import assess
class AssessmentTests(unittest.TestCase):
 def base(self): return {"knowledge_id":"K1","title":"Test","owner":"Team A","owner_status":"confirmed","service":"Mail","service_status":"confirmed","last_reviewed":"2026-01-01","review_interval_days":"180","purpose":"Restore access","preconditions":"Incident confirmed","steps":"Check queue","validation":"User confirms","rollback_or_escalation":"Escalate to service owner","audience":"On-call","risk_level":"medium"}
 def test_complete_current_record_still_requires_review(self):
  r=self.base(); r["last_reviewed"]="2026-11-01"; self.assertEqual(assess(r,date(2026,11,16))["status"],"CHECKS_PASSED_REVIEW_REQUIRED")
 def test_overdue_and_unconfirmed_mapping(self):
  r=self.base(); r["service_status"]="unconfirmed"; flags=assess(r,date(2026,11,16))["flags"]; self.assertIn("REVIEW_OVERDUE",flags); self.assertIn("SERVICE_MAPPING_UNCONFIRMED",flags)
 def test_missing_operational_fields(self):
  r=self.base(); r["validation"]=""; self.assertIn("MISSING_VALIDATION",assess(r,date(2026,11,16))["flags"])
 def test_future_review_date(self):
  r=self.base(); r["last_reviewed"]="2026-12-01"; self.assertIn("REVIEW_DATE_IN_FUTURE",assess(r,date(2026,11,16))["flags"])
if __name__=="__main__": unittest.main()
