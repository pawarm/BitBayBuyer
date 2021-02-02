import time
import schedule
from dca_job_config import DcaJobConfig

if __name__ == '__main__':
    job_config = DcaJobConfig()
    job_config.prepare_jobs()
    while True:
        schedule.run_pending()
        time.sleep(1)
