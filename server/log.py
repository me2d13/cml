import logging
import datetime
from python_elastic_logstash import ElasticHandler, ElasticFormatter

#elasticsearch_endpoint = 'http://localhost:9213'
elasticsearch_endpoint = 'http://es:9200'
elastic_handler = ElasticHandler(elasticsearch_endpoint, elastic_index='cml-'+datetime.datetime.utcnow().strftime('%Y-%m-%d'))  # Second argument is optional
elastic_handler.setFormatter(ElasticFormatter())


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

def create_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(console_handler)
    return log

def create_es_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(elastic_handler)
    return log
