import json
import logging
import os
import time
from urllib.request import Request, urlopen
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
BROKERS = os.getenv('KAFKA_BROKERS', 'kafka:9092')
TOPIC = os.getenv('KAFKA_TOPIC', 'discrepancy.flagged')
WEBHOOK = os.getenv('N8N_WEBHOOK_URL', 'http://n8n:5678/webhook/discrepancy-intake')

def deliver(payload: dict, attempts: int = 3) -> bool:
    body = json.dumps(payload).encode()
    for attempt in range(1, attempts + 1):
        try:
            request = Request(WEBHOOK, data=body, headers={'Content-Type': 'application/json'})
            with urlopen(request, timeout=15) as response:
                if 200 <= response.status < 300:
                    return True
        except Exception as exc:
            logging.warning('webhook attempt=%s event_id=%s error=%s', attempt, payload.get('event_id'), exc)
            time.sleep(attempt)
    return False

def run() -> None:
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BROKERS, group_id='ledgerguard-bridge', enable_auto_commit=False, value_deserializer=lambda value: json.loads(value.decode()))
    logging.info('bridge listening topic=%s webhook=%s', TOPIC, WEBHOOK)
    for record in consumer:
        if deliver(record.value):
            consumer.commit()
            logging.info('delivered event_id=%s offset=%s', record.value.get('event_id'), record.offset)
        else:
            logging.error('delivery failed; offset retained event_id=%s', record.value.get('event_id'))

if __name__ == '__main__': run()
