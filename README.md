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

```bash
pip install bshsolutions-sdk
```

## Quick Start

### Basic Setup

```python
from bshengine import BshEngine

bsh_services = BshEngine(host='https://your-instance.com')
```

> For full documentation on how to use it visit: [https://docs.bousalih.com/docs/bsh-engine/sdk](https://docs.bousalih.com/docs/bsh-engine/sdk)

