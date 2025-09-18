import logging
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth
from config import OPENOBSERVE_ENDPOINT, OPENOBSERVE_USERNAME, OPENOBSERVE_PASSWORD

class OpenObserveHandler(logging.Handler):
    def __init__(self, endpoint, username, password):
        super().__init__()
        self.endpoint = endpoint
        self.auth = HTTPBasicAuth(username, password)

    def emit(self, record):
        log_entry = self.format(record)
        headers = {'Content-Type': 'application/json'}
        try:
            requests.post(
                self.endpoint,
                data=log_entry,
                headers=headers,
                auth=self.auth,
                timeout=2
            )
        except Exception:
            pass  # Optionally, handle/log errors

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'pathname': record.pathname,
            'lineno': record.lineno,
            'funcName': record.funcName,
        }
        return json.dumps(log_record)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

json_formatter = JsonFormatter()
openobserve_handler = OpenObserveHandler(
    OPENOBSERVE_ENDPOINT,
    OPENOBSERVE_USERNAME,
    OPENOBSERVE_PASSWORD
)
openobserve_handler.setLevel(logging.DEBUG)
openobserve_handler.setFormatter(json_formatter)

def create_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(console_handler)
    return log

def create_oo_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(openobserve_handler)
    return log
