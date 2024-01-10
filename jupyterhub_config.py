import os
from subprocess import check_call, CalledProcessError

c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
# c.JupyterHub.disable_check_xsrf = True

c.JupyterHub.ip = '0.0.0.0'  # listen on all IPs
c.JupyterHub.token = ''     # disable authentication
c.JupyterHub.allow_origin = '*'  # allow access from anywhere
c.JupyterHub.disable_check_xsrf = True  # allow cross-site requests


# c.JupyterHub.services = [
#     {
#         "name": "my-service",
#         "api_token": "30c2eca99a6d40f1a129c5f8a9d13aa6",
#     }
# ]


def pre_spawn_hook(spawner):
    username = spawner.user.name
    try:
        # Check if user already exists
        if not os.path.exists(f'/home/{username}'):
            check_call(['useradd', '-ms', '/bin/bash', username])
        else:
            print(f"User {username} already exists.")
    except CalledProcessError as e:
        print(f"Error adding user {username}: {e}")


c.Spawner.pre_spawn_hook = pre_spawn_hook
