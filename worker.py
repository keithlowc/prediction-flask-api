import os
import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
#redis_url = os.getenv('REDISTOGO_URL', 'redis://h:pf65f564f913c62435fdd21b615e0c79e0d884072bd22072d8d85c2309b9f0b9e@ec2-34-234-124-166.compute-1.amazonaws.com:31799')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()