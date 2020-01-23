#!  /usr/local/bin/python3.7
import logging
import sys
from ariskengine import app as application

sys.stdout = sys.stderr
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/arisk-engine/')

application.config.update(
    TESTING=True,
    SECRET_KEY=12345,
    ENV='development',
    DEBUG=True
)
# print(sys.path.insert(0, '/var/www/html/arisk-engine/'))

# secret_key = '12345'
# application.testing=True

# file_handler = RotatingFileHandler(ariskparametri.ariskBaseDir+'/arisk.log', maxBytes=10240,
#                                       backupCount=10)
# file_handler.setFormatter(logging.Formatter(
#        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
# file_handler.setLevel(logging.INFO)
# application.logger.addHandler(file_handler)

# application.logger.setLevel(logging.INFO)
# application.logger.info('Microblog startup')
