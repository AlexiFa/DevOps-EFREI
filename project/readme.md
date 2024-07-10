# DevOps Project

## Objective

Objectives file :
[objectives](../Subject_project/2024-ST2DCD-PROJECT.docx)

## Installation

### Configuration

Start VM (before doing that, if you have a good compute power, you can increase the amount of memory allocated in the Vagrantfile because the VM is laggy)

```bash
cd Project
vagrant up # up to 20 minutes (on my computer)
vagrant ssh
```

The VM will do some configurations for you so you can go take a coffee and come back in a few minutes.

Wait for the gitlab to boot on <http://localhost:8080/> (it may take a few minutesn up to 10 minutes on my computer) (if it takes too much time and you have a good compute power, you can increase the resources allocated to the VM in the Vagrantfile)

### Setup Discord

To be notify either when your pipeline is well executed or when it crashed, you have to setup a webhook in a discord server. So go in your discord server then go in the server setting, click on "Integration" then create and configure your new webhook and copy its webhook url (keep it somewhere).

### Setup script

Start the setup script that will register the runners, create the project in gitlab and push the code to trigger the pipeline. Follow its intructions.

```bash
python3 /vagrant_data/setup.py
```

#### Script instructions (you can follow them in the console prompt)

Login into gitlab with ```root``` and the password given by the script.

Go to the 'Admin area -> CI/CD -> Runners' and copy the token.

![token](../images/steps/gitlabtoken.png)

Go to the admin profile (Click on your profile picture -> edit profile -> emails) and copy the email into the setup prompt given by the script.

![email](../images/steps/gitlabcopyemail.png)

#### Setup variables

You will have a message that says that you need to setup some variables in your GitLab.

Before continuing the setup script that will trigger the pipeline, in your GitLab, you will need to go to the settings of your CI/CD, then into 'Variables', and add the following variables:

- ```SSH_PRIVATE_KEY``` where you will put your EC2 VM's SSH private key
- ```DISCORD_WEBHOOK_URL``` where you will put your webhook url

![addvar](../images/steps/gitlabaddvar.png)

Warrning: The SSH key must be in file format in the variables.

![fileformat](../images/steps/gitlabfileformat.png)

Here is the rsa key of the EC2 VM used to deploy the web application

```text
-----BEGIN RSA PRIVATE KEY-----MIIEowIBAAKCAQEAo3VpQuff/frwmxqebP6YZHS3HlCy/RsouYbklSmRMmPwqeEK+j/J03dmsYZIskRsKsEQgTUuK+6X4Wpm+hKoNRruWtzC2VUoyaJRKqlxPX7pA0J2mqNeNzFTFfKCgYECF8Y6IWLutDERHKjaTAtUWnd/EKxyVzFvBq20vsbGVnwEXy9YfvDZLUTlNE4S7uhq0wYmyPa1n25IWfYGw0be3NKXRjYbc2bT6nzwXluHPGIqB9DViPU/t2NkpRxgwch226ybsb+DpfhkmpXH+q0XuQKZzjKxsQLg0U0Brh2VX5qSFsFiX3EEYSMeVv2jpYFbdgM+EGhYXAGbCz4xvu+nAQIDAQABAoIBAHGF/dEl0X9HZQuT9SultpkuJm+7hFQdJK+Va/PcpqbkmiSh00nyO23Oo1fv91U4CBe5dokGMkb4siswBszvYDthtOEOKZVfe7BuNwj2HVukZJiK9Gx5wdl7PEUl5FWlD5sLZRwC5d3npgbNjq75v2AFVg5ydgbwojd1NO66hs1QwGERVVnfIkcxJ3x7V81XD8BtfQhdPHfn9Ij6+vUwlQow+sZfIHyhlSX4e+LeAqIZPeHUXRkskhU/1S2h1u5GJOWz+aFl671oAHVDe3uEQeR6Q1ThCG8LlrzSzvg0iJB1X5cz+kGSUQc6K0S1+6mVe3C55bk//59h+4iFeZORtQECgYEAzlNcJTeGjn/bEp9yAfQJwt+Zb72likNpKTO8oX5dgV0KPkrNudzNpZLAdzkfahiZ6WzFB39sFfo8oTzpCI26AuI/KjzZ7MSS1UZQ0mG10/HvnGA0iaW+mut7xI+Vqm71vuR+w9Eb/PpFkvcs+RHpD8MNXqwspbJG3E2Io7sdBckCgYEAys/+ih/FkEWXGFwa1T66lhc2GuxNeZ9DTXGvDuwpRLDzcpDCLOw8Kn+Gd/Tr/dKREN755x0IJMG1KMufdvq6AHM5ej7WcS2keaJnYGBuUGUHYd0bN0ZBVpxxq5DBAyRPVXoB6HltvTf2Y+W2s7aG94AtBd4Av9PbwVBuyb16E3kCgYEAxTiPiw+xckMq8Hky7EUOk5VSwKoCM9DOE9FdjO0SilaaNQMh9Xjnpk5J5WzX532Omb8b81fMxJFHJUTo6AE5fgowILq8AQPB61XkacV2nhrUVKDtd2nUcZeI3lH12U1pYEhgF+Opoj7FBH97ILYLFsL247kmkFiCPZFrfD6etmkCgYAlE6M4AxjuCBrYRDZPl7kqqTGl+F8thdUa+laDht8AhMzsu9QTvFg/eLLPiUH/VBhbGjhbbO5JMfR5cchESw/n9yih1Y0EgdCYv/zgHKDuJ5oS5QYNs9VMDSumrr7qYR/zw2tH4bMTLYDowF0HO64u3wrcELrYVtXM4HRwgygnGQKBgA7Oz0uzE0tqS9iVUnrof1ECknaTPlQCfx2JEAUo52FhAekv8LFLGOxh3QntmEcYEiBjtyAJ65F/nV0dttgSLhcP6Y1SUU5TKN23DqQkWn/c9ZzYyKrQh82RvUe7I/CYmT9yn3zV3hWBpgvblV762koEmaQ7i29UPNHUd4KLuma1-----END RSA PRIVATE KEY-----
```

### EC2 configuration (optionnal)

I fyou want to run your own app you will need to create an EC2 VM in AWS to deploy the web application. For the project, there is one already configured.

- Create an account if you haven't done so already.
- Go to EC2 and create an instance.
- Choose Ubuntu for the OS.
- Then create the following security key.

![key](../images/key.png)

- Add the following rules to your security group.

![gds](../images/gsp.png)

### Final result

When your pipeline has finished executing, connect to: 13.39.243.212:5000

***The configuration steps need to be done once since you don't destroy the VM***
