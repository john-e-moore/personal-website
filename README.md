# Wage Gauge
## Overview
I made this project to understand web app deployment and service. It runs with end-to-end encryption (https) on an EC2 instance, using an nginx reverse proxy plus gunicorn to serve a Flask (Python) application. I use Cloudfare for both DNS and registrar.

Visit the website at [https://johnemoore.me](https://johnemoore.me)

## Development
##### Clone repository
`git clone https://github.com/john-e-moore/personal-website.git`
##### Create and activate virtual environment
```
cd personal-website
python3 -m venv venv
source venv/bin/activate
```
##### Install dependencies
`pip install -r requirements.txt`
##### Setup and run Flask in debug mode
```
export FLASK_ENV=development
export FLASK_APP='/path/to/project'
flask run --debug
```

## Production
##### Server (EC2)
A t3.micro Ubuntu instance is fine for a low traffic web application. Default settings should be fine, but ensure inbound traffic is allowed on ports 22 (SSH), 80 (HTTP), and 443 (HTTPS). Create a .pem key pair and SSH into your instance. Clone the repository and install dependencies.
##### Webserver (gunicorn)
Set environment variables and run gunicorn with workers equal to 2x the number of cores on the server.
##### Reverse proxy (nginx)
##### Registrar (Cloudfare)
##### DNS (Cloudfare)

