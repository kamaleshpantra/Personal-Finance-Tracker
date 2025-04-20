import logging
import logging.config
from app import create_app

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(host='0.0.0.0', port=5000, debug=False)