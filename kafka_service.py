import json
import sys
import asyncio

from confluent_kafka import Producer, KafkaError, KafkaException
from confluent_kafka import Consumer
import socket


producerConf = {
    'bootstrap.servers': "localhost:9092",
    # 'client.id': socket.gethostname()
}

consumerConf = {
    'bootstrap.servers': "localhost:9092",
    'group.id': "ordersDataGroup",
    'auto.offset.reset': "earliest"
}

producer = Producer(producerConf)
consumer = Consumer(consumerConf)

def send():
    producer.produce("stringmsg", key="2", value="string from python")
    producer.flush()

def request_to_database():
    producer.produce("requestDataFromDB", key="3", value="give me data from DB")
    producer.flush()


def request_on_orders_data():
    producer.produce("requestOrdersDataFromOrchestrator", key="4", value="give me orders data from DB")
    producer.flush()


def save_orders():
    with open("new_orders_with_usernames_without_ids.txt", "r", encoding='utf-8-sig') as f:
        raw_data = f.read()

    producer.produce("frontSaveOrders", key="7", value=raw_data.encode('utf-8'))
    producer.flush()
    print("save_orders done")


def save_products():
    # with open("products.txt", "r", encoding='utf-8-sig') as f:
    with open("new_products.txt", "r", encoding='utf-8-sig') as f:
        data = str(json.load(f))
        print(data)
        print(type(data))
    producer.produce("frontSaveProducts", key="8", value=data.encode('utf-8'))
    producer.flush()
    print("save_products done")


def get_orders_data():

    try:
        consumer.subscribe(["sendOrdersDataToRecommendationModule"])

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                    print('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(msg)
                print(msg.value())
                print(str(msg.value()))
                print(msg.value().decode('utf-8'))
    finally:
        consumer.close()


if __name__ == '__main__':
    ...
    # send()
    # request_on_orders_data()
    # get_orders_data()
    save_orders()
    # save_products()