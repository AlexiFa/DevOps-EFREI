# Titre du projet

# Description
Description du projet

# Requirements
Windows:
- Vagrant
- Virtualbox

# Installation
Cloner le projet
```bash
git clone ...
```
Start VM
```bash	
cd nom_du_projet
vagrant up
vagrant ssh
```
Start gitlab and gitlab-runner with docker compose
```bash	
cd /vagrant_data
sudo docker compose up
```
Wait for the gitlab to boot on http://localhost:8080 

Login into gitlab with root and the password given by the following command
```bash
sudo docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```
In the gitlab UI, change the password of the root user and create a new repository for exemple 'test-app'
# Utilisation
Procédure d'utilisation

# Licence
Licence du projet