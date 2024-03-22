import socket 
from typing import Union, List

def get_open_ports(target: Union[int, str], port_range: List[int], verbose = False):
    open_ports = []    
    if isinstance(target, int):
        target = socket.inet_ntoa(target.to_bytes(4, 'big'))
    elif isinstance(target, str):
        try:
            ip_adress = socket.gethostbyname(target)
            target = ip_adress
        except socket.error:
            try:
                socket.inet_aton(target)
            except socket.error:
                return f"Error: Invalid hostname"
            except socket.gaierror:
                return f"Error: Invalid hostname"
                
    for port in range(port_range[0], port_range[1]+1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        if s.connect_ex((target, port)) == 0:
            open_ports.append(port)

    return(open_ports)