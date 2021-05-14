from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import os

from bot import SynthweetixBot
from config import ConfigType, ConfigFactory


if __name__ == '__main__':
    # Configuration
    app_settings = os.getenv('CONFIGURATION ', default='deployment')
    print(app_settings)
    type_ = ConfigType.reverse_lookup(app_settings)
    cfactory = ConfigFactory()
    config = cfactory.get(type_)

    # Logging
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=config.LOG_LEVEL)

    logging.info(f'Initializing Synthweetix in {app_settings} environment')
    bot = SynthweetixBot(config.TWITTER_CONSUMER_KEY,
                         config.TWITTER_CONSUMER_SECRET,
                         config.TWITTER_ACCESS_TOKEN,
                         config.TWITTER_ACCESS_SECRET)

    # Run once on startup
    bot.execute(config.SYNTHETIX_STATS_ENDPOINT)

    # Run the bot periodically
    scheduler = BlockingScheduler()
    scheduler.add_job(bot.execute, config.TRIGGER,
                      args=[config.SYNTHETIX_STATS_ENDPOINT])

    scheduler.start()
