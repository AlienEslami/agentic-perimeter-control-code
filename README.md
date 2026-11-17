# Agentic perimeter-control reproducibility code

Code and experimental records for **A Formal Guarantee for Trustworthy Agentic Traffic Control: A Multi-region Perimeter Case**, by Ali Eslami and Jiangbo Yu.

This repository contains the traffic models, MPC-based planning tools, constraint-verification and plan-repair implementations, simulation settings, and saved experimental evidence used in the manuscript. It is a curated snapshot of the research code, with a fresh repository history. Earlier manuscripts, document-editing scripts, and preparation files are excluded.

## Quick start

Use Python 3.12. From the repository root:

```text
python -m pip install -r requirements.txt
python scripts/prepare_records.py
python -B scripts/audit_repository_records.py
python -B scripts/audit_current_results_2026_11_15.py
python -B scripts/smoke_check.py
```

Saved records are compressed in `data/study_records.zip`. The setup command verifies their hashes and restores their original relative paths. It refuses to overwrite a file whose contents differ. The audits require no network access or paid model calls.

See [REPRODUCING.md](REPRODUCING.md) for the mapping between the manuscript's results, code, settings and saved records, and instructions for rerunning experiments. Dates in study-directory names identify the source experiments; they do not identify different manuscript versions.

## Organization

- `benchmarks/reusable_perimeter_suite_2026-09-26/`: two-region dynamics, planning, verification, repair, controller comparisons, successive requests, delays, and agent experiments.
- `benchmarks/reviewer_strengthening_2026-11-11/`: the reported numerical evaluation, congested recovery, timing, and model-error sensitivity.
- `benchmarks/three_region_recovery_2026-11-16/`: three-region congested recovery, source snapshots and reproduction driver.
- Other `benchmarks/` directories: coordinate comparisons, fixed-plan checks, connected-ring results, and inputs used by these studies.
- `scripts/`: record preparation, offline audits and result plotting.
- `data/`: compressed numerical records and their integrity manifest.

The models use hours and, internally in several routines, units of 100 vehicles. Reports and plots convert counts and rates to vehicles and veh/h. Study protocols specify the exact conversion and uncertainty sets.

Experimental AI-agent prompts, tool calls, model identifiers and responses are retained because they are evidence for the agent study. Repeating live API experiments is optional, requires separate credentials, and incurs charges. No credentials are included.

## Version and provenance

Use release **`paper-2026-11-17`** when citing this package. `SOURCE_MANIFEST.json` identifies the source repository, commit and original file hashes. `REPRODUCTION_MANIFEST.json` records the packaged files. [PROVENANCE.md](PROVENANCE.md) describes the packaging changes. Numerical kernels, frozen plans, protocols used in certificate hashes, and saved numerical results retain their original contents.

Certificates apply to the model and uncertainty sets specified in the manuscript. Sampled traffic simulations and perturbed-model tests have their separately stated scope. Recorded runtimes depend on hardware and load.
