#!/usr/bin/env python3
"""Capture *actual* rsyslog forwarded packets from published Fortinet log examples.

Run on a disposable Linux lab with rsyslogd. Does NOT restart the system
rsyslog service; starts one independent subprocess, listens on loopback UDP
only and cleans up its own temporary config. Ubuntu AppArmor constrains where
the independent rsyslogd can read its config and write its pid/work files.
This script is for generating evidence, not a production installation guide.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time

HERE=Path(__file__).resolve().parent
TRAIN=HERE/'05-relay-original.log'
HOLD=HERE/'05-relay-holdout-original.log'


def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def make_port()->int:
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        sock.bind(('127.0.0.1',0))
        return sock.getsockname()[1]


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=HERE)
    args=parser.parse_args()
    if not shutil.which('rsyslogd'):
        raise SystemExit('rsyslogd is required: this is a real rsyslog capture, not an emulator')
    sources=[line for p in (TRAIN,HOLD) for line in p.read_bytes().splitlines() if line]
    assert len(TRAIN.read_bytes().splitlines())==2 and len(HOLD.read_bytes().splitlines())==1
    # On Ubuntu the active rsyslogd AppArmor profile permits configs under
    # /etc/rsyslog.d and writable spool state under /var/spool/rsyslog.
    # Use a *.tmp file NOT matched by the system service's *.conf glob.
    if os.geteuid()!=0:
        raise SystemExit('Root required by this host rsyslog AppArmor policy; run only in an isolated lab')
    ephemeral=Path(tempfile.mkdtemp(prefix='parserstudio-source-',dir='/var/spool/rsyslog'))
    config=Path('/etc/rsyslog.d')/(ephemeral.name+'.tmp')
    in_port,out_port=make_port(),make_port()
    while in_port==out_port:out_port=make_port()
    config.write_text(
        f'global(workDirectory="{ephemeral}")\n'
        'module(load="imudp")\n'
        'template(name="PSRelayWire" type="string" '
        'string="<134>%timegenerated:::date-rfc3164% relay01 forwarder: %rawmsg%\\n")\n'
        f'ruleset(name="relay") {{action(type="omfwd" target="127.0.0.1" port="{out_port}" '
        'protocol="udp" template="PSRelayWire") stop}\n'
        f'input(type="imudp" address="127.0.0.1" port="{in_port}" ruleset="relay")\n'
    )
    version=subprocess.run(['rsyslogd','-v'],capture_output=True,text=True,check=True).stdout.splitlines()[0]
    proc=None
    try:
        check=subprocess.run(['rsyslogd','-N1','-f',str(config)],capture_output=True,text=True)
        if check.returncode:
            raise RuntimeError('Isolated rsyslog config invalid: '+check.stderr)
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as collector:
            collector.bind(('127.0.0.1',out_port))
            collector.settimeout(7)
            with open(ephemeral/'stderr.log','wb') as stderr:
                proc=subprocess.Popen(
                    ['rsyslogd','-n','-f',str(config),'-i',str(ephemeral/'rsyslog.pid')],
                    stdout=subprocess.DEVNULL,stderr=stderr
                )
                time.sleep(1.0)
                if proc.poll() is not None:
                    raise RuntimeError('rsyslogd exited before receiving packets')
                captures=[]
                with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as source:
                    for i,raw in enumerate(sources):
                        source.sendto(raw,('127.0.0.1',in_port))
                        wire,_=collector.recvfrom(65535)
                        if not wire.startswith(b'<134>') or b' relay01 forwarder: ' not in wire:
                            raise RuntimeError('Actual relay output did not contain expected wire envelope')
                        if not wire.endswith(raw+b'\n'):
                            raise RuntimeError('Source payload bytes lost, escaped, or changed by forwarding')
                        captures.append(wire.rstrip(b'\n'))
                        print(f'RSYSLOG_FORWARDED_EVENT={i+1} original={len(raw)}B captured={len(wire)}B',flush=True)
        assert len(captures)==3
        args.output_dir.mkdir(parents=True,exist_ok=True)
        files={
            '05-relay-forwarded.log':b'\n'.join(captures[:2])+b'\n',
            '05-relay-holdout.log':captures[2]+b'\n'
        }
        for name,content in files.items():
            target=args.output_dir/name
            target.write_bytes(content)
            print(f'{name} {len(content)} bytes SHA256={sha(content)}',flush=True)
        evidence={
            'classification':'REAL_RSYSLOG_WIRE_CAPTURE_OF_PUBLIC_MANUFACTURER_SAMPLES',
            'origin':'Fortinet Document Library FortiOS 6.2.0 sample logs by log type',
            'origin_url':'https://docs.fortinet.com/document/fortigate/6.2.0/cookbook/986892/sample-logs-by-log-type',
            'origin_is_real_published_vendor_sample':True,
            'transmission':'actual rsyslogd imudp -> omfwd UDP on loopback, independent process',
            'rsyslog_version':version,
            'profile':'RFC3164 PRI=134, hostname=relay01, app=forwarder',
            'source_payload_preserved_exactly':True,
            'transport_scope':'127.0.0.1 only, no production equipment or live Stellar target',
            'source_sha256':{p.name:sha(p.read_bytes()) for p in (TRAIN,HOLD)},
            'capture_sha256':{name:sha(content) for name,content in files.items()},
            'source_events':2,'independent_holdout_events':1,
            'parser_studio_expected_status':'requires separate browser test, not asserted by this script'
        }
        (args.output_dir/'05-rsyslog-capture-evidence.json').write_text(
            json.dumps(evidence,indent=2,ensure_ascii=False)+'\n'
        )
        print('RSYSLOG_CAPTURE_PASS 3/3 real vendor example payloads forwarded and byte preserved')
    finally:
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=6)
        config.unlink(missing_ok=True)
        shutil.rmtree(ephemeral,ignore_errors=True)


if __name__=='__main__':
    main()
