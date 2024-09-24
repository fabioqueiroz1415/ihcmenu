import socket

def get_server_rote():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    site_url = f"http://{local_ip}:5000"
    return site_url