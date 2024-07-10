import subprocess as sp
import shlex
import time

res = sp.check_output(shlex.split(f'sudo docker exec -it gitlab grep "Password:" /etc/gitlab/initial_root_password')).decode('utf-8').split(' ')[1].rstrip()
print(f"#\n#\n#\n#\t\t\tWait for the gitlab to boot at localhost:8080 (it may takes a while)\n# \
      \n#\t\t\tYou can connect to localhost:8080 with the following credentials\n#\n#\t\t\tUsername: root\n#\t\t\tPassword: {res}\n#\n#")

print("\nGo to admin area (bottom left) \n-> CI/CD (left menu)\n-> Runners \n-> Click on the 3 dots next to 'new instance runner' (Top right) \n-> copy the registration token")

# ask for the token
token = input('\nEnter the registration token: ')

out = sp.check_output(shlex.split(f'sudo docker exec -it gitlab-runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.example.com \
  --registration-token {token} \
  --tag-list "pythonapp" \
  --executor docker \
  --docker-image python:3.9-slim-buster \
  --docker-network-mode gitlab_default'))

print('Runner registered') if 'Registering runner... succeeded' in out.decode('utf-8') else print('Failed to register runner')

out = sp.check_output(shlex.split(f'sudo docker exec -it gitlab-runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.example.com \
  --registration-token {token} \
  --tag-list "dockerapp" \
  --executor docker \
  --docker-image docker:26.1 \
  --docker-network-mode gitlab_default \
  --docker-privileged true \
  --docker-volumes "/certs/client"'))

print('Runner registered') if 'Registering runner... succeeded' in out.decode('utf-8') else print('Failed to register runner')

out = sp.check_output(shlex.split(f'sudo docker exec -it gitlab-runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.example.com \
  --registration-token {token} \
  --tag-list "shellapp" \
  --executor shell \
  --docker-network-mode gitlab_default'))

print('Runner registered') if 'Registering runner... succeeded' in out.decode('utf-8') else print('Failed to register runner')

sp.run(shlex.split(f'git remote set-url origin http://gitlab.example.com/root/devops_project.git'), cwd='/vagrant_data/python-demoapp')

print('\n\nClick on the user profile (top left) -> edit profile -> emails -> copy the email address of the root user\n\n')

email = input('Enter the email address for the gitlab root user: ')

print('config email for git')
sp.run(shlex.split(f'git config --global user.email "{email}"'), cwd='/vagrant_data/python-demoapp')

print('config name for git')
sp.run(shlex.split(f'git config --global user.name "Adminitrator"'), cwd='/vagrant_data/python-demoapp')

print(f"\nRemider of the gitlab root password: {res}\n")

print('push files into gitlab')
sp.run(shlex.split(f'git push --all origin'), cwd='/vagrant_data/python-demoapp') # login and password

sp.run(shlex.split(f'cp /vagrant_data/.gitlab-ci.yml /vagrant_data/python-demoapp/.gitlab-ci.yml'), cwd='/vagrant_data/python-demoapp')

print('\nSetup varibles')
print('got to your new project -> settings -> CI CD settings -> variables')
print('add the following variables:')
print('\nSSH_PRIVATE_KEY: go to the readme and copy the private key')
print('DISCORD_WEBHOOK: the webhook url for the discord channel that you copied before')
input('\nPress enter when you are done')

print('add new files')
sp.run(shlex.split(f'git add .'), cwd='/vagrant_data/python-demoapp')
time.sleep(1)

print('commit files')
sp.run(shlex.split(f'git commit -a -m "pipeline"'), cwd='/vagrant_data/python-demoapp')
time.sleep(3)

print(f"\nRemider of the gitlab root password: {res}\n")

print('push pipeline')
sp.run(shlex.split(f'git push'), cwd='/vagrant_data/python-demoapp') # login and password

print('\nYou can now access the gitlab at http://localhost:8080 to see the pipeline in action')