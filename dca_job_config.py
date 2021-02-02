import json
import schedule


def prepare_jobs():
    with open('config.json',) as config_file:
        config_json = json.load(config_file)
        api = config_json['api_key']
        for pair in config_json['pairs']:
            schedule.every(pair['days']).days.do(print, "TEST")
