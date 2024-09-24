import sys
import os
#para o import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from generate_qr import generate_qr, get_server_rote
import config as config

generate_qr(f'{get_server_rote()}/m/{config.TABLES_TO_IDS[9]}').show()
