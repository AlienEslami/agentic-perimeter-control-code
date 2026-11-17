# Two-region perimeter-control benchmark

See the repository [reproduction guide](../../REPRODUCING.md) for the manuscript result map, installation, offline checks and fresh-run sequence.

`common.py`, `vendor/` and the fixed `anchor.json` define the model, planning and verification implementations and minute-20 information state. `PROTOCOL.md` defines the experiment, while the other protocol files define the scenario-based planning, fresh backups, delays, sequential requests and optional agent studies. Protocols and source files used in certificate hashes retain their original bytes.

After `python scripts/prepare_records.py` is run from the repository root, `results/` contains the reported per-case plans, simulations, certificates and agent responses. The incomplete early integration and expiry-alignment runs are excluded. Failed checks from the reported parameter grid remain available.

Run `python audit.py` here for the model/derivative checks, or `python audit.py --replay` for the more extensive independent trajectory audit. These commands write audit outputs locally. API drivers are optional and incur charges; all reported responses are already archived.

The CLF benchmark is a local implementation of the equations cited in the manuscript. The predictive tools are local implementations with the planning horizons, control blocks and information sets in the protocols. Results are not outputs from the original authors' software.
