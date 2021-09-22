import log
import time
import clients
import config
import cherrypy
import jwt

logger = log.create_logger(__name__)

class Security:
    def __init__(self):
        self.last_jtis = {} # dictionary client id => last used jti. Maybe convert to list to be more secure

    def is_public_access(self, request):
        #logger.debug("Access from request.base %s with headers %s", request.base, request.headers)
        on_port = request.base.endswith(str(config.HTTPD_PUBLIC_PORT))
        on_custom_heaer = request.headers.get('X-Cml-Public') == "True"
        return on_port or on_custom_heaer

    def find_client(self, request):
        if self.is_public_access(request):
            logger.debug("Public access detected, checking jwt")
            token = request.headers.get('AUTHORIZATION')
            if not token:
                logger.error("Authorization header missing")
            elif token.startswith("Bearer "):
                token = token[7:]
                logger.debug("Found token %s", token)
                all_clients = clients.get_clients()
                for client in all_clients:
                    try:
                        logger.debug("Checking client %s (%s)", client.get('id'), client.get('message'))
                        if not client.get('approved'):
                            logger.debug("Not approved")
                            continue
                        # https://stackoverflow.com/a/32804171 - we're receiving PKCS8, not PKCS1
                        decoded = jwt.decode(token, client.get('key'), algorithms='RS256')
                        if (self.check_time(decoded, client)):
                            return client
                        #print(decoded)
                    except ValueError:
                        logger.warn("Skipping key %s as it can't be parsed", client.get('key'))
                    except jwt.exceptions.InvalidSignatureError:
                        logger.debug("Skipping client %s (%s) on signature error", client.get('id'), client.get('message'))
            else:
                logger.error("Unknown authorization")
            return False

    def registered_client(self, request):
        client = self.find_client(request)
        if not client:
            raise cherrypy.HTTPError(403, message="Token missing or wrong")

    def check_time(self, token, client):
        current_epoch = time.time()
        token_time = token.get('jti')
        if token_time:
            last_used_jti = self.last_jtis.get(client.get('id'))
            if last_used_jti and last_used_jti == token_time:
                logger.warn("Jti reused detected for client %s", client.get('id'))
                return False
            self.last_jtis[client.get('id')] = token_time
            diff = current_epoch - int(token_time) / 1000.0
            logger.debug("Detected time diff: %f seconds", diff)
            return diff < 120
        return False

    def only_internal(self, request):
        if self.is_public_access(request):
            raise cherrypy.HTTPError(403)

    def command(self, request, number):
        if self.is_public_access(request):
            client = self.find_client(request)
            if client:
                if client.get('all_commands'):
                    return client
                logger.debug("Commands are %s", str(client.get('commands', [])))
                if int(number) in client.get('commands', []):
                    return client
                raise cherrypy.HTTPError(403, message="Forbidden command")
            raise cherrypy.HTTPError(401)
        else:
            return None # internal network

