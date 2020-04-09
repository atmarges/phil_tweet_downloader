# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import time
import datetime
import os


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    myPath = ""
    outJson = ""
    fileCount = 1
    fileSize = 0
    startCount = 1
    current_hour = datetime.datetime.now().time().hour

    def __init__(self, output_dir, useInterval=None, fileSizeLimit=250000000,
                 text_only=False, logfile='logfile.txt', startCount=1,
                 customFunction=lambda a: a):
        # self.myPath = os.getcwd() + "\\tweets"
        self.myPath = output_dir
        self.startCount = startCount
        self.fileSizeLimit = fileSizeLimit
        self.logfile = logfile
        self.useInterval = useInterval

        if text_only:
            self.customFunction = self.get_text_only
        else:
            self.customFunction = customFunction

        # self.fileCount = len(os.listdir(self.myPath)) + self.startCount
        self.fileCount = self.startCount
        self.get_outJson()

        if len(os.listdir(self.myPath)) == 0:
            self.fileSize = 0
        else:
            self.fileSize = os.path.getsize(
                os.path.join(self.myPath, self.outJson))

        print("Downloder running!")

    def on_data(self, data):
        self.get_tweet(data)

    def on_error(self, status):
        print(status)
        return True

    def get_outJson(self, data=None):

        if self.useInterval:
            try:
                json_data = json.loads(data)
                timestamp = json_data['created_at']

            except:
                timestamp = datetime.datetime.now()
                timestamp = timestamp.strftime('%a %b %d %H:%M:%S +0000 %Y')

            # Replace timestamp based on interval
            if self.useInterval == 'minute':
                timestamp = ''.join((timestamp[:17], '00', timestamp[19:]))
            elif self.useInterval == 'hour':
                timestamp = ''.join((timestamp[:14], '00:00', timestamp[19:]))
            elif self.useInterval == 'day':
                timestamp = ''.join(
                    (timestamp[:11], '00:00:00', timestamp[19:]))
            elif self.useInterval == 'month':
                timestamp = ''.join(
                    (timestamp[:8], '00 00:00:00', timestamp[19:]))
            elif self.useInterval == 'year':
                timestamp = ''.join((timestamp[:0], 'Day', timestamp[3:]))
                timestamp = ''.join(
                    (timestamp[:8], '00 00:00:00', timestamp[19:]))

            # Replace symbols
            timestamp = timestamp.replace(':', ';')
            timestamp = timestamp.replace('+', '-')
            timestamp = timestamp.replace(' ', '_')

            self.outJson = timestamp + '.json'
        else:
            self.outJson = "tweet" + str(self.fileCount) + ".json"

    def get_tweet(self, data):

        self.get_outJson(data)

        if self.useInterval:
            create_file_condition = self.current_hour == datetime.datetime.now().time().hour

        else:
            create_file_condition = self.fileSize <= self.fileSizeLimit

        if create_file_condition:

            try:
                with open(os.path.join(self.myPath, self.outJson), 'ab') as f:
                    data = self.customFunction(data)
                    f.write(data.encode('utf-8'))
                    self.fileSize = os.path.getsize(
                        os.path.join(self.myPath, self.outJson))
                    return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                time.sleep(5)
            return True

        else:
            self.current_hour = datetime.datetime.now().time().hour
            self.fileCount = self.fileCount + 1

            try:
                open(os.path.join(self.myPath, self.outJson), 'a')
            except BaseException as e:
                print("Error on_data: %s" % str(e))

            self.fileSize = os.path.getsize(
                os.path.join(self.myPath, self.outJson))
            print("Creating file #" + str(self.fileCount))

            try:
                with open(self.logfile, 'a') as f:
                    f.write("Created " + self.outJson + " at " + str(time.strftime(
                        "%I:%M:%S") + " - " + str(time.strftime("%d/%m/%Y")) + "\n"))
                    # print(self.fileSize)
            except BaseException as e:
                print("Error on_data: %s" % str(e))

    def get_text_only(self, data):
        data = json.loads(data)

        if not data['in_reply_to_status_id']:
            try:
                data = data['extended_tweet']['full_text']
            except:
                data = data['text']

        for i in ['\t', '\r', '\n', '\f']:
            data = data.replace(i, ' ')

        data = data.strip()
        data = data + '\n'

        return data


def download_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
                    output_dir, startCount=1,
                    locations=[116.702882, 5.621718, 129.387207, 21.933351],
                    follow=None, track=None,
                    fileSizeLimit=250000000, logfile='logfile.txt', *args, **kwargs):
    """Download tweets from Twitter API and save to .json files of specified size

    Arguments:
        consumer_key {str} -- the consumer_key access token obtained from Twitter app
        consumer_secret {str} -- consumer_secret access token obtained from Twitter app
        access_token {str} -- access_token obtrained from Twitter app
        access_token_secret {str} -- access_token_secret obtained from Twitter app
        output_dir {str} -- directory of the output .json files containing tweets

    Keyword Arguments:
        useInterval {str} -- Create a new file every hour. Intervals include ['minute', 'hour', 'day', 'month', 'year']. The filename will be the timestamp of the tweet.
        startCount {int} -- the starting number of the output json file. Use this for continuation when previous files were removed. (default: {1})
        locations {list of size 4} -- the coordinates of the location bounding box. Values represents [west_long, south_lat, east_long, north_lat]. Default is Philippine area (default: {[116.702882, 5.621718, 129.387207, 21.933351]})
        follow {int} -- A comma separated list of user IDs, indicating the users to return statuses for in the stream. (default: {None})
        track {int} -- Keywords to track. Phrases of keywords are specified by a comma-separated list. See track for more information. (default: {None})
        fileSizeLimit {int} -- the estimated size of each output .json file in bytes (default: {250000000})
        logfile {str} -- the log file (default: {'logfile.txt'})
        customFunction {function} -- Use to customize the retrieved data from the API. This accepts a function with a single parameter for data.
        text_only {boolean} -- Set to True if you want the output to only contain the text within the tweet
    """

    myCount = 0

    while True:
        try:
            # This handles Twitter authetification and the connection to Twitter Streaming API
            l = MyListener(output_dir=output_dir, fileSizeLimit=fileSizeLimit,
                           logfile=logfile, startCount=startCount, **kwargs)
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            stream = Stream(auth, l)

            # Philippine bounding box
            stream.filter(follow=follow, track=track,
                          locations=locations)

        except BaseException as e:
            myCount += 1
            print("Error on_data: %s" % str(e))
            print("Restarting connection... Attempt #" + str(myCount))
            time.sleep(30)
            continue
