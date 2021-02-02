import time
import schedule
from dca_job_config import prepare_jobs

if __name__ == '__main__':
    prepare_jobs()
    while True:
        schedule.run_pending()
        time.sleep(1)
