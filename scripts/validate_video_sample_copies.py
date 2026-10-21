#!/usr/bin/env python3
"""Offline regression guard for the exact public training records embedded in English/Korean MDX."""
from pathlib import Path
import hashlib
import json
import re
import sys

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/"scripts/video-sample-hashes.json").read_text(encoding="utf-8"))
sample_map={
"complete":["01-juniper-srx.log"],
"partial":["02-sophos-xg.log"],
"unknown":["03-snort-alert.log","03-snort-holdout.log"],
"multiple-types":["04-fortigate-traffic.log","04-fortigate-threat.log"]
}
F=chr(96)*3
errors=[]
tested=0
for scenario,names in sample_map.items():
 for prefix in ("","ko/"):
  for area, filename in (("videos",scenario),("scenarios",{"complete":"auto-success","partial":"partial-event","unknown":"unknown-log","multiple-types":"mixed-events"}[scenario])):
   page=root/prefix/area/(filename+".mdx")
   original=page.read_text(encoding="utf-8")
   if original.count("PARSER-STUDIO-EXACT-SAMPLE-START")!=1 or original.count("PARSER-STUDIO-EXACT-SAMPLE-END")!=1:
    errors.append(f"{page.relative_to(root)}: missing or duplicate exact-source markers")
    continue
   block=original.split("PARSER-STUDIO-EXACT-SAMPLE-START",1)[1].split("PARSER-STUDIO-EXACT-SAMPLE-END",1)[0]
   chunks=re.findall(re.escape(F)+r"text\n(.*?)\n"+re.escape(F),block,flags=re.DOTALL)
   if len(chunks)!=len(names):
    errors.append(f"{page.relative_to(root)}: expected {len(names)} text blocks; got {len(chunks)}")
    continue
   for actual,name in zip(chunks,names):
    if name not in block:
     errors.append(f"{page.relative_to(root)}: missing source label {name}")
    data=actual.encode("utf-8")
    expected=manifest[name]
    if len(data)!=expected["size_bytes"] or hashlib.sha256(data).hexdigest()!=expected["sha256"]:
     errors.append(f"{page.relative_to(root)}: source does not match published SHA-256: {name}")
    tested+=1
   json_chunks=re.findall(re.escape(F)+r"json\n(.*?)\n"+re.escape(F),block,flags=re.DOTALL)
   if scenario=="unknown":
    if len(json_chunks)!=1:
     errors.append(f"{page.relative_to(root)}: missing the approved-for-testing recipe example")
    else:
     name="03-snort-reviewed-recipe.json"
     payload=json_chunks[0].encode("utf-8")
     if len(payload)!=manifest[name]["size_bytes"]-1 or hashlib.sha256(payload+b"\n").hexdigest()!=manifest[name]["sha256"]:
      errors.append(f"{page.relative_to(root)}: example JSON does not match downloaded recipe")
     try:
      value=json.loads(payload)
      if value["nativeVerified"] is not False or value["targetVerified"] is not False:
       errors.append(f"{page.relative_to(root)}: missing explicit unverified status")
     except (ValueError,KeyError) as exc:errors.append(f"{page.relative_to(root)}: invalid JSON {exc}")
   elif json_chunks:
    errors.append(f"{page.relative_to(root)}: unexpected JSON block")
# The end-to-end examples require the full original data, not snippets.
if len(manifest)!=7: errors.append(f"Unexpected manifest file count: {len(manifest)}")
if tested!=24:errors.append(f"Wrong number of documented original log blocks: {tested} (expected 24)")
if errors:
 for item in errors:print("FAIL:",item)
 sys.exit(1)
print(f"PASS: {tested} exact published source blocks in 16 English/Korean pages, 4 matching JSON examples; byte counts, SHA-256, unverified flags and scenario group boundaries checked.")
