# phil_tweet_downloader

A simple python module for downloading tweets within the Philippines

Need to download tweets for NLP and machine learning? phil_tweet_downloader
allows access to [Twitter's streaming API](https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data)
through [Tweepy](https://www.tweepy.org/) without the hassle of writting a bunch of codes.

## Quick Start

Just create your own Twitter app (here's a [tutorial](https://docs.inboundnow.com/guide/create-twitter-application/)) to obtain your access tokens. Open `test.py` and paste in the access tokens. Save and run the file on the terminal.

```python
import os
from phil_tweet_downloader import downloader

access_token = "put_your_access_token_here"
access_token_secret = "put_your_access_token_secret_here"
consumer_key = "put_your_consumer_key_here"
consumer_secret = "put_your_consumer_secret_here"

output_dir = os.path.join(os.getcwd(), 'output')

downloader.download_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
                           output_dir=output_dir)

```

The downloaded tweets will be saved as json files in the `output` folder 
(Note: create the output folder manually if it is missing).
You can specify the size of the json files using `fileSizeLimit`. 
By default, each json file will be around 250mb in size.

```python
downloader.download_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
                           output_dir=output_dir, fileSizeLimit=250000000)
```

By default, this module will download tweets sent within the Philippines. However, you can specify
any location you want by providing a list representing a bounding box in the following format:
`[west_long, south_lat, east_long, north_lat]` to `location`.

```python
downloader.download_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
                           output_dir=output_dir, locations=[116.702882, 5.621718, 129.387207, 21.933351])
```

You can also specify specific keywords to search using the `track` keyword.

```python
downloader.download_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
                           output_dir=output_dir, track=['baguio'])
```

Or you can keep track of specific users using the `follow` keyword.

## Requirement

This requires the [Tweepy](https://www.tweepy.org/) library to work.

```
pip install tweepy
```

## Recommendation

If you're planning to download a large number of tweets for a long time, I recommend setting up
a linux cloud server using AWS EC2, Google Cloud or Azure. Install python and then run the provided
`test.py` script on a screen multiplexer like `tmux`. This will allow you to disconnect the terminal
without halting the execution of the script. Let it download tweets for some time, then use Filezilla
to retrieve the json files.
