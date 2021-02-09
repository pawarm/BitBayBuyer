BitBayBuyer
=
Open-source python bot to automatically buy crypto on BitBay using the DCA strategy

##General

This small app can be used to create orders to buy various cryptocurrencies on [BitBay](https://bitbay.net/pl). 

It can be configured so that orders for each currency are made at various times, every given number of days, and for different amounts. 

Please note that your bitbay account needs to have enough funds to complete the purchase.


##Requirements
For the script to work properly, it should run on a Unix system that has python3 installed. 
The requirements for additional modules are included in the requirements.txt file, and you can check them out below:
* [ccxt](https://github.com/ccxt/ccxt)
* [schedule](http://github.com/dbader/schedule)

##Installation
To install the script, download the latest version from the repository:

```git clone https://github.com/pawarm/BitBayBuyer.git```

Then enter the directory where it was downloaded:

```cd BitBayBuyer/```

Download the necessary modules (it may take some time):

```python3 -m pip install -r requirements.txt```

##Configuration
If everything went ok, you should be able to run `python3 main.py`, but you will get an error about invalid configuration.

To configure the script, edit the `config_template.json` file.
```
  "apiKey": "PUBLIC_KEY",
  "secret": "PRIVATE_KEY",
```
First two fields are api keys: public and private. They have to be obtained from your [BitBay account](https://auth.bitbay.net/settings/api).

Then under the *"pairs"* field you should write pairs of currencies you want the script to buy and for each of them give the purchase amount and the number of days every which you want to buy the currency. 

Optionally, you can add the time of purchase, if you do not specify it, the script's start time will be used.

It is best to save the file with the configuration under the name `config.json`.


##Launching
If everything has been configured, you can proceed to run the script
```
python3 main.py [-h] [-f [FILENAME]] [-v] [-c CONFIG]
    -h, --help                              Show this help message and exit
    -f [FILENAME], --filename [FILENAME]    Save log to a file
    -v, --verbose                           Increase log verbosity
    -c CONFIG, --config CONFIG              Read config from custom filename
```
###Nohup
Its best to run the script from docker, or nohup like this:
```
nohup python3 main.py &
```
Then you can check output in `nohup.out`.
