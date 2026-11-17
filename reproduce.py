"""Run the published checks and recovery plots from one entry point."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
THREE = "benchmarks/three_region_recovery_2026-11-16"


def run(relative, *arguments):
    print(f"\nRunning {relative}", flush=True)
    subprocess.run(
        [sys.executable, "-B", str(ROOT / relative), *map(str, arguments)],
        cwd=ROOT,
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    tasks = parser.add_subparsers(dest="task", required=True)
    tasks.add_parser("prepare", help="Verify and unpack the saved records")
    tasks.add_parser("check", help="Run offline integrity and numerical checks")
    tasks.add_parser("figures", help="Recreate the two recovery figures from records")
    fresh = tasks.add_parser("three-region", help="Run fresh three-region verification and simulations")
    fresh.add_argument("--output-dir", type=Path, default=Path("reruns/three_region_recovery"),
                       help="A new output directory, relative to the repository by default")
    args = parser.parse_args()

    if args.task == "three-region":
        destination = (ROOT / args.output_dir).resolve()
        if destination.exists():
            parser.error(f"Output already exists: {destination}. Choose a new directory.")

    run("scripts/prepare_records.py")
    if args.task == "check":
        for script in ("audit_repository_records.py", "audit_current_results_2026_11_15.py", "smoke_check.py"):
            run("scripts/" + script)
        print("\nAll offline checks passed.", flush=True)
    elif args.task == "figures":
        run("scripts/plot_recovery_compact_2026_11_16.py")
        run(THREE + "/plot_all_queues.py")
        output = ROOT / "output/figures"
        output.mkdir(parents=True, exist_ok=True)
        sources = {
            "two-region-recovery.pdf": "output/package/PERIMETER_PARTB_CONSOLIDATED_2026-11-12/figures/congested_recovery_compact_2026_11_16.pdf",
            "two-region-recovery.png": "output/review/simulation_figure_trim_2026_11_16/congested_recovery_compact_2026_11_16.png",
            "three-region-recovery.pdf": "output/review/three_region_paper_2026_11_16/three_region_recovery_all_queues.pdf",
            "three-region-recovery.png": "output/review/three_region_paper_2026_11_16/three_region_recovery_all_queues.png",
        }
        for name, relative in sources.items():
            shutil.copyfile(ROOT / relative, output / name)
        print(f"\nFigures saved to {output}", flush=True)
    elif args.task == "three-region":
        run(THREE + "/reproduce.py", "--output-dir", destination)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from None
