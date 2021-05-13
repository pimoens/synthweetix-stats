from datetime import datetime
from enum import Enum
import logging
import requests
import tweepy

__author__ = 'Pieter Moens'
__email__ = "pieter@pietermoens.be"


class StatisticsType(Enum):
    NETWORK = 'Network'
    STAKING = 'Staking'
    TRADING = 'Trading'
    YIELD_FARMING = 'Yield Farming'


class SynthweetixBot:

    def __init__(self, key, secret, access_token, access_secret, debug=False):
        auth = tweepy.OAuthHandler(key, secret)
        auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(auth)
        self.debug = debug

    def send_statistics(self, type_: StatisticsType, message):
        message = f'\U0001F6A8 #Synthetix {type_.value} Statistics \U0001F6A8\n' \
                  f'{message}\n' \
                  f'Full stats: https://stats.synthetix.io/'

        logging.debug(message)
        if not self.debug:
            self.api.update_status(message)

    def create_tweets(self, data):
        if StatisticsType.NETWORK.name in data:
            self.create_network_tweet(data[StatisticsType.NETWORK.name])
        if StatisticsType.STAKING.name in data:
            self.create_staking_tweet(data[StatisticsType.STAKING.name])
        if StatisticsType.TRADING.name in data:
            self.create_trading_tweet(data[StatisticsType.TRADING.name])
        if StatisticsType.YIELD_FARMING.name in data:
            self.create_yieldfarming_tweet(data[StatisticsType.YIELD_FARMING.name])

    def create_network_tweet(self, stats):
        snxprice = stats['SNXPRICE']
        percentsnxchnge24h = stats['PERCENTSNXCHNGE24H'] * 100
        snxmktcap = stats['SNXMKTCAP']
        totalsnxlocked = stats['TOTALSNXLOCKED']
        percentsnxlocked = stats['PERCENTSNXLOCKED'] * 100
        activecratio = stats['ACTIVECRATIO'] * 100
        snxholdrs = stats['SNXHOLDRS']

        message = [
            '$SNX = ${:.2f} ({:+.2f}%)'.format(snxprice, percentsnxchnge24h),
            'MARKET CAP = ${:,.0f}'.format(snxmktcap),
            'STAKED = ${:,.0f} ({:.2f}%)'.format(totalsnxlocked, percentsnxlocked),
            'ACTIVE C-RATIO = {:.2f}%'.format(activecratio),
            'NUMBER OF HOLDERS = {:,.0f}'.format(snxholdrs),
        ]

        self.send_statistics(StatisticsType.NETWORK, ', '.join(message))

    def create_staking_tweet(self, stats):
        snxstakingapy = stats['SNXSTKAPY'] * 100
        snxstakingapysnx = stats['SNXSTKAPYSNX'] * 100
        crrntfeerwpoolsnx = stats['CRRNTFEERWPOOLSNX']
        unclmfeesusd = stats['UNCLMFEESUSD']
        upcomingfeesusd = stats['UPCOMINGFEESUSD']
        snxstakrs = stats['SNXSTAKRS']

        message = [
            'SNX STAKING APY = {:.2f}%'.format(snxstakingapy),
            'SNX STAKING APY (REWARDS) = {:.2f}%'.format(snxstakingapysnx),
            'REWARDS POOL = ${:,.0f}'.format(crrntfeerwpoolsnx),
            'UNCLAIMED FEES & REWARDS = ${:,.0f}'.format(unclmfeesusd),
            'UPCOMING FEES (NEXT PERIOD) = ${:,.0f}'.format(upcomingfeesusd),
            'NUMBER OF STAKERS = {:,.0f}'.format(snxstakrs)
        ]

        self.send_statistics(StatisticsType.STAKING, ', '.join(message))

    def create_trading_tweet(self, stats):
        totaltrdvolume = stats['TOTALTRDVOLUME']
        totlfees = stats['TOTLFEES']
        totlnotrdes = stats['TOTLNOTRDES']
        totdailyvolume = stats['TOTLDAILYVOLUME']
        totalnounqtraders = stats['TOTALNOUNQTRADERS']
        avgdailytrdrs = stats['AVGDAILYTRDRS']

        message = [
            'TRADING VOLUME = ${:,.0f}'.format(totaltrdvolume),
            'TRADING FEES = ${:,.0f}'.format(totlfees),
            '24H EXCHANGE VOLUME = ${:,.0f}'.format(totdailyvolume),
            'NUMBER OF TRADES = {:,.0f}'.format(totlnotrdes),
            'NUMBER OF UNIQUE TRADERS = {:,.0f}'.format(totalnounqtraders),
            'AVERAGE DAILY TRADERS = {:,.0f}'.format(avgdailytrdrs)
        ]

        self.send_statistics(StatisticsType.TRADING, ', '.join(message))

    def create_yieldfarming_tweet(self, stats):
        lndingapy = stats['LNDINGAPY'] * 100

        message = [
            'LENDING APY = {:.2f}%'.format(lndingapy),
        ]

        currency_mapping = {
            'CURVESUSDRWRDS': 'Curvepool sUSD',
            'SHORTSETHRWRDS': 'Short sETH',
            'SHORTSBTCRWRDS': 'Short sBTC'
        }
        for key, name in currency_mapping.items():
            if key in stats.keys():
                currency = stats[key]
                message.append(
                    '{}: WEEKLY REWARDS = {}, APY = {}'.format(name, currency['WEEKLYRWRDSSNX'], currency['APY'])
                )

        self.send_statistics(StatisticsType.YIELD_FARMING, '\n'.join(message))

    def execute(self, stats_endpoint):
        start = datetime.now()
        logging.info('Running SynthweetixBot')

        logging.info(f'Fetching data from Synthetix Stats at {stats_endpoint}')
        with requests.get(stats_endpoint) as resp:
            r = resp.json()

        logging.info('Sending tweets')
        self.create_tweets(r)

        end = datetime.now()
        logging.info(f'Executed SynthweetixBot in {end - start}s')