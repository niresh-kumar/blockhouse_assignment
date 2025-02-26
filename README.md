# Blockhouse Assignments Trading API

A FastAPI-based trading API with PostgreSQL backend, deployed on AWS EC2 via Docker Compose and GitHub Actions CI/CD.

## Features
- Create and retrieve trading orders (buy/sell) via REST API.
- Real-time WebSocket updates for new orders.
- PostgreSQL database for persistent storage.
- CI/CD pipeline with tests on PRs and deployment on merge to `main`.

## Prerequisites
- Docker and Docker Compose
- Python 3.9
- GitHub account with secrets (`EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`)
- AWS EC2 instance (Ubuntu)

## Setup Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/blockhouse_assignments.git
   cd blockhouse_assignments
