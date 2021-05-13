from datetime import timedelta
from enum import Enum
import logging
import os


__author__ = 'Pieter Moens'
__email__ = "pieter@pietermoens.be"


class BaseConfig:
    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY', default='')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET', default='')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', default='')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', default='')

    SYNTHETIX_STATS_ENDPOINT = os.getenv('SYNTHETIX_STATS_ENDPOINT', default='https://stats.synthetix.io/api')


class DevelopmentConfig(BaseConfig):
    LOG_LEVEL = logging.DEBUG
    INTERVAL = timedelta(minutes=1).total_seconds()


class ProductionConfig(BaseConfig):
    LOG_LEVEL = logging.INFO
    INTERVAL = timedelta(hours=24).total_seconds()


class ConfigType(Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'

    @classmethod
    def reverse_lookup(cls, value):
        """Reverse lookup."""
        for _, member in cls.__members__.items():
            if member.value == value:
                return member
        raise LookupError


class ConfigFactory:
    _configs = {
        ConfigType.DEVELOPMENT: DevelopmentConfig,
        ConfigType.PRODUCTION: ProductionConfig
    }
    current = None

    def get(self, type_: ConfigType):
        cls = self._configs[type_]
        self.current = cls()
        return self.current
