# DevOps Project

## Objective

Objectives file :
[objectives](../Subject_project/2024-ST2DCD-PROJECT.docx)

## Installation

### Configuration

Start VM

```bash
cd Project
vagrant up
vagrant ssh
```

Start gitlab and gitlab-runner with docker compose

```bash
cd /vagrant_data
sudo docker compose up
```

Wait for the gitlab to boot on <http://localhost:8080/>

Login into gitlab with ```root``` and the password given by the following command

```bash
sudo docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```

In the gitlab UI, change the password of the root user

Clone the gitlab project on the VM vagrant, or clone it on your laptop and put it in the share folder between your laptop and the vagrant VM :

```bash
git clone https://github.com/benc-uk/python-demoapp.git
```

Return to your vagrant VM and create a docker network "gitlab_default" :

```bash
docker network create gitlab_default
```

Then in the /etc/hosts file add the line: "10.0.2.15 gitlab.example.com".

```bash
sudo nano /etc/hosts
```

### Runners creation

Afterwards, create the following three runners:

```bash
sudo docker exec -it gitlab-runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.example.com \
  --registration-token {token} \
  --tag-list "pythonapp" \
  --executor docker \
  --docker-image python:3.9-slim-buster \
  --docker-network-mode gitlab_default
```

```bash
sudo docker exec -it gitlab-runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.example.com \
  --registration-token {token} \
  --tag-list "dockerapp" \
  --executor docker \
  --docker-image docker:26.1 \
  --docker-network-mode gitlab_default \
  --docker-privileged true \
  --docker-volumes "/certs/client"
```

```bash
sudo docker exec -it gitlab-runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.example.com \
  --registration-token {token} \
  --tag-list "shellapp" \
  --executor shell \
  --docker-network-mode gitlab_default
```

Replace {token} with your own runner token. To find it, go to 'Admin area', then click on 'Instance runner', click on the three dots, and copy your token.

### EC2 configuration

You will need to create an EC2 VM in AWS to deploy the web application.

- Create an account if you haven't done so already.
- Go to EC2 and create an instance.
- Choose Ubuntu for the OS.
- Then create the following security key.

![key](../images/key.png)

- Add the following rules to your security group.

![gds](../images/gsp.png)

### Setup variables

Then in your GitLab, you will need to go to the settings of your CI/CD, then into 'Variables', and add the following variables:

- ```REGISTRY_PASS``` where you will put your Docker Hub password
- ```REGISTRY_USER``` where you will put your Docker Hub username
- ```SSH_PRIVATE_KEY``` where you will put your EC2 VM's SSH private key

### Setup .gitlab-ci.yml

Finally, go to your GitLab project and create a .gitlab-ci.yml file. Add the following content to it, replace {public DNS} with the public DNS of your EC2 and replace {IMAGE_NAME} with your own image name, for example "julesdavoust/devops_project" :

```bash
touch /vagrant_data/python-demoapp/.gitlab-ci.yml
nano /vagrant_data/python-demoapp/.gitlab-ci.yml
```

