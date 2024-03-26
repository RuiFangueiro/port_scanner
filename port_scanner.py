import socket
import re 
from typing import Union, List
from common_ports import ports_and_services

def get_open_ports(target: Union[int, str], port_range: List[int], verbose = False):
    open_ports = []
    ip = ""
    ip_given = False 
    original_target = target
    resolved_hostname = ""

    if isinstance(target, int):
        target = socket.inet_ntoa(target.to_bytes(4, 'big'))
        ip_given = True
    elif isinstance(target, str):
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
            try:
                ip = socket.gethostbyname(target)
                ip_given = True
                try:
                    resolved_hostnames = socket.gethostbyaddr(ip)[0]
                    if isinstance(resolved_hostnames, list):
                        resolved_hostname = resolved_hostnames[0]
                    else:
                        resolved_hostname = resolved_hostnames
                except socket.herror:
                        resolved_hostname = ""
            except socket.error:
                return f"Error: Invalid IP address"
        elif re.match(r'^[a-zA-Z.-]+$', target):
            try:
                ip_given = False
                ip = socket.gethostbyname(target)
            except:
                ip= ""
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
        if ip_given and resolved_hostname:
            verbose_output = f"Open ports for {resolved_hostname} ({ip})\nPORT     SERVICE"
        elif ip_given:
            verbose_output = f"Open ports for {ip}\nPORT     SERVICE"
        else:
            verbose_output = f"Open ports for {original_target} ({ip})\nPORT     SERVICE"
       
        for port in open_ports:
            service_name = ports_and_services.get(port, 'unknown')
            verbose_output += f"\n{port:<9}{service_name}"
        return verbose_output


    return(open_ports)


