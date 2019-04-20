from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import zmq

# read in the app credentials from external file
creds = {}
credentials_file = 'credentials-vm1-tw-app'

with open(credentials_file, 'r') as f:
    for line in f.readlines():
        line = line.split(':')
        creds[line[0]] = line[1].strip()

# set up ZMQ to publish tweets
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')

# create Twitter Stream Listener 
class LiveStreamListener(StreamListener):
    def __init__(self, socket):
        self.socket = socket

    def on_data(self, data):
        # FOR QA: to confirm streamer is listening
        # print(data)
        # send data over zmq
        self.socket.send_json(data)
        return True

    def on_error(self, status):
        print(status)

# instantiate listener and set up authentication
listener = LiveStreamListener(socket=socket)
auth = OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
auth.set_access_token(creds['access_token'], creds['access_token_secret'])

# create stream object
stream = Stream(auth, listener)

while True:
    # filter for just the data you want from the stream
    stream.filter(track = ['verizon', 'humanability'])
