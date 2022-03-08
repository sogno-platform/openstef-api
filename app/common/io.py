from app.core.settings import Settings
from sognojq.amqp import AmqpPublisher

amqp_publisher = AmqpPublisher(
    amqp_host=Settings.amqp_host,
    amqp_port=Settings.amqp_port,
    amqp_username=Settings.amqp_username,
    amqp_password=Settings.amqp_password.get_secret_value(),
    amqp_exchange_name=Settings.amqp_exchange,
    topic_prefix="forecasting",
)