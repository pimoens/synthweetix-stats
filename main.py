import logging
import os
import threading

from app import app
from bot import SynthweetixBot
from config import ConfigType, ConfigFactory


if __name__ == '__main__':
    # Configuration
    app_settings = os.getenv('CONFIGURATION ')
    if app_settings is not None:
        type_ = ConfigType.reverse_lookup(app_settings)
    else:
        type_ = ConfigType.DEVELOPMENT
    cfactory = ConfigFactory()
    config = cfactory.get(type_)

    # Logging
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=config.LOG_LEVEL)

    bot = SynthweetixBot(config.TWITTER_CONSUMER_KEY,
                         config.TWITTER_CONSUMER_SECRET,
                         config.TWITTER_ACCESS_TOKEN,
                         config.TWITTER_ACCESS_SECRET)

    # Run the bot
    threading.Timer(config.INTERVAL, bot.execute, args=(config.SYNTHETIX_STATS_ENDPOINT,)).start()
    bot.execute(config.SYNTHETIX_STATS_ENDPOINT)

    app.run(host='0.0.0.0')
