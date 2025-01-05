# DevOps Lab
Environment to practise DevOps tools. Setting up and configuring VM's, using LXC to host various tools & services needed to maintain a production like environment.


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
1. Check if homelab server/cluster is showing up in the inventory:<br>
`ansible-inventory --graph -i ansible/environments/01-lab.yaml`
1. Setup the workstation node using the following command:<br>
`ansible-playbook -i ansible/environments/01-homelab.yaml ansible/playbooks/homelab.yaml`
1. Update the environment by launching the required containers and configure them using the following command:</br>
`ansible-playbook -i ansible/environments/01-lab.yaml ansible/playbooks/lab.yaml`


## Notes for using this repo for development
1. When updating the requirements.txt, make sure to use the following command:
  `poetry export --without-hashes --format=requirements.txt > requirements.txt`
  `poetry export --with dev,test --without-hashes --format=requirements.txt > requirements-dev.txt`


<!-- `ansible -i ansible/environments/01-homelab.yaml all -m ping` -->
