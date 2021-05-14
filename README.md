# Synthweetix - Synthetix Statistics Twitter Bot

Twitter bot using tweepy to announce relevant statistics about Synthetix.

## Deployment

### Configuration

#### Environment variables

| Name                      | Description                                          | Default                                     |
| :-------------:           | :-------------:                                      | :-----:                                      |
| CONFIGURATION             | Configuration to run (`development` or `production`) | `development`                               |
| TWITTER_CONSUMER_KEY      | Twitter Consumer Key                                 | `''`                                        |
| TWITTER_CONSUMER_SECRET   | Twitter Consumer Secret                              | `''`                                        |
| TWITTER_ACCESS_TOKEN      | Twitter OAuth Access Token                           | `''`                                        |
| TWITTER_ACCESS_SECRET     | Twitter OAuth Access Secret                          | `''`                                        |
| SYNTHETIX_STATS_ENDPOINT  | API Endpoint of the Synthetix Stats application      | `https://synthetix-stats.herokuapp.com/api` |

### Heroku

Application is deployed on [Heroku](https://heroku.com) using a CronJob

```
clock: python main.py
```

**Note:** Scale up the process when deploying for the first time using the Heroki CLI

```
heroku ps:scale clock=1
```