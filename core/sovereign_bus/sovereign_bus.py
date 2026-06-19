import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union
import structlog
from pydantic import BaseModel, Field
import nats
from nats.aio.client import Client as NATSClient
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from opentelemetry import trace
from opentelemetry.propagate import inject, extract

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

class SovereignMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sender: str
    topic: str
    payload: Dict[str, Any]
    context: Dict[str, str] = Field(default_factory=dict)

class SovereignBus:
    def __init__(self, nats_url: str = "nats://localhost:4222", kafka_bootstrap_servers: str = "localhost:9092"):
        self.nats_url = nats_url
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.nats_client: Optional[NATSClient] = None
        self.kafka_producer: Optional[AIOKafkaProducer] = None
        self.subscriptions: Dict[str, Any] = {}

    async def connect(self):
        try:
            self.nats_client = await nats.connect(self.nats_url)
            self.kafka_producer = AIOKafkaProducer(
                bootstrap_servers=self.kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self.kafka_producer.start()
            logger.info("Bus: Connected to NATS and Kafka")
        except Exception as e:
            logger.error("Bus: Connection Failed", error=str(e))
            raise

    async def disconnect(self):
        if self.nats_client: await self.nats_client.drain()
        if self.kafka_producer: await self.kafka_producer.stop()

    async def publish_fast(self, topic: str, message: SovereignMessage):
        with tracer.start_as_current_span(f"publish_fast:{topic}"):
            inject(message.context)
            if self.nats_client:
                await self.nats_client.publish(topic, message.model_dump_json().encode())

    async def publish_durable(self, topic: str, message: SovereignMessage):
        with tracer.start_as_current_span(f"publish_durable:{topic}"):
            inject(message.context)
            if self.kafka_producer:
                await self.kafka_producer.send_and_wait(topic, message.model_dump())

    async def subscribe_fast(self, topic: str, callback: Callable[[SovereignMessage], Any]):
        async def handler(msg):
            ctx = extract(json.loads(msg.data.decode()).get("context", {}))
            with tracer.start_as_current_span(f"handle_fast:{topic}", context=ctx):
                await callback(SovereignMessage.model_validate_json(msg.data.decode()))
        sub = await self.nats_client.subscribe(topic, cb=handler)
        self.subscriptions[f"fast:{topic}"] = sub

    async def subscribe_durable(self, topic: str, group_id: str, callback: Callable[[SovereignMessage], Any]):
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.kafka_bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        await consumer.start()
        async def loop():
            try:
                async for msg in consumer:
                    ctx = extract(msg.value.get("context", {}))
                    with tracer.start_as_current_span(f"handle_durable:{topic}", context=ctx):
                        await callback(SovereignMessage.model_validate(msg.value))
            finally: await consumer.stop()
        task = asyncio.create_task(loop())
        self.subscriptions[f"durable:{topic}"] = (consumer, task)
