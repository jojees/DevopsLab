# kubernetes
Kubernetes Archive


## Ansible
Pending Items:
1. authbind

## Setup and Installation of the workstation development node
1. Install following packages:
    - pyenv
    - poetry
1. Install ansible and other code packages required by this project.<br>
Setup local environment:<br>
        `pyenv install 3.11.5`<br>
        `pyenv virtualenv-create devops-tools`<br>
        `pyenv activate devops-tools`<br>
        `poetry install`<br>
1. Check connectivity with the homelab server:<br>
`ansible-inventory --graph -i ansible/environments/01-homelab.yaml`<br>
`ansible -i ansible/environments/01-homelab.yaml all -m ping`
1. Setup the workstation node using the following command:<br>
`ansible-playbook -i ansible/environments/01-homelab.yaml ansible/playbooks/homelab.yaml`
