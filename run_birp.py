import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from main import app
config = Config()
config.bind = ["0.0.0.0:8091"]
config.worker_class = 4
# logs
# config.accesslog = "-"
# config.errorlog = "-"
config.startup_timeout = 669
config.keep_alive_timeout = 669

# ssl config
# config.ca_certs = "path/to/ca_certs.pem" #Path to the SSL CA certificate file.
# config.certfile = "path/to/certfile.pem" #Path to the SSL certificate file.
# config.ciphers = "ECDHE+AESGCM" #The ciphers to use for the SSL connection.

asyncio.run(serve(app, config))