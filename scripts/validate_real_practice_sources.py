#!/usr/bin/env python3
"""Offline fidelity check: documented raw samples equal upstream-sourced fixture bytes."""
from pathlib import Path
import hashlib,json,re,sys
R=Path(__file__).resolve().parents[1]
P=R/'practice'
FAIL=[]
def check(condition,msg):
 if not condition:FAIL.append(msg)
def digest(blob):return hashlib.sha256(blob).hexdigest()
def lines(name):
 return (P/name).read_text(encoding='utf8').splitlines()
checks={
 'videos/complete.mdx':['01-juniper-srx.log'],
 'videos/partial.mdx':['02-sophos-xg.log'],
 'videos/unknown.mdx':['03-snort-alert.log','03-snort-holdout.log'],
 'videos/multiple-types.mdx':['04-fortigate-traffic.log','04-fortigate-threat.log'],
 'videos/relay.mdx':['05-relay-forwarded.log','05-relay-holdout.log'],
 'scenarios/relay-forwarder.mdx':['05-relay-original.log','05-relay-forwarded.log','05-relay-holdout.log'],
 'scenarios/normalization.mdx':['05-relay-original.log'],
 'scenarios/unnamed-values.mdx':['06-panos-traffic-issue.log'],
 'scenarios/long-events.mdx':['07-elasticsearch-java-error.log'],
 'scenarios/ai-invalid-response.mdx':['03-snort-alert.log','03-snort-holdout.log'],
 'scenarios/ai-test-change.mdx':['03-snort-alert.log','03-snort-holdout.log'],
 'scenarios/revisions.mdx':['01-juniper-srx.log'],
 'scenarios/test-sender.mdx':['05-relay-original.log'],
 'scenarios/recipe-ai.mdx':['02-sophos-xg.log'],
}
for page,files in checks.items():
 for loc in ('', 'ko/'):
  content=(R/(loc+page)).read_text(encoding='utf8')
  blocks=re.findall(r'^'+re.escape(chr(96)*3)+r'(?:text|csv|log)?\n(.*?)^'+re.escape(chr(96)*3),content,re.S|re.M)
  for file in files:
   source=(P/file).read_text(encoding='utf8').rstrip('\n')
   check(source in [b.rstrip("\n") for b in blocks], f'{loc}{page}: exact multiline source block for {file} missing or mutated')
source=lines('05-relay-original.log')
holdout=lines('05-relay-holdout-original.log')
captured=lines('05-relay-forwarded.log')
captured_hold=lines('05-relay-holdout.log')
check(source==lines('04-fortigate-traffic.log'),'05 original must equal published Fortinet traffic bytes')
check(holdout==lines('04-fortigate-threat.log')[:1],'05 holdout must equal first public Fortinet Web Filter event')
check(len(source)==2 and len(holdout)==1 and len(captured)==2 and len(captured_hold)==1,'event counts must be 2+1')
pattern=re.compile(r'^<134>[A-Z][a-z]{2} +[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2} relay01 forwarder: (.+)$')
for a,b in zip(captured+captured_hold,source+holdout):
 match=pattern.fullmatch(a)
 check(bool(match),'rsyslog wire header missing')
 if match:check(match.group(1)==b,'relay packet changed vendor message payload')
e=json.loads((P/'05-rsyslog-capture-evidence.json').read_text(encoding='utf8'))
for name,hash_ in e['source_sha256'].items():
 check(hash_==digest((P/name).read_bytes()),'source hash mismatch '+name)
for name,hash_ in e['capture_sha256'].items():
 check(hash_==digest((P/name).read_bytes()),'wire hash mismatch '+name)
check(e['source_payload_preserved_exactly']==True,'rsyslog evidence claims incomplete source')
for loc in ('videos/relay.mdx','ko/videos/relay.mdx','scenarios/relay-forwarder.mdx','ko/scenarios/relay-forwarder.mdx'):
 content=(R/loc).read_text(encoding='utf8')
 check('synthetic training' not in content and '합성된 교육용' not in content,loc+' still mislabels vendor source as synthetic')
if FAIL:
 print('\n'.join('FAIL '+x for x in FAIL))
 sys.exit(1)
print('PASS: '+str(2*len(checks))+' EN/KR scenario/video pages exact source blocks; rsyslog envelope, published payload identity and source/capture hashes verified.')
