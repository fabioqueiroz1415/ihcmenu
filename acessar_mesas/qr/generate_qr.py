import qrcode
import socket
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config as config

def generate_qr(s = "/"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2
    )
    qr.add_data(s)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def get_server_rote():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    site_url = f"http://{local_ip}:5000"
    return site_url