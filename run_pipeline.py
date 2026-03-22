import argparse
from pprint import pprint

from autminietl.config import SETTINGS
from autminietl.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AutMiniETL once")
    parser.add_argument(
        "--source",
        choices=["mock", "api", "scrape"],
        default=SETTINGS.default_source,
        help="Data source",
    )
    args = parser.parse_args()
    result = run_pipeline(args.source)
    pprint(result)


if __name__ == "__main__":
    main()
