import webbrowser
import sys
import os
from main import get_server_rote

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import config as config

webbrowser.open(f'{get_server_rote()}/m/{config.TABLES_TO_IDS[7]}')

print(f'{get_server_rote()}/m/{config.TABLES_TO_IDS[7]}')