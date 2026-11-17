# Reproduction guide

[Repository home](README.md) · [Study-to-code guide](docs/STUDIES.md)

Use Python 3.12 and install the root [`requirements.txt`](requirements.txt) in a virtual environment, as shown in the [quick start](README.md#quick-start). Run the commands below from the repository root. The current `main` branch provides the `reproduce.py` entry point; the fixed paper release has the individual commands listed in its own guide.

## Choose what to reproduce

| Goal | Command | Result |
|---|---|---|
| Inspect the saved data | `python reproduce.py prepare` | Unpacks and hash-checks the numerical records |
| Check the package and reported summaries | `python reproduce.py check` | Integrity audit, summary checks and a small independent numerical check |
| Recreate the main recovery plots | `python reproduce.py figures` | Four files in `output/figures/`: PDF and PNG for each network |
| Run new three-region simulations and verification | `python reproduce.py three-region --output-dir reruns/three-region-01` | New proof records, ensemble simulations and summary in the chosen directory |

`python reproduce.py --help` lists these commands. All four run without language-model API calls. The fresh study requires more computation than checking saved results.

## What the offline checks establish

`check` runs the following steps in order and stops if any fails:

1. [`prepare_records.py`](scripts/prepare_records.py) verifies the archive and restores 714 saved records. An existing record with different contents is preserved and reported as an error.
2. [`audit_repository_records.py`](scripts/audit_repository_records.py) checks all files in the reproduction manifest, parses the distributed Python sources, and checks 994 stored certificate records against their descriptors, exact control inputs and bound source files.
3. [`audit_current_results_2026_11_15.py`](scripts/audit_current_results_2026_11_15.py) recomputes selected reported summaries, including the matched 640-simulation comparisons, larger state-error cases, model perturbations and 80-case acceptance grid.
4. [`smoke_check.py`](scripts/smoke_check.py) checks the model derivatives and interval arithmetic and independently simulates one saved adverse trajectory.

A successful run ends with **`All offline checks passed.`** The command validates the supplied evidence and the selected numerical checks; it does not rerun every optimizer or reconstruct every certificate.

## Recreate figures

```sh
python reproduce.py figures
```

This produces:

```text
output/figures/
  two-region-recovery.pdf
  two-region-recovery.png
  three-region-recovery.pdf
  three-region-recovery.png
```

The plots use the saved trajectories and verified bounds. The three-region figure includes all three entry queues. The underlying plotting scripts also write their source-data checks and original-named figures under `output/review/` and `output/package/`.

For the supporting numerical plots, run:

```sh
python -B scripts/reproduce_current_figures_2026_11_15.py
```

Those figures are written under `output/package/PERIMETER_PARTB_CONSOLIDATED_2026-11-12/figures/`. No manuscript source or PDF is needed.

## Fresh three-region study

```sh
python reproduce.py three-region --output-dir reruns/three-region-01
```

The driver recomputes the backup and repaired-plan certificates, runs the ensemble simulations, and writes a new `validated_results.json` alongside the detailed records. It refuses an existing output directory. Relative output paths are resolved from the repository root.

The [protocol](benchmarks/three_region_recovery_2026-11-16/PROTOCOL.md) describes the network, uncertainty bounds and fixed plans. The [study guide](docs/STUDIES.md#three-region-recovery) links the numerical implementation and stored reference evidence.

## Other numerical studies

The [study guide](docs/STUDIES.md) maps each result to its drivers, protocols and records. Several two-region drivers resume from existing case files. Running them over the published records therefore reuses those cases rather than performing a fresh experiment.

For a fresh two-region sweep, use a separate working copy, keep the published copy for comparison, and move the particular result directory being regenerated out of that working copy. Do not run the record-preparation command again before the fresh sweep, because it would restore the saved cases. Preserve the fixed `anchor.json`, which supplies the minute-20 state and backup plan.

From `benchmarks/reusable_perimeter_suite_2026-09-26/`, the main sequence is:

```sh
python -B run_regulation.py
python -B run_contracts.py --workers 2
python -B run_full_scenario.py --workers 2
python -B run_reserve_refresh.py --workers 2
python -B select_certified_tools.py
python -B run_delayed_handover.py --workers 2
```

For the two-region congested study, the fixed proposal and backup are stored in `benchmarks/congested_recovery_2026-11-10/results/`. The arrival-error extension is reproduced with `arrival_extension.py`, `queue_witnesses.py` and `consolidated_recovery.py` in `benchmarks/reviewer_strengthening_2026-11-11/`. Its main 600 veh/h case and the separate 300 veh/h sensitivity/timing cases must be evaluated under their respective settings.

Some intermediate traces are regenerated by the drivers. The included records contain the fixed inputs, aggregate outcomes and selected full certificates used to inspect the reported results. For timing comparisons, run the checks without competing numerical workers.

## Optional agent experiments

The saved prompts, responses, tool arguments and model identifiers can be inspected offline after unpacking the records. See the [agent study guide](docs/STUDIES.md#agent-experiments).

Repeating live agent experiments requires separate API credentials and incurs charges. Read the [API protocol](benchmarks/reusable_perimeter_suite_2026-09-26/API_PROTOCOL.md) and the budget controls in [`run_api.py`](benchmarks/reusable_perimeter_suite_2026-09-26/run_api.py) and [`run_end_to_end_api.py`](benchmarks/reusable_perimeter_suite_2026-09-26/run_end_to_end_api.py) before running them. The root reproduction commands never invoke these drivers. Keep credentials outside the repository.

## Units, records and versions

- Reported vehicle counts and flow rates use vehicles and veh/h. Several numerical routines internally use units of 100 vehicles and hours; their protocols specify the conversions.
- Numerical records are bundled in `data/study_records.zip`, with hashes in [`data/records_manifest.json`](data/records_manifest.json). The preparation command restores the original relative paths.
- Recorded certificates identify exact numerical inputs and source files. Keep the certificate-bound files and `source_snapshots/` unchanged when checking the published records.
- Use a fresh working copy for modified models, settings or plans, and preserve its new outputs separately from the published evidence.
- The manuscript's immutable snapshot is [release `paper-2026-11-17`](https://github.com/AlienEslami/agentic-perimeter-control-code/releases/tag/paper-2026-11-17). The live documentation and convenience commands on `main` can develop independently of that release.

If record preparation reports a mismatch, inspect the named file and keep a copy of any intentional edits before restoring the published version. An offline package audit is expected to fail after published numerical records have been replaced by fresh or modified results.
