# DevOps Project

## Objective

Objectives file :
[objectives](../Subject_project/2024-ST2DCD-PROJECT.docx)

## Installation

### Configuration

Start VM (before doing that, if you have a good compute power, you can increase the amount of memory allocated in the Vagrantfile because the VM is laggy)

```bash
cd project
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

- ```SSH_PRIVATE_KEY``` where you will put your EC2 VM's SSH private key, don't forget to set the "Type" in file
- ```DISCORD_WEBHOOK_URL``` where you will put your webhook url

![addvar](../images/steps/gitlabaddvar.png)

Warrning: The SSH key must be in file format in the variables.

![fileformat](../images/steps/gitlabfileformat.png)

Here is the rsa key of the EC2 VM used to deploy the web application, you can find it in the data folder (not anymore)

### EC2 configuration (optionnal)

If you want to run your own app you will need to create an EC2 VM in AWS to deploy the web application. For the project, there is one already configured.

- Create an account if you haven't done so already.
- Go to EC2 and create an instance.
- Choose Ubuntu for the OS.
- Then create the following security key.

![key](../images/key.png)

- Add the following rules to your security group.

![gds](../images/gsp.png)

### Final result

At the end, you will see in your discord server the result of the pipeline.

![discord](../images/discordBot.png)

When your pipeline has finished executing, connect to: 13.39.243.212:5000

***The configuration steps need to be done once since you don't destroy the VM***
