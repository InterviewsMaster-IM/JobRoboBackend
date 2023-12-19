# JobRoboBackend Installation Guide

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Redis server

## Installation Instructions

### Clone the Repository

```bash
git clone https://github.com/InterviewsMaster-IM/JobRoboBackend.git
cd JobRoboBackend
```

### Setup a Virtual Environment
```bash
sudo apt-get install virtualenv #install virtual env on ubuntu if not there
virtualenv venv
source venv/bin/activate 
```

### Install Required Packages
```
pip install -r requirements.txt
```


### Environment Variables

Set the following environment variables:

- AWS_ACCESS_KEY_ID=your_aws_access_key_id
- AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
- OPEN_AI_KEY=your_openai_api_key

```bash
export AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
export AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
export OPEN_AI_KEY=<your_openai_api_key>
```
For setting environment variables in Linux, you can follow this guide: [How to set environment variables in Linux](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).


### Database Setup

Run migrations to create the database schema:

```bash
python manage.py migrate
```

### Celery and Redis

Ensure Redis is running on your machine. Install Redis by following the instructions here: [How to install and configure Redis](https://redis.io/docs/install/install-redis/).

### Start the Celery worker:

```bash
celery -A JobRoboBackend worker -l info
```
Don't close this terminal.

### Run the development server

In a new terminal, activate the virtual environment and then run the following:

```bash
python manage.py runserver
```

### Access the Application

Open your web browser and navigate to http://127.0.0.1:8000/admin/ for the admin console. Login with your superuser credentials.

## Production Notes

- Set `DEBUG = False` in the settings file for production.
- Configure `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` for your domain.