import zmq
import datetime
import sqlite3
import json

dbname = 'tweets.sqlite'

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://0.0.0.0:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')

table_create_sql = '''
CREATE TABLE IF NOT EXISTS tweets (
logtime DATETIME,
createdat DATETIME,
tweetid BIGINT,
tweettext TEXT,
source TEXT,
userid TEXT,
quotecount BIGINT,
replycount BIGINT,
retweetcount BIGINT,
favoritecount BIGINT,
rawtweet VARCHAR
)
'''

def create_table():
    conn = sqlite3.connect(dbname)
    conn.execute(table_create_sql)
    conn.close()


def parse_tweet(tweet):
    '''
    Read in a tweet and parse out desired fields.
    '''
    try:
        # logtime is time of tweet capture
        logtime = datetime.datetime.now()
        createdat = datetime.datetime.strptime(tweet['created_at'],
                                               '%a %b %d %H:%M:%S %z %Y')
        tweetid = tweet['id']
        tweettext = tweet['text']
        source = tweet['source']
        userid = tweet['user']['id']
        quotecount = tweet['quote_count']
        replycount = tweet['reply_count']
        retweetcount = tweet['retweet_count']
        favoritecount = tweet['favorite_count']
        rawtweet = json.dumps(tweet)
        parsed_tweet = [logtime, createdat, tweetid, tweettext,
                        source, userid, quotecount, replycount,
                        retweetcount, favoritecount, rawtweet]
        return parsed_tweet
    
    except:
        pass

def write_tweet_to_db(parsed_tweet, db):
    '''
    Write the parsed tweet to the databse
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    insert_sql = """
    INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """
    cur.execute(insert_sql, parsed_tweet)
    conn.commit()
    conn.close()


create_table()
while True:
    msg = socket.recv_json()
    loaded_msg = json.loads(msg)
    parsed_tweet = parse_tweet(loaded_msg)
    write_tweet_to_db(parsed_tweet, dbname)
