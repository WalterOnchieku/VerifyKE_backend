"""
VerifyKE risk analysis worker.

This worker listens for report-created events from RabbitMQ.

For now, it only demonstrates that the event was successfully
received and processed.

Later, this worker will call the actual risk analysis service.
"""
import asyncio
import json

import aio_pika

#RabbitMQ connection url

RABBITMQ_URL = "amqp://guest:guest@localhost/"

# Queue that receives newly created report events
QUEUE_NAME = "report_created"

async def process_report(event: dict) ->None:
    """
    Process a newly created report event.

    For now, we simply display the event.

    Later this function will perform things such as:
    - Risk scoring
    - Duplicate detection
    - Entity analysis
    """

    print("\n========================================")
    print("New VerifyKE report event received")
    print("========================================")

    print(
        f"Event type: {event.get('event_type')}"
    )

    print(
        f"Report ID: {event.get('report_id')}"
    )

    print(
            f"User ID: {event.get('user_id')}"
        )

    print(
            f"Entity ID: {event.get('report_id')}"
        )

    print("========================================\n")

async def main():
    """
    Connect to RabbitMQ and continuously listen
    for report-created events.
    """

    print("Connecting to RabbitMQ...")

    connection = await aio_pika.connect_robust(
        RABBITMQ_URL
    )

    print("Connected to RabbitMQ.")

    channel = await connection.channel()

    # Make sure the queue exists
    queue = await channel.declare_queue(
        QUEUE_NAME,
        durable=True
    )

    print(
        f"waiting for messages on '{QUEUE_NAME}'...."
    )

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    # Convert the message body from bytes
                    # back into a Python dictionary
                    event = json.loads(
                        message.body.decode()
                    )

                    await process_report(event)
                except Exception as error:
                    print(
                        f"Error processing message: {error}"
                    )

if __name__ == "__main__":
    asyncio.run(main())
