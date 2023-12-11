# kubernetes
Kubernetes Archive


## Ansible
Pending Items:
1. authbind

## Setup and installation of the lab environment
1. Install following packages:
    - pyenv
    - poetry
1. Install ansible and other code packages required by this project.<br>
Setup local environment:<br>
        `pyenv install 3.11.5`<br>
        `pyenv virtualenv-create devops-tools`<br>
        `pyenv activate devops-tools`<br>
        `poetry install`<br>
        `cp ansible/vars/lab_servers.yaml.sample ansible/vars/lab_servers.yaml`
1. Update the lab server IP address in the file:
    > ansible/environments/01-homelab.yaml
1. Enable Wake-On-Boot for the lab server. <br>
    Update the MAC address of the lab server in the file:
    > ansible/vars/lab_servers.yaml
1. Check if homelab server is showing up in the inventory:<br>
`ansible-inventory --graph -i ansible/environments/01-homelab.yaml`
1. Setup the workstation node using the following command:<br>
`ansible-playbook -i ansible/environments/01-homelab.yaml ansible/playbooks/homelab.yaml`




<!-- `ansible -i ansible/environments/01-homelab.yaml all -m ping` -->
