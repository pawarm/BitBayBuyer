import json
import schedule
import ccxt


class DcaJobConfig:
    def __init__(self):
        self.bitbay = ccxt.bitbay()
        self.markets = self.bitbay.load_markets()

    def print_price(self, pair):
        print(self.bitbay.market_id(pair))

    def prepare_jobs(self):
        with open('config.json',) as config_file:
            config_json = json.load(config_file)
            api = config_json['api_key']
            for pair in config_json['pairs']:
                schedule.every(5).seconds.do(self.print_price, pair['pair'])
            # for x in markets:
            #     print(f"{x}: {markets[x]}")
