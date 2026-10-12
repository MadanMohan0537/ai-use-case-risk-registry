from __future__ import annotations

import argparse
import json

from .demo import run_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ControlLedger governance registry demo")
    parser.add_argument("--json", default="controlledger-report.json")
    parser.add_argument("--csv", default="controlledger-audit.csv")
    args = parser.parse_args()
    report = run_demo()
    csv_data = report.pop("csv")
    with open(args.json, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, default=list)
    with open(args.csv, "w", encoding="utf-8", newline="") as handle:
        handle.write(csv_data)
    print(json.dumps({k: v for k, v in report.items() if k not in {"portfolio", "scope_change_experiment"}}, indent=2))


if __name__ == "__main__":
    main()
