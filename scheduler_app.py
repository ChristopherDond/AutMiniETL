import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from autminietl.config import SETTINGS
from autminietl.pipeline import run_pipeline


def scheduled_job() -> None:
    logging.getLogger("autminietl.scheduler").info("Triggered scheduled ETL run")
    run_pipeline(SETTINGS.default_source)


def main() -> None:
    scheduler = BlockingScheduler(timezone=SETTINGS.timezone)
    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        minutes=SETTINGS.schedule_minutes,
        id="autminietl_job",
        replace_existing=True,
    )

    logging.getLogger("autminietl.scheduler").info(
        "Starting scheduler each %s minutes with source=%s",
        SETTINGS.schedule_minutes,
        SETTINGS.default_source,
    )
    scheduler.start()


if __name__ == "__main__":
    main()
