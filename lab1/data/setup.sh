# change root password
# echo "user = User.first\nuser.password = 'new_password'\nuser.password_confirmation = 'new_password'\nuser.save!\nexit" | sudo gitlab-rails console -e production