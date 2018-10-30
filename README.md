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

1. Create an anaconda environment using the environment.yml file
    - Alternatively, use the environment file as a basis for creating a venv if not using anaconda
2. Create a credentials file and add credentials as noted above.
3. Run the tw_stream_listener notebook
4. Run the recieve_and_parse_tweets notebook
    - This will create a tweets.sqlite file that stores the tweets
5. Run the dash_app_tw_streamer.py file to launch the webapp


## Future To-Dos

- Make the stream keywords more customizable
- Further develop the visualizations in the webapp