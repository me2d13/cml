import log
import json 
import config
import uuid
import datetime

logger = log.create_logger(__name__)


def register_client(key, message):
    logger.debug('Registering cient with note %s', message)
    client = {
        "id": str(uuid.uuid4()),
        "key": key,
        "message": message,
        "registered_at": datetime.datetime.today().isoformat(),
        "all_commands": True,
        "commands": []
    }
    clients = load_clients_from_file()
    clients.append(client)
    save_clients_to_file(clients)

def enrich_with(origin, updater):
    res = {}
    for k, v in origin.items():
        if k in updater:
            res[k] = updater[k]
        else:
            res[k] = v
    return res

def update_client(id, data):
    logger.debug('Updating cient with id %s', id)
    clients = load_clients_from_file()
    new_clients = []
    for cl in clients:
        if cl.get('id') == id:
            new_clients.append(enrich_with(cl, data))
        else:
            new_clients.append(cl)
    save_clients_to_file(new_clients)
    return new_clients

def delete_client(id):
    logger.debug('Deleting cient with id %s', id)
    clients = load_clients_from_file()
    new_clients = []
    deleted = False
    for cl in clients:
        if cl.get('id') == id:
            deleted = True
        else:
            new_clients.append(cl)
    save_clients_to_file(new_clients)
    return deleted

def get_clients():
    return load_clients_from_file()

def save_clients_to_file(clients):
    with open(config.CLIENTS_FILE, 'w') as outfile:
        json.dump(clients, outfile, indent=4)

def load_clients_from_file():
    try:
        with open(config.CLIENTS_FILE) as json_file:  
            data = json.load(json_file)
            #logger.debug("Read clients data from file %s: %s", config.CLIENTS_FILE, json.dumps(data, indent=4))
            return data
    except OSError:
        logger.info("Config file %s not found. Using empty list", config.CLIENTS_FILE)
    return []