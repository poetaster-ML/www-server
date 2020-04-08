from rabbitmq:3.6-management

COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.config

ENV RABBITMQ_LOGS=
ENV RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS=rotate_logs

RUN chown -R rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.config
