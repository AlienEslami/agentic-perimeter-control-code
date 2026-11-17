# Reproducing the manuscript results

First follow the root README to install dependencies and restore the compressed records. Commands below run from the repository root unless a study directory is specified. Saved results contain the exact floating-point plans, initial states, uncertainty bounds and verification outcomes. Historical identifiers such as `class_box`, `inventory`, and `affine` correspond to destination coordinates, conservation coordinates and signed-generator bounds, respectively; they are retained in code and records.

## Result-to-code map

| Result in the manuscript | Code and settings | Saved evidence |
|---|---|---|
| Two-region congested recovery, including the 600 veh/h arrival-error case | `benchmarks/congested_recovery_2026-11-10/run_study.py`; `benchmarks/reviewer_strengthening_2026-11-11/arrival_extension.py`, `consolidated_recovery.py`, `queue_witnesses.py` | In the latter directory: `arrival_extension_protocol.json`, `full_certificates/`, `consolidated_recovery/`, `queue_witnesses_w600.json` |
| Three-region congested recovery | `benchmarks/three_region_recovery_2026-11-16/reproduce.py`, `study.py`, `refined.py`, `PROTOCOL.md` | Its `results/` and certificate-bound `source_snapshots/` |
| Regional-priority controller comparison, 640 simulations per plan | Portable suite `run_contracts.py`, `run_full_scenario.py`; `scripts/run_partb_matched_cbf_2026_11_15.py` | Portable suite `results/contracts/D027.json`; `benchmarks/partb_traffic_presentation_2026-11-15/matched_controller_table.json`, `cbf_ensemble.json` |
| Regional state-estimation bounds of 1 and 25 vehicles | Portable suite `run_contracts.py`, `PROTOCOL.md` | `results/contracts/D027.json` and `D063.json` |
| Traffic cost of repair across the contracts | Portable suite `run_contracts.py` | Per-case `results/contracts/`; `benchmarks/partb_traffic_presentation_2026-11-15/repair_traffic_statistics.json` |
| Coordinate and uncertainty comparisons | `benchmarks/manuscript_review_2026-11-08/run_checks.py`, `coordinate_fixture.json` | Its `results/coordinate_comparison.json` and individual coordinate certificates |
| Fixed verification portfolio and numerical evaluation | `benchmarks/reviewer_strengthening_2026-11-11/run_comparison.py`, `probe.py`, `four_box_bounds.py`, `timing.py` | `benchmarks/fixed_portfolio_2026-11-10/`; refined `decision_summary.json`, `four_box_bound_summary.json`, `timing_summary.json` |
| Successive requests and delayed implementation | Portable suite `run_sequential_authority.py`, `run_delayed_handover.py`, their protocols | `results/sequential_authority_2026-10-01/`, `results/delayed_handover/` |
| Eight live agent traces and 96-query interpretation study | Portable suite `run_end_to_end_api.py`, `run_api.py`, `API_PROTOCOL.md` | `results/end_to_end_api/`, `results/api/` and support summaries |
| Network-efficiency comparison with the CLF controller | Portable suite `run_regulation.py` | `results/regulation/` |
| MFD/internal-demand perturbations | `benchmarks/reviewer_strengthening_2026-11-11/plant_sensitivity.py`, `plant_sensitivity_protocol.json` | `plant_sensitivity.json` |
| Supporting connected-ring checks | `benchmarks/connected_network_2026-09-11/reproducibility/mfd_multiregion_transfer.py` | Its `results/`, including compressed proof records |

The portable suite is `benchmarks/reusable_perimeter_suite_2026-09-26/`. `benchmarks/section5_support_2026-11-11/summaries/` and the restored `output/review/` JSON/CSV files provide the corresponding aggregate evidence and source hashes. These are numerical records, not manuscript files.

## Offline checks and plotting

```text
python -B scripts/audit_repository_records.py
python -B scripts/audit_current_results_2026_11_15.py
python -B scripts/smoke_check.py
python -B scripts/plot_recovery_compact_2026_11_16.py
python -B benchmarks/three_region_recovery_2026-11-16/plot_all_queues.py
python -B scripts/reproduce_current_figures_2026_11_15.py
```

The first audit checks packaged-file hashes and the binding between stored certificate descriptors, exact control inputs and source files. The second recomputes reported aggregate results from saved simulation records. The smoke check evaluates model and derivative consistency, replays one stored adverse trajectory independently, and tests the interval arithmetic used by the refined implementation.

Plotting writes under `output/`. It reconstructs numerical figures from records and does not require the manuscript. Conceptual network and architecture illustrations are outside this code package.

## Fresh numerical runs

Three-region recovery writes to a new directory and preserves the archived evidence:

```text
python -B benchmarks/three_region_recovery_2026-11-16/reproduce.py --output-dir reruns/three_region_recovery
```

For a fresh complete two-region run, use a separate extraction of this repository, install dependencies and restore records. The portable-suite drivers reuse existing case files, so retain the published copy for comparison and use a working copy without the particular result directory being regenerated. The fixed `anchor.json` supplies the minute-20 state and backup plan; it does not require an external author archive.

From the portable-suite directory, the main order is:

```text
python -B run_regulation.py
python -B run_contracts.py --workers 2
python -B run_full_scenario.py --workers 2
python -B run_reserve_refresh.py --workers 2
python -B select_certified_tools.py
python -B run_delayed_handover.py --workers 2
```

The congested-study drivers use the frozen proposal and backup in `benchmarks/congested_recovery_2026-11-10/results/`. Run `arrival_extension.py`, `queue_witnesses.py` and `consolidated_recovery.py` in the refinement directory for its published arrival-error extension. The 300 veh/h sensitivity/timing study and 600 veh/h main recovery study use distinct contracts. Their records must not be pooled.

Some complete intermediate traces are regenerated by the drivers rather than distributed. The frozen inputs, aggregate outcomes and selected full certificates needed to inspect the reported claims are included. Timing should be measured without other numerical workers; recorded timing values are not guaranteed latencies.

## Optional agent calls

Offline audits and simulation do not call a language-model API. The saved prompts, responses, tool arguments, model identifier and budget records permit inspection of every reported agent decision. To repeat the live experiments, consult `API_PROTOCOL.md` and the explicit budget controls in the two API drivers. Repeating calls requires a separately supplied API credential and incurs charges. Never commit credentials.
