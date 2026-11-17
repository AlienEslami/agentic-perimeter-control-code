NUMERICAL EVALUATION AND CONGESTED RECOVERY

The published implementation uses the tight12 variant in probe.py: parity-aware interval powers, verified matrix-function series of order 12, interval products with outward rounding, and trial-radius inflation of 1% with at most 64 attempts. The underlying traffic model and acceptance conditions are unchanged. The archived baseline remains available for the comparison in Appendix C.

The full-hour 600 veh/h arrival-error case uses regional component error bounds of 25 vehicles, a queue error bound of 10 vehicles, and repair weight 0.65. Its frozen plans, full certificates, 640 simulations per plan and exact queue witnesses are included. The 300 veh/h numerical-width, timing and model-error study uses repair weight 0.35 and a distinct contract.

See ../../REPRODUCING.md for the result map and commands. The source and exact protocols for fresh runs are included. Complete intermediate comparison traces can be regenerated from protocol_final.json and run_comparison.py; aggregate decisions and selected full certificates are distributed. No live language-model call is required for these calculations.
