"""
VerifyKE RabbitMQ connection and messaging utilities.

This file handles the connection between the VerifyKE
application and RabbitMQ.

RabbitMQ will allow VerifyKE to send background-processing
events without making the user's HTTP request wait for
that processing to finish.
"""

import json
import aio_pika
from aio_pika import message

# RabbitMQ connection settings.
#
# These are development defaults.
# We will move these into application configuration later.
RABBITMQ_URL = "amqp://guest:guest@localhost"

async def publish_event(
    queue_name:str,
    event: dict,
) -> None:
    """
    Publish an event to a RabbitMQ queue.

    Args:
        queue_name:
            The name of the RabbitMQ queue.

        event:
            A Python dictionary containing the event data.
    """
   # Open a connection to RabbitMQ
   
    connection = await aio_pika.connect_robust(
       RABBITMQ_URL
    )
    try:
        # Create a communication channel
        channel = await connection.channel() 

        # Make sure the queue exists
        queue = await channel.declare_queue(
            queue_name,
            durable =  True,
        )

        # Convert the Python dictionary into JSON
        message_body = json.dumps(event).encode()

        # Create the RabbitMQ message
        message = message(
            body = message_body,
            content_type = "application/json",
            delivery_mode = aio_pika.DeliveryMode.PERSISTENT,
        )

        # Publish the message directly to the queue
        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )

    finally:
        # Always close the connection after publishing
        await connection.close()