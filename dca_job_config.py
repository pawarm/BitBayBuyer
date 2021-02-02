import json
import schedule
import ccxt


class DcaJobConfig:
    def __init__(self):
        with open('config.json') as config_file:
            self.config_dict = json.load(config_file)
        self.bitbay = ccxt.bitbay({
            'apiKey': self.config_dict['apiKey'],
            'secret': self.config_dict['secret'],
        })
        self.markets = self.bitbay.load_markets()

    def buy_for_current_price(self, pair):
        current_price = self.bitbay.fetch_order_book(pair)['asks'][0][0]
        amount_to_buy_not_precise = self.config_dict['pairs'][pair]['amount'] / current_price
        amount_to_buy = ccxt.decimal_to_precision(amount_to_buy_not_precise, precision=10)
        self.bitbay.create_market_buy_order(pair, amount_to_buy)

    def prepare_jobs(self):
        for pair in self.config_dict['pairs']:
            schedule.every(self.config_dict['pairs'][pair]['days']).days.do(self.buy_for_current_price, pair)
