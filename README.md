# Twitter-Sentiment-Analysis

## Requirements:
````sh
pip install tweepy
pip install pandas
pip install matplotlib
pip install transformers
pip install scipy
````

## Credentials
Due to security reasons, a **config.ini** is not included. However, this can easily obtained from twitter. <br>
Really Useful Guide: [Youtube](https://www.youtube.com/playlist?list=PL7Lkk4UtXtOw04G1nRapMNgd2myNJCZSJ) <br>
The config file can be created and saved in the folder & its structure should look like this: <br>
````sh
[twitter]

api_key = <api key>
api_key_secret = <api key secret>

access_token = <access token>
access_token_secret = <access token secret>
````

Do not give anyone access to these credentials, as they will gain **full access** to your Twitter account without needing to know your twitter handle or your password.

#Automation
You can use a task scheduler to run a batch file on your Windows Server/Computer (see example under automate), or a cron job for linux
