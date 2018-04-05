import io
import json
import logging

from fastavro import schemaless_reader
from kafka import KafkaConsumer

from metro_analyzer import setup_logging, config

KAFKA_SERVER = config['kafka']['servers']
KAFKA_GROUP_ID = config['kafka']['group_id']
KAFKA_TOPIC = config['kafka']['topic']


def read_data(data):
    """
    Decode raw data with fastavro module into avro format given a schema.

    :param data: data to encode
    :return: data encoded
    """
    io_stream = io.BytesIO(data)
    return schemaless_reader(io_stream, schema)


if __name__ == '__main__':
    # setup logging
    logger = logging.getLogger(__name__)
    setup_logging()
    # loading avro schema
    with open('../schema/tweet.avsc', 'r', encoding='utf-8') as schema_spec:
        schema = json.loads(schema_spec.read())
    # setup kafka
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, group_id=KAFKA_GROUP_ID, value_deserializer=read_data)
    consumer.subscribe(topics=KAFKA_TOPIC)
    for message in consumer:
        with open("tweets.json", "a") as my_file:
            msg_json = json.dumps(message.value, ensure_ascii=False)
            my_file.write(msg_json + ',')
