# DevOps Lab
Environment to practise DevOps tools. Setting up and configuring containers to host various tools & services needed to maintain a production like environment.

## Requirements:
1. Infrastructure requirements:
   1. Node capable of hosting few containers using "Docker Desktop".
   2. Prefarably a MacBook.

2. Following software packages are needed:
   1. Python-3.12
   2. Poetry
   3. Docker Desktop

## Installation and provisioning of the lab environment
1. Check out this repository and 'cd' to the checkedout directory.
1. Install required packages by this project using poetry.<br>
        `poetry install`<br>
2.  Launch lab environment using the following command:<br>
        `ansible-playbook -i localhost ansible/playbooks/lab.yaml`

## Terminate the lab environment
Use the below command to terminate the lab environment:<br>
`ansible-playbook -i localhost ansible/playbooks/lab.yaml -t terminate-lab`


## Notes for using this repo for development
1. When updating the requirements.txt, make sure to use the following command:<br>
   1. For requirements.txt:<br>
  `poetry export --without-hashes --format=requirements.txt > requirements.txt`<br>
   1. For dev-requirements.txt:<br>
  `poetry export --with dev,test --without-hashes --format=requirements.txt > requirements-dev.txt`<br>


<!-- `ansible -i ansible/environments/01-homelab.yaml all -m ping` -->
