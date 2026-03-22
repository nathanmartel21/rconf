# rconf - remote configuration 

My own IAC tool (ansible-like)

`rconf` is an agentless Infrastructure as Code (IaC) tool that connects to servers via SSH to apply configurations idempotently.

## Installation & Usage

To start using `rconf`, it is recommended to set up a Python virtual environment and install the package in editable mode:

```bash
python3 -m venv venv
source venv/bin/activate

# Install rconf in editable mode
pip install -e .
rconf -h
```

## Documentation

The documentation for this project is built and managed with [Zensical](https://zensical.org/)

To build and launch the documentation locally, run the following commands:

```bash
pip install zensical
zensical build
zensical serve

# Documentation is available at http://localhost:8001
```
