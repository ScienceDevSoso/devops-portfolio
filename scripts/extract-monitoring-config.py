#!/usr/bin/env python3
"""Extract rendered config and dashboard PromQL for promtool validation.

Usage: python3 scripts/extract-monitoring-config.py rendered.yaml output-directory
Requires PyYAML (validation dependency only).
"""
import json
from pathlib import Path
import sys

import yaml

output = Path(sys.argv[2])
output.mkdir(parents=True, exist_ok=True)
resources = list(yaml.safe_load_all(Path(sys.argv[1]).read_text()))
for resource in resources:
    if resource and resource['kind'] == 'ConfigMap':
        data = resource['data']
        if 'prometheus.yml' in data:
            (output / 'prometheus.yml').write_text(data['prometheus.yml'])
        if 'overview.json' in data:
            dashboard = json.loads(data['overview.json'])
            rules = [{'record': f'validation:panel_{p["id"]}', 'expr': t['expr']}
                     for p in dashboard['panels'] for t in p['targets']]
            (output / 'dashboard-rules.yml').write_text(yaml.safe_dump(
                {'groups': [{'name': 'dashboard-validation', 'rules': rules}]}))
for name in ('prometheus.yml', 'dashboard-rules.yml'):
    if not (output / name).is_file():
        raise SystemExit(f'Missing rendered configuration: {name}')
print('Extracted Prometheus configuration and dashboard queries.')
