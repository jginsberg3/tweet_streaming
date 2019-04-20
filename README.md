# Tweet Streaming Project

## Overview

This is a basic Tweet streamer using the Tweepy library.  Right now it streams tweets for the keywords "Verizon" and "Humanability".  

The tweets are shown in a Plotly Dash webapp.  The current app displays the number of tweets per minute and the text of the latest five tweets.

**NOTE:**

To run this app, you must supply your own Twitter Developer API credentials.  I have not included any credentials in this repo.  

The code assumes the credentials are passed in a credentials file with the format:

---

access_token:[access_tocken]

access_token_secret:[access_token_secret]

consumer_key:[consumer_key]

consumer_secret:[consumer_secret]

---

## Instructions to Run

1. pip install the requirements.txt
2. Run tweet_streamer.py to start getting the tweets from Twitter
3. Run store_tweets.py to store the tweets to a local sqlite db
4. Run dash_app_tw_streamer.py to start the webapp


## Future To-Dos

- Make the stream keywords more customizable
- Further develop the visualizations in the webapp
