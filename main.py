import time
import schedule
import logging
import argparse
from dca_job_config import DcaJobConfig

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", nargs='?', const="BitBayBuyer.log", help="Save log to a file")
parser.add_argument("-v", "--verbose", action="store_true", help="Increase log verbosity")
parser.add_argument("-c", "--config", help="Read config from custom file")
args = parser.parse_args()

if args.verbose:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO
log_format = '%(levelname)s\t%(asctime)s %(message)s'
date_format = '%d/%m/%Y %H:%M:%S'
if args.filename:
    logging.basicConfig(
        filename=args.filename,
        format=log_format,
        datefmt=date_format,
        level=loglevel)
else:
    logging.basicConfig(
        format=log_format,
        datefmt=date_format,
        level=loglevel)

if __name__ == '__main__':
    logging.info("")
    logging.info("BitBayBuyer is starting...")
    if args.config:
        dca_job_config = DcaJobConfig(args.config)
    else:
        dca_job_config = DcaJobConfig()
    dca_job_config.prepare_jobs()
    while True:
        schedule.run_pending()
        time.sleep(1)
