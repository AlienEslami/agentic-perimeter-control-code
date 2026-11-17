# Guide to the studies

[Repository home](../README.md) · [Reproduction commands](../REPRODUCING.md)

This guide connects the traffic questions to their code, settings and saved evidence. Run `python reproduce.py prepare` before opening numerical records locally. Records listed below are restored from [`data/study_records.zip`](../data/); the linked source files and protocols can be read directly on GitHub.

## Two-region recovery

**Question:** Can a proposed congestion-recovery plan be modified to respect entry-queue storage and a regional service deadline under uncertainty?

- **Code:** [baseline model and plans](../benchmarks/congested_recovery_2026-11-10/run_study.py), [arrival-error extension](../benchmarks/reviewer_strengthening_2026-11-11/arrival_extension.py), [combined recovery results](../benchmarks/reviewer_strengthening_2026-11-11/consolidated_recovery.py), [queue-violation calculations](../benchmarks/reviewer_strengthening_2026-11-11/queue_witnesses.py).
- **Records after unpacking:** `benchmarks/reviewer_strengthening_2026-11-11/arrival_extension_protocol.json`, `full_certificates/`, `consolidated_recovery/` and `queue_witnesses_w600.json` in that same study directory.
- **Figure:** `python reproduce.py figures` produces `output/figures/two-region-recovery.pdf` and `.png`.

The main recovery experiment uses an arrival-error bound of 600 veh/h. The 300 veh/h timing and model-perturbation studies use different plans and uncertainty specifications.

## Three-region recovery

**Question:** Can the same verification and repair construction handle three connected regions with separate entry queues?

- **Settings:** [study protocol](../benchmarks/three_region_recovery_2026-11-16/PROTOCOL.md).
- **Code:** [model and verification](../benchmarks/three_region_recovery_2026-11-16/study.py), [simulation evaluation](../benchmarks/three_region_recovery_2026-11-16/evaluate.py), [fresh-run driver](../benchmarks/three_region_recovery_2026-11-16/reproduce.py).
- **Records after unpacking:** `benchmarks/three_region_recovery_2026-11-16/results/validated_results.json`, the proposed/repaired/backup `*_ensemble.npz` files, and the stored `*_proof.json.gz` certificates.
- **Figure:** `python reproduce.py figures` produces `output/figures/three-region-recovery.pdf` and `.png`, showing all three regions and all three queues.
- **Fresh run:** `python reproduce.py three-region --output-dir reruns/three-region-01`.

## Regional priorities and controller comparisons

**Question:** How do proposed and repaired plans trade regional priority against total time spent, queue storage and the service deadline?

- **Settings:** [contract grid](../benchmarks/reusable_perimeter_suite_2026-09-26/PROTOCOL.md) and [scenario-based planning](../benchmarks/reusable_perimeter_suite_2026-09-26/FULL_SCENARIO_PROTOCOL.md).
- **Code:** [contracts and repair](../benchmarks/reusable_perimeter_suite_2026-09-26/run_contracts.py), [scenario-based planning](../benchmarks/reusable_perimeter_suite_2026-09-26/run_full_scenario.py), [matched CBF-QP simulations](../scripts/run_partb_matched_cbf_2026_11_15.py).
- **Records after unpacking:** `benchmarks/reusable_perimeter_suite_2026-09-26/results/contracts/D027.json` and `D063.json` contain the 1- and 25-vehicle state-error cases. `benchmarks/partb_traffic_presentation_2026-11-15/` contains `matched_controller_table.json`, `cbf_ensemble.json` and `repair_traffic_statistics.json`.

The matched comparison uses 640 simulations per plan. The CBF-QP benchmark does not enforce the fixed service deadline in its formulation. A verification check that does not pass may be inconclusive; a simulated violation and an inconclusive check are different outcomes.

## Coordinates and uncertainty

**Question:** How do the state coordinates, shared uncertainty and numerical bounds affect which plans can be verified?

- **Code:** [coordinate comparison](../benchmarks/manuscript_review_2026-11-08/run_checks.py), [verification comparison](../benchmarks/reviewer_strengthening_2026-11-11/run_comparison.py), [subdivision bounds](../benchmarks/reviewer_strengthening_2026-11-11/four_box_bounds.py), [timing](../benchmarks/reviewer_strengthening_2026-11-11/timing.py).
- **Records after unpacking:** `benchmarks/manuscript_review_2026-11-08/results/coordinate_comparison.json`; `benchmarks/fixed_portfolio_2026-11-10/`; and `decision_summary.json`, `four_box_bound_summary.json`, `timing_summary.json` in `benchmarks/reviewer_strengthening_2026-11-11/`.

Several code identifiers predate the manuscript terminology:

| Identifier in code or records | Meaning |
|---|---|
| `class_box` / `class` | Destination-specific vehicle-count coordinates |
| `inventory` | Conservation coordinates combining regional counts and allocated queue shares |
| `affine` | Signed-generator bounds retaining shared uncertainty dependence |
| `continuation` | Remaining schedule of the current plan in the controller comparison |
| `grid_repair` | Repaired plan selected from the tested interpolation weights |

The source identifiers are retained so the saved records remain directly readable by their original numerical routines.

## Successive requests and delayed implementation

**Question:** When can a new plan replace the current plan while respecting pending requirements and traffic evolution during computation?

- **Settings:** [successive-request protocol](../benchmarks/reusable_perimeter_suite_2026-09-26/SEQUENTIAL_AUTHORITY_PROTOCOL.md), [delayed-implementation protocol](../benchmarks/reusable_perimeter_suite_2026-09-26/DELAYED_PROTOCOL.md).
- **Code:** [successive requests](../benchmarks/reusable_perimeter_suite_2026-09-26/run_sequential_authority.py), [delayed implementation](../benchmarks/reusable_perimeter_suite_2026-09-26/run_delayed_handover.py).
- **Records after unpacking:** `benchmarks/reusable_perimeter_suite_2026-09-26/results/sequential_authority_2026-10-01/` and `results/delayed_handover/`.

## Agent experiments

**Question:** How do instruction interpretation and a structured task record affect planning requests and verified execution?

- **Settings:** [API protocol and budgets](../benchmarks/reusable_perimeter_suite_2026-09-26/API_PROTOCOL.md).
- **Code:** [end-to-end agent study](../benchmarks/reusable_perimeter_suite_2026-09-26/run_end_to_end_api.py), [interpretation study](../benchmarks/reusable_perimeter_suite_2026-09-26/run_api.py).
- **Records after unpacking:** `benchmarks/reusable_perimeter_suite_2026-09-26/results/end_to_end_api/` and `results/api/`, including the eight end-to-end traces and the 96-query interpretation study.

The stored prompts and responses can be inspected offline. Live calls are optional and are not invoked by the root reproduction commands.

## Additional studies

| Study | Code | Records after unpacking |
|---|---|---|
| Network efficiency with a CLF benchmark | [regulation driver](../benchmarks/reusable_perimeter_suite_2026-09-26/run_regulation.py) | Portable suite `results/regulation/` |
| MFD and internal-demand perturbations | [plant sensitivity](../benchmarks/reviewer_strengthening_2026-11-11/plant_sensitivity.py) | Same directory: `plant_sensitivity_protocol.json` and `plant_sensitivity.json` |
| Connected-ring verification | [network driver](../benchmarks/connected_network_2026-09-11/reproducibility/mfd_multiregion_transfer.py) | Same directory: `results/`, including compressed proof records |

The plant-perturbation study changes model quantities held fixed by the certificates. It measures sensitivity outside the certified model. The recorded checking times are measurements on the reported hardware, not worst-case latency bounds.
