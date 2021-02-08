import json
import schedule
import ccxt
import logging
import time
import re
from ccxt.base.errors import RequestTimeout
from datetime import datetime


class DcaJobConfig:
    def __init__(self, config_filename="config.json"):
        logging.debug("Getting config from file...")
        with open(config_filename) as config_file:
            self.config_dict = json.load(config_file)
        logging.debug("Verifying config...")
        self.verify_config()
        logging.debug("Creating bitbay instance...")
        self.bitbay = ccxt.bitbay({
            'enableRateLimit': True,
            'apiKey': self.config_dict['apiKey'],
            'secret': self.config_dict['secret'],
        })
        logging.debug("Loading available markets...")
        self.markets = self.bitbay.load_markets()

    def verify_config(self):
        if self.config_dict.get("apiKey", "PUBLIC_KEY") == "PUBLIC_KEY":
            logging.error("apiKey is not properly set in config file!")
            exit()
        if self.config_dict.get("secret", "PRIVATE_KEY") == "PRIVATE_KEY":
            logging.error("secret is not properly set in config file!")
            exit()
        if "pairs" not in self.config_dict \
                or not isinstance(self.config_dict['pairs'], dict) \
                or not self.config_dict['pairs']:
            logging.error("pairs are not properly set in config file!")
            exit()
        for pair in self.config_dict['pairs']:
            if not re.match(r"\w{3,4}/\w{3}", pair):
                logging.error("pairs must be written as \"QUOTE_CURRENCY/BASE_CURRENCY\" eg. BTC/PLN")
                exit()
            if 'days' not in self.config_dict['pairs'][pair] \
                    or not isinstance(self.config_dict['pairs'][pair]['days'], int) \
                    or self.config_dict['pairs'][pair]['days'] < 1:
                logging.error(f"Pair {pair} does not have properly set \"days\" field.")
                exit()
            if 'amount' not in self.config_dict['pairs'][pair] \
                    or type(self.config_dict['pairs'][pair]['amount']) not in (int, float):
                logging.error(f"Pair {pair} does not have properly set \"amount\" field.")
                exit()
            if 'at' in self.config_dict['pairs'][pair] \
                    and not re.match(r"\d\d:\d\d", self.config_dict['pairs'][pair]['at']):
                logging.error(f"Pair {pair} has improperly set \"at\" field.")
                exit()

    def buy_for_current_price(self, pair):
        logging.debug(f"Ordering {pair}:")
        current_price = self.bitbay.fetch_order_book(pair)['asks'][0][0]
        logging.debug(f"Current price: {current_price}")
        amount_to_buy_not_precise = self.config_dict['pairs'][pair]['amount'] / current_price
        precision = self.markets[pair]['precision']['amount']
        amount_to_buy = ccxt.decimal_to_precision(amount_to_buy_not_precise, precision=precision)
        logging.debug(f"Amount to buy: {amount_to_buy}")
        base = self.markets[pair]['base']
        quote = self.markets[pair]['quote']
        retries = 3
        for r in range(retries):
            try:
                self.bitbay.create_market_buy_order(pair, amount_to_buy)
                logging.info(f"Order created to buy {amount_to_buy} {base} at price {current_price}{quote}")
                break
            except RequestTimeout as e:
                logging.exception(f"Exception occurred: {e}")
                if r != retries - 1:
                    logging.info(f"Waiting a few seconds and retrying: {r}/{retries}")
                    time.sleep(3)
                else:
                    logging.warning("Order not created")

    def prepare_jobs(self):
        logging.info("Scheduling jobs:")
        for pair in self.config_dict['pairs']:
            base = self.markets[pair]['base']
            quote = self.markets[pair]['quote']
            amount = self.config_dict['pairs'][pair]['amount']
            days = self.config_dict['pairs'][pair]['days']
            if 'at' in self.config_dict['pairs'][pair]:
                at = self.config_dict['pairs'][pair]['at']
            else:
                at = datetime.strftime(datetime.now(), '%H:%M')
            logging.info(f"Will buy {base} for {amount}{quote} every {days} days at {at}.")
            schedule.every(days).days.at(at).do(self.buy_for_current_price, pair)
