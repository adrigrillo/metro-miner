"""
Twitter stream listener that listen for tweets related with the madrid metro. The filter parameters could be found
in the 'config.ini' file and the Twitter API authentication tokens have to be saved in a file named
'authentication.ini'.

The 'authentication.ini' parameters should be:
key = Access Token
secret = Access Token Secret
app_key = Consumer Key (API Key)
app_secret = Consumer Secret (API Secret)
"""
import io
import json
import logging

from fastavro import schemaless_writer
from kafka import KafkaProducer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from metro_streamer import auth_config, config, setup_logging

KAFKA_SERVER = config['kafka']['servers']
KAFKA_CLIENT_ID = config['kafka']['client_id']
KAFKA_TOPIC = config['kafka']['topic']
TWITTER_KEY = auth_config['twitter']['key']
TWITTER_SECRET = auth_config['twitter']['secret']
TWITTER_APP_KEY = auth_config['twitter']['app_key']
TWITTER_APP_SECRET = auth_config['twitter']['app_secret']
TWITTER_ACCOUNTS = list(config['accounts'].values())
METRO_KEYWORDS = config['keywords']['general'].split(',')
METRO_STATIONS = config['keywords']['stations'].split(',')


def on_send_error(exception):
    """
    Error handler for the kafka producer, if any error is catch it will be logged
    :param exception: catch exception by the producer
    """
    logger.error('Error sending the message to kafka', exc_info=exception)


def write_data(data):
    """
    Encode json with fastavro module into avro format given a schema.

    :param data: data to encode
    :return: data encoded
    """
    raw_data = io.BytesIO()
    schemaless_writer(raw_data, schema, data)
    return raw_data.getvalue()


def generate_tweet_dict(text, date, user_id, place=None, country=None, country_code=None):
    """
    Tweet dict generator. This method generated a tweet schema compliant dict that avro
    will encode correctly with the passed data
    :param text: twitter text
    :param date: timestamp in UTC when the tweet was created
    :param user_id: user id of the writer of the tweet
    :param place: name of the place where the tweet was written
    :param country: country where the tweet was written
    :param country_code: code of the country where the tweet was written
    :return: dict with the data generated
    """
    date = date.replace(microsecond=0).isoformat()
    return locals()


class TwitterListener(StreamListener):
    """ Twitter stream listener that receives the tweet and creates the object that will be processed """

    def on_status(self, status):
        """
        Method that is executed when a new twitter status is received. This method will generate
        the tweet object that will be used to process the content.

        :param status: api tweet object will al the information
        :return: true to keep the steam connected
        """
        logger.debug('Received tweet: %s', status.text)
        # form the tweet object with the data
        if hasattr(status, 'retweeted_status'):
            status = status.retweeted_status
        if hasattr(status, 'quoted_status'):
            status.text = status.text + status.quoted_status['text']
        if status.place is None:
            tweet_data = generate_tweet_dict(status.text, status.created_at, status.user.id)
        else:
            tweet_data = generate_tweet_dict(status.text, status.created_at, status.user.id, status.place.name,
                                             status.place.country, status.place.country_code)
        # encode and send tweet
        producer.send(topic=KAFKA_TOPIC, value=tweet_data).add_errback(on_send_error)
        return True

    def on_error(self, error_code):
        """
        Method that log if any error is raised by the twitter stream
        :param error_code: error code indicating the error raised
        :return: if the error is connection related disconnect the client (false) else keep the connection (true)
        """
        logger.error('Error with the stream connection. Error code: %s', error_code)
        if error_code == 420:
            producer.close()
            return False
        else:
            return True


if __name__ == '__main__':
    # setup logging
    logger = logging.getLogger(__name__)
    setup_logging()
    # loading avro schema
    with open('../schema/tweet.avsc', 'r', encoding='utf-8') as schema_spec:
        schema = json.loads(schema_spec.read())
    # setup kafka
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, client_id=KAFKA_CLIENT_ID, value_serializer=write_data)
    # setup twitter auth
    oauth = OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
    oauth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
    listener = TwitterListener()
    # twitter stream configuration and start
    stream = Stream(oauth, listener)
    stream.filter(track=METRO_KEYWORDS + METRO_STATIONS, follow=TWITTER_ACCOUNTS, languages=["es", "en"], async=True)
