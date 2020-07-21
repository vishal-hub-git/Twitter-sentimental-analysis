import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
class TwitterClient(object):
    def __init__(self): 
        consumer_key = 'gMWadfLq6xqfSaZ3MwU6wCRKr'
        consumer_secret = 'bNO86F6RbfQ5GJhzn8L5n5JMU5edUEemXcoGSkYrGBKB9kE0R0'
        access_token = '2184272348-OWbHhav2A16bapjkktWDxX3BvvVBjx0QrJKz8j8'
        access_token_secret = 'Ovbh6az92iCU7ZoX9gKJ2R64g4ssfLTQH8jloLvO66wsX'
        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed")
            
    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
    
    def get_tweet_sentiment(self, tweet):  
        analysis = TextBlob(self.clean_tweet(tweet))  
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
        
    def fetch_tweets(self, query, count = 10): 
        tweets = [] 
        try: 
            fetched_tweets = self.api.search(q = query, count = count)             
            for tweet in fetched_tweets: 
                parsed_tweet = {}                
                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                if tweet.retweet_count > 0:  
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets
        except tweepy.TweepError as e: 
            print("Error : " + str(e))
            
def main():  
    api = TwitterClient() 
    tweets = api.fetch_tweets(query = 'Vijay', count = 200)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))  
    print("Neutral tweets percentage: {} % \ ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))  
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text'])  
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 
  
if __name__ == "__main__":  
    main() 