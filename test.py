import os
from phil_tweet_downloader import downloader

access_token = "put_your_access_token_here"
access_token_secret = "put_your_access_token_secret_here"
consumer_key = "put_your_consumer_key_here"
consumer_secret = "put_your_consumer_secret_here"

output_dir = os.path.join(os.getcwd(), 'output')

downloader.download_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
                           output_dir=output_dir)
