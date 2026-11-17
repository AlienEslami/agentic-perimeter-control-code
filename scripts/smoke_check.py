"""Independent local numerical checks; no optimization sweep or API requests."""
from pathlib import Path
import importlib.util
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / 'benchmarks/reusable_perimeter_suite_2026-09-26'
sys.path.insert(0, str(SUITE))
import common
import audit

def main():
    model = audit.initial_audit()
    case = json.loads((SUITE / 'results/contracts/D027.json').read_text())
    policy = case['policies']['grid_repair']
    actual = common.adaptive_replay(np.asarray(policy['commands']), case['contract'], profile='constant_high')
    saved = next(r for r in policy['realizations'] if r['corner'] == '+++++++' and r['profile'] == 'constant_high')
    keys = ('tts_veh_h', 'queue_veh_h', 'completed_trips', 'priority_cost', 'deadline_n1_vehicles', 'peak_queue_vehicles')
    differences = {key: abs(actual[key] - saved[key]) for key in keys}
    assert max(differences.values()) < .08, differences
    assert abs(actual['conservation_residual_vehicles']) < 1e-6
    folder = ROOT / 'benchmarks/reviewer_strengthening_2026-11-11'
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location('interval_validation', folder / 'validate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    arithmetic = module.validate_arithmetic()
    print(json.dumps({'passed': True, 'model_checks': model,
                      'independent_replay_absolute_differences': differences,
                      'interval_arithmetic': arithmetic}, indent=2))

if __name__ == '__main__':
    main()
