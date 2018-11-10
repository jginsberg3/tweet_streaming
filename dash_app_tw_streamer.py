import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import sqlite3
import datetime
import pytz
from functools import reduce
import itertools


# set up database info
dbname = 'tweets.sqlite'

# set query command to get data from the db into the app
query_command = '''
SELECT logtime, createdat, tweetid, tweettext,source, userid, quotecount, replycount, retweetcount, favoritecount
FROM tweets
WHERE logtime >= ?
'''
tweets_since_min = 1500000

def query_db(db, query, recency):
    '''
    Query the databsae and return the results to the app.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    time_filter = datetime.datetime.now() - datetime.timedelta(minutes=recency)
    time_filter = time_filter.strftime('%Y-%m-%d %H:%M:%S.%f')

    cur.execute(query, (time_filter,))
    res = cur.fetchall()

    cur.close()
    conn.close()

    return res

def trunc_to_minute(dt_str):
    '''
    Truncate timestamp to minute (not round to nearest minute - truncate to minute)
    '''
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S%z')
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

def get_minute_plot_data(query_res):
    '''
    Get data to plot the tweets-per-minute graphself.
    '''
    # for all the tweets in the query results, get their minute
    tweet_minutes = list(map(lambda x: trunc_to_minute(x[1]), query_res))

    # get the unique minutes in the query result
    unique_minutes = reduce(lambda x,y: x + [y] if not y in x else x, tweet_minutes,[])

    # get the number of tweets for each unique minute
    minute_counts = [tweet_minutes.count(i) for i in unique_minutes]

    return unique_minutes, minute_counts

def parse_tweet_time(tweet_row):
    '''
    Expect a row from the SQL query results and return both the parsed time of the tweet and the tweet text
    '''
    parsed_ts = datetime.datetime.strptime(tweet_row[1], '%Y-%m-%d %H:%M:%S%z')
    nytz = pytz.timezone('America/New_York')
    parsed_ts_tz = parsed_ts.astimezone(nytz)

    tweet_text = tweet_row[3]

    return parsed_ts_tz, tweet_text


def format_parsed_tweet_for_display(tw):
    '''Expects a parsed tweet from parse_tweet_time(); formats time and text for printing'''
    ts, txt = tw

    ts_frmt = ts.strftime('%m/%d/%y %H:%M:%S')

    #return ts_frmt + '\n' + txt + '\n-----'
    return [html.P(ts_frmt), html.P(txt), html.P('-----')]


# define dash app
app = dash.Dash()
server = app.server

# colors for formatting
colors = {'darkBackground':'#2F4F4F'}

# define app layout
app.layout = html.Div([
    html.Div([    # div to hold invisible stuff
        dcc.Interval(id='tweets-per-min-interval',  # control how often the elements auto-update
            interval = 5 * 1000,  # 5 seconds (in milliseconds)
            n_intervals = 0,
            max_intervals=-1
        ),
        
        html.Div([
            dcc.Store(id='query-results-store', storage_type='memory') # use to store query results
        ]),
    ]),
    
    html. Div([    
        html.Div([
            html.H2('Trending Tweets Per Minute'),
            html.H4('This is the graph that uses the Dash Store data:'),
            dcc.Graph(id='test-store-graph'),  # using to test new store component            
        ]),

        html.Div([
            html.H2('Here are the latest tweets:'),
            html.Div(id='tweet-text-div')
        ])
    ])
], style={'backgroundColor':colors['darkBackground'],'color':'white'})  # note: font color is set by "color" keyword



### define dash dynamic functions


# update the dcc.Store on the dcc tweets-per-min-interval
@app.callback(
    Output('query-results-store', 'data'),
    [Input('tweets-per-min-interval','n_intervals')]
)
def update_and_store_query_results(n_intervals):
    return query_db(dbname, query_command, tweets_since_min)


# update the test-store-graph using the dcc.Store
@app.callback(
    Output('test-store-graph', 'figure'),
    [Input('query-results-store', 'modified_timestamp')],
    [State('query-results-store', 'data')]
)
def update_test_graph(mod_ts, res):
    x_minutes, y_counts = get_minute_plot_data(res)

    plot_data = [go.Scatter(x=x_minutes, y=y_counts)]  # note: plot_data must be a LIST
    graph = {'data':plot_data}
    return graph


# display latest tweet text
@app.callback(
    Output('tweet-text-div', 'children'),
    [Input('query-results-store', 'modified_timestamp')],
    [State('query-results-store', 'data')]
)
def get_latest_tweet_text(mod_ts, res):
    parsed_times = list(map(parse_tweet_time, res))
    latest_parsed_times = sorted(parsed_times, key = lambda x: x[0], reverse=True)[0:5]

    output_p = list(map(format_parsed_tweet_for_display, latest_parsed_times))
    return list(itertools.chain(*output_p))  # flatten the list


# run the app
# probs remove for production and run with gunicorn
if __name__ == '__main__':
    app.run_server()
