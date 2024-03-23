import socket
import re 
from typing import Union, List
from common_ports import ports_and_services

def get_open_ports(target: Union[int, str], port_range: List[int], verbose = False):
    open_ports = []
    ip = "" 
    original_target = target

    if isinstance(target, int):
        target = socket.inet_ntoa(target.to_bytes(4, 'big'))
        ip_given = True
    elif isinstance(target, str):
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
            ip_given = True
            try:
                socket.inet_aton(target)
            except socket.error:
                return f"Error: Invalid IP address"
        elif re.match(r'^[a-zA-Z.-]+$', target):
            ip_given = False
            ip = socket.gethostbyname(target)
            try:
                socket.gethostbyname(target)
            except socket.gaierror:
                return f"Error: Invalid hostname"
        else:
            return f"Error: Ambiguous input (neither IP address nor hostname)"


    for port in range(port_range[0], port_range[1]+1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            if s.connect_ex((target, port)) == 0:
                open_ports.append(port)
        finally:
            s.close()

    if verbose:
        if ip_given:
            verbose_output = f"Open ports for {ip}\nPORT     SERVICE"
        else:
            verbose_output = f"Open ports for {original_target} ({ip})\nPORT"
       
        for port in open_ports:
            service_name = ports_and_services.get(port, 'unknown')
            verbose_output += f"\n{port}    {service_name}"
        return verbose_output


    return(open_ports)


