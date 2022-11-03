# Project Title

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

[Short Design Doc](https://docs.google.com/document/d/1Nc8SLw_fXM4dxmLg6qsIjWm96jjBqoFhLAxrhBgkhpA/edit?usp=sharing)

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

RabbitMQ running with default guest settings  
MongoDB running locally with default settings  

Create an .env file in the root directory, replacing with your own Jira API details:

```
JIRA_API_TOKEN=<API TOKEN>
JIRA_USERNAME=<your email address>
JIRA_SERVER=https://<yourdomain>.atlassian.net/
```

In rabbitmq.conf, add/change:

```
consumer_timeout = 31622400000
```

This ensures that workers don't time out after 30 minutes while waiting to create Jira Issues.

### Installing

Install requirements

```
pip install -r requirements.txt
```

Start a celery worker

```
(from src directory) ~ celery -A mq.master worker --loglevel=INFO      
```

## Usage <a name = "usage"></a>

python start.py generate-issues will generate 100 jira issues
python start.py graph will point your browser to a histogram created using the generated jira issues
