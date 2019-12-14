# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import time
import os


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    myPath = ""
    outJson = ""
    fileCount = 1
    fileSize = 0
    startCount = 1

    def __init__(self, output_dir, fileSizeLimit=250000000, logfile='logfile.txt', startCount=1):
        # self.myPath = os.getcwd() + "\\tweets"
        self.myPath = output_dir
        self.startCount = startCount
        self.fileSizeLimit = fileSizeLimit
        self.logfile = logfile

        # self.fileCount = len(os.listdir(self.myPath)) + self.startCount
        self.fileCount = self.startCount
        self.outJson = "tweet" + str(self.fileCount) + ".json"

        if len(os.listdir(self.myPath)) == 0:
            self.fileSize = 0
        else:
            self.fileSize = os.path.getsize(self.myPath + "\\" + self.outJson)

        print("Downloder running!")

    def on_data(self, data):
        self.get_tweet(data)

    def on_error(self, status):
        print(status)
        return True

    def get_tweet(self, data):
        if self.fileSize <= self.fileSizeLimit:
            try:
                with open(self.myPath + "\\" + self.outJson, 'a') as f:
                    f.write(data)
                    self.fileSize = os.path.getsize(
                        self.myPath + "\\" + self.outJson)
                    return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                time.sleep(5)
            return True

        else:
            self.fileCount = self.fileCount + 1
            self.outJson = "tweet" + str(self.fileCount) + ".json"

            try:
                open(self.myPath + "\\" + self.outJson, 'a')
            except BaseException as e:
                print("Error on_data: %s" % str(e))

            self.fileSize = os.path.getsize(self.myPath + "\\" + self.outJson)
            print("Creating file #" + str(self.fileCount))

            try:
                with open(self.logfile, 'a') as f:
                    f.write("Created " + self.outJson + " at " + str(time.strftime(
                        "%I:%M:%S") + " - " + str(time.strftime("%d/%m/%Y")) + "\n"))
                    # print(self.fileSize)
            except BaseException as e:
                print("Error on_data: %s" % str(e))


def download_tweets(consumer_key, consumer_secret, access_token, access_token_secret,
                    output_dir, startCount=1,
                    locations=[116.702882, 5.621718, 129.387207, 21.933351],
                    follow=None, track=None,
                    fileSizeLimit=250000000, logfile='logfile.txt'):
    """Download tweets from Twitter API and save to .json files of specified size

    Arguments:
        consumer_key {str} -- the consumer_key access token obtained from Twitter app
        consumer_secret {str} -- consumer_secret access token obtained from Twitter app
        access_token {str} -- access_token obtrained from Twitter app
        access_token_secret {str} -- access_token_secret obtained from Twitter app
        output_dir {str} -- directory of the output .json files containing tweets

    Keyword Arguments:
        startCount {int} -- the starting number of the output json file. Use this for continuation when previous files were removed. (default: {1})
        locations {list of size 4} -- the coordinates of the location bounding box. Values represents [west_long, south_lat, east_long, north_lat]. Default is Philippine area (default: {[116.702882, 5.621718, 129.387207, 21.933351]})
        follow {int} -- A comma separated list of user IDs, indicating the users to return statuses for in the stream. (default: {None})
        track {int} -- Keywords to track. Phrases of keywords are specified by a comma-separated list. See track for more information. (default: {None})
        fileSizeLimit {int} -- the estimated size of each output .json file in bytes (default: {250000000})
        logfile {str} -- the log file (default: {'logfile.txt'})
    """

    myCount = 0

    while True:
        try:
            # This handles Twitter authetification and the connection to Twitter Streaming API
            l = MyListener(output_dir=output_dir, fileSizeLimit=fileSizeLimit,
                           logfile=logfile, startCount=startCount)
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