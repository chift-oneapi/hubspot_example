import os

import chift
from chift.api.client import ChiftClient
from chift.openapi.models import Consumer
from dotenv import load_dotenv


def get_client():
    return ChiftClient(
        client_id=os.getenv("CHIFT_CLIENT_ID"),
        client_secret=os.getenv("CHIFT_CLIENT_SECRET"),
        account_id=os.getenv("CHIFT_ACCOUNT_ID"),
        url_base=os.getenv("CHIFT_URL"),
    )


def get_consumer(client: ChiftClient, consumer_id: str) -> Consumer:
    return chift.Consumer.get(consumer_id, client)


def main():
    client = get_client()
    consumer = get_consumer(client, os.getenv("CHIFT_CONSUMER_ID"))
    contacts = consumer.invoicing.Contact.all(client=client)
    print(contacts)


if __name__ == "__main__":
    load_dotenv()
    main()
