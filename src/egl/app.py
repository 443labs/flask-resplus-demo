# #!/usr/bin/env python
import logging

from egl import config
from egl.app_factory import app_factory

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

app = app_factory()


def main():
    host = config.get('FLASK_HOST', '0.0.0.0')
    port = config.get('FLASK_PORT', 5000)
    debug = config.get('FLASK_DEBUG', True)
    use_reloader = config.get('FLASK_USE_RELOADER', True)
    app.run(host=host, port=port, debug=debug, use_debugger=debug, use_reloader=use_reloader)


if __name__ == '__main__':
    main()
