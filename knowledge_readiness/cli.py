"""Review synthetic knowledge records using transparent deterministic checks."""
import argparse, csv, json
from datetime import date
from pathlib import Path
REQUIRED=("owner","service","last_reviewed","review_interval_days","purpose","preconditions","steps","validation","rollback_or_escalation","audience")
def assess(row,today):
 flags=[]
 for field in REQUIRED:
  if not row.get(field,"").strip(): flags.append("MISSING_"+field.upper())
 if row.get("last_reviewed","").strip():
  try:
   reviewed=date.fromisoformat(row["last_reviewed"]); interval=int(row.get("review_interval_days","")); age=(today-reviewed).days
   if age<0: flags.append("REVIEW_DATE_IN_FUTURE")
   elif age>interval: flags.append("REVIEW_OVERDUE")
  except (ValueError,TypeError): flags.append("INVALID_REVIEW_DATE_OR_INTERVAL")
 if row.get("owner","").strip() and row.get("owner_status","").lower()!="confirmed": flags.append("OWNER_UNCONFIRMED")
 if row.get("service","").strip() and row.get("service_status","").lower()!="confirmed": flags.append("SERVICE_MAPPING_UNCONFIRMED")
 if row.get("risk_level","").lower()=="high" and not row.get("rollback_or_escalation","").strip(): flags.append("HIGH_RISK_NO_ROLLBACK_OR_ESCALATION")
 return {"knowledge_id":row.get("knowledge_id",""),"title":row.get("title",""),"status":"HUMAN_REVIEW" if flags else "CHECKS_PASSED_REVIEW_REQUIRED","flags":sorted(set(flags)),"flag_count":len(set(flags))}
def run(source,out,today):
 with open(source,newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
 results=[assess(r,today) for r in rows]; out=Path(out); out.mkdir(parents=True,exist_ok=True)
 with open(out/"review.csv","w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["knowledge_id","title","status","flag_count","flags"]); w.writeheader()
  for r in results: w.writerow({**r,"flags":";".join(r["flags"])})
 summary={"review_date":today.isoformat(),"records_reviewed":len(results),"records_flagged":sum(bool(r["flags"]) for r in results),"flag_counts":{k:sum(k in r["flags"] for r in results) for k in sorted({x for r in results for x in r["flags"]})},"decision":"HUMAN_REVIEW_ONLY"}
 (out/"review.json").write_text(json.dumps({"summary":summary,"results":results},indent=2)+"\n",encoding="utf-8"); (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8"); return summary
def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument("--input",default="data/knowledge_items.csv"); p.add_argument("--output-dir",default="reports"); p.add_argument("--today",default=date.today().isoformat()); a=p.parse_args(); s=run(a.input,a.output_dir,date.fromisoformat(a.today)); print(f'Reviewed {s["records_reviewed"]} knowledge item(s); {s["records_flagged"]} flagged; human review required. Reports: {a.output_dir}')
if __name__=="__main__": main()
