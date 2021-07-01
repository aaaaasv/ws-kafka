import os

KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost')
KAFKA_PORT = os.environ.get('KAFKA_PORT', default='9092')
KAFKA_TOPICS = os.environ.get('KAFKA_TOPICS', default='quickstart-events').split(' ')
