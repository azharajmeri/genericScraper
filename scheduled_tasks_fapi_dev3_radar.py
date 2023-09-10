from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
import subprocess


@task
def install_required_package():
    subprocess.run(["pip", "install", "-r", "requirements_fapi_dev3_radar.txt"])


@flow(log_prints=True)
def radar_scraping_flow():
    install_required_package()
    from process_layer.radar.execute import execute_radar
    execute_radar()

#    import threading
#
#    from process_layer.edi_radar_seo_iapi_db_insert_update2 import radar_process
#    from process_layer.edi_scrapping_websites import scrapping_process
#    from utils.functions import initialize_driver
#    threads = []
#    th = threading.Thread(target=radar_process, args=(initialize_driver(),))
#    th.start()
#    threads.append(th)
#    time.sleep(60)
#    th2 = threading.Thread(target=scrapping_process, args=(initialize_driver(),))
#    th2.start()
#    threads.append(th2)
#    for th in threads:
#        th.join()


# Change the GITHUB BLOCK name below
github_block = GitHub.load("temp-radar")

deployments = [
    Deployment.build_from_flow(
        flow=radar_scraping_flow,
        name="radar_scraping_deployment",
        storage=github_block,
    ),
]


def main():
    for deployment in deployments:
        deployment.apply()


if __name__ == "__main__":
    main()
