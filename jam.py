import requests
import json

import json
import datetime
import uuid
from websocket import create_connection
import requests


class JupyterHubAPI:
    def __init__(self, api_key, kernel_id=None):
        self.api_url = "http://localhost:9090/user/e"
        self.headers = {
            "Authorization": f"token {api_key}",
        }
        self.kernel_id = kernel_id

    def create_kernel(self):
        response = requests.post(
            f"{self.api_url}/api/kernels",
            headers=self.headers
        )
        if response.status_code == 201:
            self.kernel_id = response.json()['id']
            return self.kernel_id
        else:
            return response.text

    def install_packages(self, packages):
        if not self.kernel_id:
            return "Kernel not created"

        install_command = f"!pip install {' '.join(packages)}"
        self.execute_code(install_command)

    def send_execute_request(self, code):
        msg_type = 'execute_request'
        content = {'code': code, 'silent': False}
        msg_id = uuid.uuid1().hex
        session_id = uuid.uuid1().hex
        timestamp = datetime.datetime.now().isoformat()

        msg = {
            'header': {
                'msg_id': msg_id,
                'username': 'test',
                'session': session_id,
                'data': timestamp,
                'msg_type': msg_type,
                'version': '5.0'
            },
            'parent_header': {
                'msg_id': msg_id,
                'username': 'test',
                'session': session_id,
                'data': timestamp,
                'msg_type': msg_type,
                'version': '5.0'
            },
            'metadata': {},
            'content': content
        }

        # Convert the message to bytes
        msg_bytes = json.dumps(msg)

        return msg_bytes

    def execute_code(self, code):
        msg = self.send_execute_request(code)

        self.ws_url = f'ws://localhost:9090/user/e/api/kernels/{self.kernel_id}/channels'
        self.ws = create_connection(self.ws_url, header=self.headers)
        self.ws.send(msg)

        msg_type = ''
        while msg_type != 'stream':
            response_msg = json.loads(self.ws.recv())
            msg_type = response_msg.get('msg_type', '')
            if msg_type == 'stream':
                print(response_msg['content']['text'])

    def destroy_kernel(self):
        if not self.kernel_id:
            return "Kernel not created or already destroyed"

        response = requests.delete(
            f"{self.api_url}/api/kernels/{self.kernel_id}",
            headers=self.headers
        )
        if response.status_code == 204:
            self.kernel_id = None
            return "Kernel destroyed"
        else:
            return response.text


# Assume JupyterHubAPI class is already defined as provided earlier.
# Replace 'your_api_key_here' with your actual JupyterHub API key
api_key = ''
kernel_id = "955e9cc0-c9aa-4f96-a3b4-5c5f179d85c2"
jupyter_hub_api = JupyterHubAPI(api_key, kernel_id=kernel_id)

# # Create a new kernel
# kernel_id = jupyter_hub_api.create_kernel()

# print(kernel_id)

# Install packages
# Replace with desired packages
# packages_to_install = ['requests', 'numpy']
# install_response = jupyter_hub_api.install_packages(packages_to_install)
# print(f"Package Installation Response: {install_response}")

# Execute Python code
python_code = """
print('Hello Worlddd!')
"""
execute_response = jupyter_hub_api.execute_code(python_code)
# print(f"Code Execution Response: {execute_response}")

# Destroy the kernel
# destroy_response = jupyter_hub_api.destroy_kernel()
# print(f"Kernel Destruction Response: {destroy_response}")
