import requests
import json

import json
import datetime
import uuid
from websocket import create_connection
import requests


class JupyterHubAPI:
    def __init__(self, base_url='http://localhost:8888', base_ws_url='ws://localhost:8888'):
        self.base_url = base_url
        self.base_ws_url = base_ws_url
        self.kernel_id = None

    def create_kernel(self):
        response = requests.post(f"{self.base_url}/api/kernels",)
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

        self.ws_url = f'{self.base_ws_url}/api/kernels/{self.kernel_id}/channels'
        self.ws = create_connection(self.ws_url)
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
            f"{self.base_url}/api/kernels/{self.kernel_id}"
        )
        if response.status_code == 204:
            self.kernel_id = None
            return "Kernel destroyed"
        else:
            return response.text


# Assume JupyterHubAPI class is already defined as provided earlier.
# Replace 'your_api_key_here' with your actual JupyterHub API key
jupyter_hub_api = JupyterHubAPI()

# Create a new kernel
kernel_id = jupyter_hub_api.create_kernel()

print(kernel_id)

# Install packages
# Replace with desired packages
packages_to_install = ['requests', 'numpy', 'PyPDF2', 'pytesseract']
install_response = jupyter_hub_api.install_packages(packages_to_install)
print(f"Package Installation Response: {install_response}")

# Execute Python code
python_code = """
print('Hello!')
"""
execute_response = jupyter_hub_api.execute_code(python_code)
# print(f"Code Execution Response: {execute_response}")

# # Destroy the kernel
# destroy_response = jupyter_hub_api.destroy_kernel()
# print(f"Kernel Destruction Response: {destroy_response}")
