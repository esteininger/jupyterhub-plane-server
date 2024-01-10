# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    nodejs \
    npm \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install configurable-http-proxy
RUN npm install -g configurable-http-proxy

# Upgrade pip
RUN pip install --upgrade pip

# Install JupyterHub, notebook, and dummy authenticator
RUN pip install jupyterhub notebook jupyterhub-dummyauthenticator

# Create a user to avoid running as root
RUN useradd -ms /bin/bash jupyteruser

# Create directory for configuration file
RUN mkdir -p /etc/jupyterhub && \
    chown -R jupyteruser:jupyteruser /etc/jupyterhub

# Copy jupyterhub configuration to the specified location
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

# Change ownership of the configuration file to the non-root user
RUN chown jupyteruser:jupyteruser /etc/jupyterhub/jupyterhub_config.py

# Change ownership of the work directory to the non-root user
RUN chown -R jupyteruser:jupyteruser /usr/src/app

# Expose the port JupyterHub will run on
EXPOSE 9090

# Set the command to run JupyterHub with the specified config file
CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
