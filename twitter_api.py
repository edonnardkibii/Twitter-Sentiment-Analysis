import tweepy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from datetime import datetime as dt
import os
# import configparser
import twitterconfig as tc
ENCODING = 'utf-8'


def scrape(hashtag, start_date, tweetlim, current_date, extension):
    # column_info = ['username', 'description', 'location', 'following', 'followers', 'totaltweets',
    #         'text', 'hashtags']
    column_info = ['Tweets']
    df = pd.DataFrame(columns=column_info)

    tweets = tweepy.Cursor(api.search_tweets, hashtag, lang="en", since_id=start_date,
                           tweet_mode='extended').items(tweetlim)
    list_tweets = [tweet for tweet in tweets]

    # print(list_tweets)
    i=1

    for tweet in list_tweets:
        # username = tweet.user.screen_name
        # description = tweet.user.description
        # location = tweet.user.location
        # following = tweet.user.friends_count
        # followers = tweet.user.followers_count
        # totaltweets = tweet.user.statuses_count
        # hashtags = tweet.entities['hashtags']

        try:
            text_tweet = tweet.retweeted_status.full_text
        except AttributeError:
            text_tweet = tweet.full_text

        """
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
        """

        # single_tweet = [username, description, location, following, followers, totaltweets,
        #                 text, hashtext]

        # df.loc[len(df)] = single_tweet
        df.loc[len(df)] = text_tweet
        i=i+1

    path = 'Values\\'
    filename = '-Scraped_Tweets.csv'
    if not os.path.exists(extension + path + current_date + "\\"):
        os.mkdir(extension + path + current_date + "\\")

    df.to_csv(extension + path + current_date + "\\" + hashtag+ filename, index=False, encoding=ENCODING)


def sentiment_analysis(hashtag, current_date, extension):
    path = 'Values\\'
    filename = hashtag + '-Scraped_Tweets.csv'
    data = pd.read_csv(extension + path + current_date + "\\" + filename, usecols=['Tweets'], encoding=ENCODING)
    data.sort_values('Tweets', inplace=True)
    data.drop_duplicates(subset='Tweets', keep=False, inplace=True)
    scraped_tweets = data['Tweets'].tolist()

    processed_tweets_list = []
    for tweet in scraped_tweets:
        tweet_words = []
        for word in tweet.split(' '):
            if word.startswith('@') and len(word) > 1:
                word = '@user'
            elif word.startswith('http'):
                word = "http"

            tweet_words.append(word)
        processed_tweet = " ".join(tweet_words)
        processed_tweets_list.append(processed_tweet)

    # Load model & tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    # labels = ['Negative', 'Neutral', 'Positive']

    #Sentiment Analysis
    output_list = []
    for proc_tweet in processed_tweets_list:
        encoded_tweet = tokenizer(proc_tweet, return_tensors='pt')
        output=model(**encoded_tweet)
        output_list.append(output)

    scores_list = []
    for output_score in output_list:
        scores = output_score[0][0].detach().numpy()
        scores = softmax(scores)
        scores_list.append(scores)

    # print(scores_list)
    sentiment_values = np.array(scores_list)
    # print(sentiment_values)
    save_results(sentiment_values, processed_tweets_list, hashtag, current_date, extension)
    """
    negative_values = sentiment_values[:,0]
    neutral_values = sentiment_values[:,1]
    positive_values = sentiment_values[:,2]



    mean_negative_values = np.mean(negative_values)
    mean_neutral_values = np.mean(neutral_values)
    mean_positive_values = np.mean(positive_values)

    # print("Negative Values: " +str(mean_negative_values))
    # print("Neutral Values: " + str(mean_neutral_values))
    # print("Positive Values: " + str(mean_positive_values))

    return mean_negative_values, mean_neutral_values, mean_positive_values
    """


def save_results(dataset, tweets, hashtag, current_date, extension):
    negative_values = dataset[:,0]
    neutral_values = dataset[:,1]
    positive_values = dataset[:,2]

    dict = {'Tweet': tweets, 'Negative': negative_values, 'Neutral': neutral_values,
            'Positive': positive_values}

    df = pd.DataFrame(dict)

    path = 'SentimentResults\\'
    filename = hashtag + '-Sentiment_Results.csv'
    #Save
    if not os.path.exists(extension+ path + current_date + "\\"):
        os.mkdir(extension + path + current_date + "\\")

    df.to_csv(extension + path + current_date + "\\" + filename, header=True, index=True)


def piechart_plot(plot_values):
    # dataset = [negative_values, neutral_values, positive_values]
    mercedes_dataset = plot_values[0]
    audi_dataset = plot_values[1]
    bmw_dataset = plot_values[2]
    vw_dataset = plot_values[3]
    tesla_dataset = plot_values[4]

    legend = ['Negative', 'Neutral', 'Positive']

    # Subplots
    plt.subplot(321)
    plt.pie(mercedes_dataset, labels=legend)
    plt.title('Mercedes')

    plt.subplot(322)
    plt.pie(audi_dataset, labels=legend)
    plt.title('Audi')

    plt.subplot(323)
    plt.pie(bmw_dataset, labels=legend)
    plt.title('BMW')

    plt.subplot(324)
    plt.pie(vw_dataset, labels=legend)
    plt.title('VW')

    plt.subplot(325)
    plt.pie(tesla_dataset, labels=legend)
    plt.title('Tesla')

    plt.tight_layout()
    # fig = plt.figure()

    plt.show()


if __name__ == '__main__':
    try:
        # read config file
        # config = configparser.ConfigParser()
        # config.read('config.ini')
        extension = "C:\\Users\\james\\PycharmProjects\\TwitterSentimentAnalysis\\"
        current_date = dt.now().strftime('%Y_%m_%d_%H_%M_%S')
        print('Configuring Twitter API')
        """
        api_key = config['twitter']['api_key']
        print(type(api_key))
        api_key_secret = config['twitter']['api_key_secret']

        access_token = config['twitter']['access_token']
        access_token_secret = config['twitter']['access_token_secret']
        """
        api_key = tc.api["api key"]
        # print(type(api_key_1))
        api_key_secret = tc.api["api key secret"]

        access_token = tc.access["access token"]
        access_token_secret = tc.access["access token secret"]

        # Authentication
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True)

        hashtags = ['#MercedesBenz','#Audi', '#BMW', '#VW', '#Tesla']

        start_date = '2022--05--01'
        num_of_tweets = 200

        sentiment_values = []
        for hashtag in hashtags:
            print('Starting scraping process for ' +(hashtag))
            scrape(hashtag, start_date, num_of_tweets, current_date, extension)
            print('Scraping complete')

            print('Starting Sentiment Analysis')
            sentiment_analysis(hashtag, current_date, extension)
            print('Sentiment Analysis Complete for ' + (hashtag))

        """
            mean_neg_val, mean_neut_val, mean_pos_val = sentiment_analysis(hashtag)
            mean_values = [mean_neg_val, mean_neut_val, mean_pos_val]
            sentiment_values.append(mean_values)
            print('Sentiment Analysis Complete for ' + (hashtag))
        sentiment_values = np.array(sentiment_values)

        # piechart_plot(sentiment_values)
        """
    except KeyboardInterrupt:
        print('Process terminated')