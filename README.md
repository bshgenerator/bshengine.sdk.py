# bshsolutions-sdk

A Python SDK for integrating with [BSH Engine](https://engine.bousalih.com) - a low code backend platform that allows you to create APIs for your application with minimal configuration.

## What is BSH Engine?

[BSH Engine](https://engine.bousalih.com) is a backend tool that enables you to build robust APIs quickly without writing boilerplate code. It provides:

- **Entity Management**: Create, read, update, and delete entities with built-in CRUD operations
- **Search & Filtering**: Advanced search and filtering for your entities
- **Authentication**: User registration, login, and JWT token management
- **File Storage**: Upload and manage images and files
- **Email Services**: Send emails with templates
- **API Key Management**: Secure API key generation and management
- Visit [https://engine.bousalih.com](https://engine.bousalih.com) for more details.

## Installation

### Using pip (global installation)

```bash
pip install bshsolutions-sdk
```

### Development Setup (Recommended)

For development, it's recommended to use a virtual environment to isolate dependencies:

#### Using the setup script (Linux/macOS):

```bash
chmod +x setup_env.sh
./setup_env.sh
```

#### Using the setup script (Windows):

```batch
setup_env.bat
```

#### Manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install package in development mode with dev dependencies
pip install -e ".[dev]"
```

After setup, activate the virtual environment before working on the project:

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## Quick Start

The BSH Engine SDK requires you to provide your own HTTP client function. This makes the library lightweight and allows you to use your preferred HTTP library (requests, httpx, aiohttp, etc.).

```python
from bshengine import BshEngine
import requests

def http_client_fn(params):
    """HTTP client function using requests library"""
    method = params.options.get("method", "GET")
    url = params.path
    headers = params.options.get("headers", {})
    body = params.options.get("body")
    
    # Handle form data
    if params.options.get("request_format") == "form":
        # body should be a dict with "files" and "data" keys
        if isinstance(body, dict):
            files = body.get("files")
            data = body.get("data", {})
            # Remove Content-Type header for multipart/form-data
            headers.pop("Content-Type", None)
            return requests.request(method, url, headers=headers, files=files, data=data)
        return requests.request(method, url, headers=headers, data=body)
    
    # Handle JSON
    json_data = None
    if body and params.options.get("request_format") != "form":
        json_data = body
    
    response = requests.request(method, url, headers=headers, json=json_data)
    # Ensure response has required attributes
    if not hasattr(response, 'ok'):
        response.ok = 200 <= response.status_code < 300
    return response

# Initialize BSH Engine with your HTTP client
bsh_services = BshEngine(
    host='https://your-instance.com',
    client_fn=http_client_fn
)
```

## HTTP Client Requirements

Your HTTP client function must:
- Accept a `BshClientFnParams` object as the only parameter
- Return a response object with the following attributes/methods:
  - `ok`: bool (True for 2xx status codes)
  - `status_code`: int
  - `json()`: method that returns a dict
  - `content`: bytes (for blob responses)
  - `text`: str

### Example with httpx

```python
import requests


def http_client_fn(params) -> requests.Response:
    """Default HTTP client function using requests"""
    method = params.options.get("method", "GET")
    url = params.path
    headers = params.options.get("headers", {})
    body = params.options.get("body")
    
    # Handle form data
    if params.options.get("request_format") == "form":
        # body should be a dict with "files" and "data" keys
        if isinstance(body, dict):
            files = body.get("files")
            data = body.get("data", {})
            # Remove Content-Type header for multipart/form-data
            headers.pop("Content-Type", None)
            return requests.request(method, url, headers=headers, files=files, data=data)
        return requests.request(method, url, headers=headers, data=body)
    
    # Handle JSON
    json_data = None
    if body and params.options.get("request_format") != "form":
        if isinstance(body, dict):
            json_data = body
        else:
            json_data = body
    
    return requests.request(method, url, headers=headers, json=json_data)

bsh_services = BshEngine(host='https://your-instance.com', client_fn=http_client_fn)
```

> For full documentation on how to use it visit: [https://docs.bousalih.com/docs/bsh-engine/sdk](https://docs.bousalih.com/docs/bsh-engine/sdk)
