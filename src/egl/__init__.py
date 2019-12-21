import os
from pycarbon import Configuration

project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
if os.environ.get('PROJECT_ROOT', None) is None:
    os.environ['PROJECT_ROOT'] = project_root

config_dir = os.path.join(project_root, 'config')
if os.environ.get('CONFIG_DIR', None) is None:
    os.environ['CONFIG_DIR'] = config_dir

config = Configuration()