```yml
variables:
    IMAGE_NAME: $REGISTRY_USER/devops-project
    IMAGE_TAG: pythonapp-1.1

stages:
    - test
    - build
    - deploy

run_test:
    stage: test
    tags:
        - pythonapp
    before_script:
        - apt-get update && apt-get install -y make
    script:
        - make test

build_image:
    stage: build
    services:
        - name: docker:26.1-dind
          alias: docker
    tags:
        - dockerapp
    variables:
        DOCKER_HOST: tcp://docker:2375
        DOCKER_TLS_CERTDIR: ""
    before_script:
        - docker info
        - echo "$REGISTRY_PASS" | docker login --username "$REGISTRY_USER" --password-stdin
    script:
        - cd build
        - docker build . -t $IMAGE_NAME:$IMAGE_TAG
        - docker push $IMAGE_NAME:$IMAGE_TAG

deploy:
    stage: deploy
    tags:
        - shellapp
    script:
        - cp "-----BEGIN RSA PRIVATE KEY-----MIIEowIBAAKCAQEAo3VpQuff/frwmxqebP6YZHS3HlCy/RsouYbklSmRMmPwqeEK+j/J03dmsYZIskRsKsEQgTUuK+6X4Wpm+hKoNRruWtzC2VUoyaJRKqlxPX7pA0J2mqNeNzFTFfKCgYECF8Y6IWLutDERHKjaTAtUWnd/EKxyVzFvBq20vsbGVnwEXy9YfvDZLUTlNE4S7uhq0wYmyPa1n25IWfYGw0be3NKXRjYbc2bT6nzwXluHPGIqB9DViPU/t2NkpRxgwch226ybsb+DpfhkmpXH+q0XuQKZzjKxsQLg0U0Brh2VX5qSFsFiX3EEYSMeVv2jpYFbdgM+EGhYXAGbCz4xvu+nAQIDAQABAoIBAHGF/dEl0X9HZQuT9SultpkuJm+7hFQdJK+Va/PcpqbkmiSh00nyO23Oo1fv91U4CBe5dokGMkb4siswBszvYDthtOEOKZVfe7BuNwj2HVukZJiK9Gx5wdl7PEUl5FWlD5sLZRwC5d3npgbNjq75v2AFVg5ydgbwojd1NO66hs1QwGERVVnfIkcxJ3x7V81XD8BtfQhdPHfn9Ij6+vUwlQow+sZfIHyhlSX4e+LeAqIZPeHUXRkskhU/1S2h1u5GJOWz+aFl671oAHVDe3uEQeR6Q1ThCG8LlrzSzvg0iJB1X5cz+kGSUQc6K0S1+6mVe3C55bk//59h+4iFeZORtQECgYEAzlNcJTeGjn/bEp9yAfQJwt+Zb72likNpKTO8oX5dgV0KPkrNudzNpZLAdzkfahiZ6WzFB39sFfo8oTzpCI26AuI/KjzZ7MSS1UZQ0mG10/HvnGA0iaW+mut7xI+Vqm71vuR+w9Eb/PpFkvcs+RHpD8MNXqwspbJG3E2Io7sdBckCgYEAys/+ih/FkEWXGFwa1T66lhc2GuxNeZ9DTXGvDuwpRLDzcpDCLOw8Kn+Gd/Tr/dKREN755x0IJMG1KMufdvq6AHM5ej7WcS2keaJnYGBuUGUHYd0bN0ZBVpxxq5DBAyRPVXoB6HltvTf2Y+W2s7aG94AtBd4Av9PbwVBuyb16E3kCgYEAxTiPiw+xckMq8Hky7EUOk5VSwKoCM9DOE9FdjO0SilaaNQMh9Xjnpk5J5WzX532Omb8b81fMxJFHJUTo6AE5fgowILq8AQPB61XkacV2nhrUVKDtd2nUcZeI3lH12U1pYEhgF+Opoj7FBH97ILYLFsL247kmkFiCPZFrfD6etmkCgYAlE6M4AxjuCBrYRDZPl7kqqTGl+F8thdUa+laDht8AhMzsu9QTvFg/eLLPiUH/VBhbGjhbbO5JMfR5cchESw/n9yih1Y0EgdCYv/zgHKDuJ5oS5QYNs9VMDSumrr7qYR/zw2tH4bMTLYDowF0HO64u3wrcELrYVtXM4HRwgygnGQKBgA7Oz0uzE0tqS9iVUnrof1ECknaTPlQCfx2JEAUo52FhAekv8LFLGOxh3QntmEcYEiBjtyAJ65F/nV0dttgSLhcP6Y1SUU5TKN23DqQkWn/c9ZzYyKrQh82RvUe7I/CYmT9yn3zV3hWBpgvblV762koEmaQ7i29UPNHUd4KLuma1-----END RSA PRIVATE KEY-----" ~/.ssh/id_rsa 
        - chmod 600 ~/.ssh/id_rsa
        - ssh-keyscan -H ec2-13-39-243-212.eu-west-3.compute.amazonaws.com >> ~/.ssh/known_hosts
        - chmod 644 ~/.ssh/known_hosts
        - ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa ubuntu@ec2-13-39-243-212.eu-west-3.compute.amazonaws.com "
          sudo apt-get update &&
          sudo apt-get install -y docker.io &&
          sudo echo $REGISTRY_USER && echo $REGISTRY_PASS &&
          echo $REGISTRY_PASS | sudo docker login -u $REGISTRY_USER --password-stdin &&
          sudo docker ps -aq | xargs -r sudo docker stop &&
          sudo docker ps -aq | xargs -r sudo docker rm &&
          sudo docker run -d -p 5000:5000 $IMAGE_NAME:$IMAGE_TAG"
```

modify requirements.txt

```bash
sudo nano /vagrant_data/python-demoapp/src/requirements.txt
```

```txt
Flask>=2.2.2
py-cpuinfo==7.0.0
psutil==5.8.0
gunicorn==20.1.0
black==20.8b1
flake8==3.9.0
pytest==6.2.2
jinja2<3.1.0
```

move the docker file to /

```bash
sudo mv /vagrant_data/python-demoapp/build/Dockerfile /vagrant_data/python-demoapp/
```

then push this into the repo

```bash
cd /vagrant_data/python-demoapp
git remote set-url origin http://gitlab.example.com/root/devops_project.git
git push --all origin
```

When your pipeline has finished executing, connect to: 13.39.243.212:5000

***The configuration steps need to be done once since you don't destroy the VM***
