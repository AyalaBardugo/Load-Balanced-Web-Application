
# Load Balanced Web Application

## Overview

This project deploys a Python web application in Docker containers, utilizing Nginx as a load balancer and MySQL as a database. The application increments a global counter, logs client requests, and uses cookies to enforce session stickiness in the load balancer. Deployment is managed with Docker Compose, and a Bash script enables dynamic scaling of application containers.


## Sequence Diagram
<div align="center">
<img src="https://github.com/user-attachments/assets/a54e4709-0a94-4250-8fa5-d698fff3ee1b" alt="Project Structure" width="800">
</div>


### Structure
<div align="center">
<img src="https://github.com/user-attachments/assets/07ddb57a-268b-4cf1-b8f0-aa3b0efd9127" alt="Project Structure" width="500">
</div>


## The system consists of three main components:

1. `app`: Flask application with Python backend
2. `nginx`: Load balancer configuration
3. `db`: MySQL database setup

<br>

## The diagram demonstrates the system's request handling:

- **Load balancing** with session persistence
- **Database transaction flow**
- **Response handling mechanism**

---

## Quick Start

```bash
# Deploy application
docker-compose up -d

# Scale application
./scale.sh <number_of_replicas>
```

---

## Core Features

- **High Availability**: Load balanced architecture
- **Session Persistence**: Cookie-based sticky sessions (5-minute TTL)
- **Data Persistence**: Transactional database operations
- **Horizontal Scaling**: Dynamic container management

---

## API Specification

| Endpoint         | Method | Description                                 |
|------------------|--------|---------------------------------------------|
| `/`              | GET    | Retrieves server IP and establishes session |
| `/showcount`     | GET    | Retrieves global request counter            |

---

## System Configuration

### Network Configuration

| Service      | Port  | Protocol |
|--------------|-------|----------|
| Nginx        | 80    | HTTP     |
| Application  | 5000  | HTTP     |
| MySQL        | 3306  | TCP      |

### Environment Configuration

```properties
DB_HOST=mysql-db
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=app_db
