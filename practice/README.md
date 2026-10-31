# Actual Fortinet vendor logs forwarded with actual rsyslogd

Source: [Fortinet Document Library, FortiOS 6.2.0, Sample logs by log type](https://docs.fortinet.com/document/fortigate/6.2.0/cookbook/986892/sample-logs-by-log-type).

**All security-event payload lines are verbatim official published samples** also used in the existing FortiGate multiple-event-type training. These are not customer logs, and the published vendor example is not a live appliance capture from the lab.

- `05-relay-original.log`: Fortinet Traffic events (two lines), no relay header.
- `05-relay-forwarded.log`: two actual UDP packets as output by rsyslogd, one per line, with RFC3164 wrapper on each.
- `05-relay-holdout-original.log`: independently selected official Fortinet Web Filter event (one line).
- `05-relay-holdout.log`: the actual rsyslogd UDP output for the holdout event.
- `05-rsyslog-capture-evidence.json`: SHA-256 checksums, rsyslog version and capture method.
- `capture_with_rsyslog.py`: optional real rsyslogd lab capture, NOT a text-based relay simulator.

The rsyslog input used `imudp` and forwarded to a loopback UDP collector with `omfwd`. A custom output template prepended a **new relay-generated** RFC3164 header and retained the full original text via `%rawmsg%`. The captured packets are not manufacturer-issued Syslog wrappers and are not evidence of connectivity to any Stellar Cyber deployment.

**Browser verification:** on the current deployed Parser Studio Web UI, 2/2 forwarded Traffic events fully parsed and a separate 1/1 forwarded Web Filter holdout fully parsed after explicit `relay01` declaration. No live Stellar runtime was involved.
