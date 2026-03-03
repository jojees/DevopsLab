#!/usr/bin/env python3
import json
import subprocess

def get_containers():
    result = subprocess.run(['lxc', 'list', '--format', 'json'], capture_output=True, text=True)
    containers = json.loads(result.stdout)
    inventory = {"containers": {"hosts": [], "vars": {"ansible_connection": "lxd", "ansible_lxd_remote": "jdevlabcluster"}}}

    for container in containers:  # Adjusted this line to iterate over containers directly
        name = container['name']
        # print(container)
        # Extract the first IPv4 address from eth0
        ip = None
        if 'eth0' in container['state']['network']:
            for address in container['state']['network']['eth0']['addresses']:
                if address['family'] == 'inet':  # Check for IPv4
                    ip = address['address']
                    break  # Exit the loop once the first IPv4 address is found

        if ip:
            inventory["containers"]["hosts"].append(name)
            inventory["containers"][name] = {"ansible_host": name, "container_ip": ip}

    return inventory

if __name__ == "__main__":
    print(json.dumps(get_containers()))

