import subprocess

from prefect import task, flow
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from prefect.server.schemas.schedules import CronSchedule

# GITHUB BLOCKS
radar_github_block = GitHub.load("prefect-radar")


@task
def install_radar_required_package():
    subprocess.run(["pip", "install", "-r", "requirements_prefect_radar.txt"])


@flow(log_prints=True)
def radar_scraping_flow():
    install_radar_required_package()
    from process_layer.radar.execute import execute_radar
    execute_radar()


deployments = [
    Deployment.build_from_flow(
        flow=radar_scraping_flow,
        name="radar_scraping_deployment",
        storage=radar_github_block,
        # schedule=(CronSchedule(cron="* * * * *", timezone="UTC"))
    ),
]


def main():
    for deployment in deployments:
        deployment.apply()


if __name__ == "__main__":
    main()
