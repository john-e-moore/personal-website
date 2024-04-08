# Personal Website
## Overview
I made this project to understand web app deployment and service. The application, hosted on an EC2 instance, uses gunicorn as webserver for a Flask application and nginx as a reverse proxy. I use Cloudfare for both DNS and registrar.

For security, the application is served over https which requires a certificate and some additional nginx configuration. Additionally, nginx and gunicorn are communicating via socket rather than port which also helps with speed. gunicorn is set up to run as a systemd service and enabled to run automatically on server restarts. 

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

To run via gunicorn: 
```
pip install gunicorn
gunicorn --workers 2 --bind 0.0.0.0:8000 app:app
```

## Production
##### Server (EC2)
A t3.micro Ubuntu instance is fine for a low traffic web application. Default settings should be fine, but ensure inbound traffic is allowed on ports 22 (SSH), 80 (HTTP), and 443 (HTTPS). Create a .pem key pair and SSH into your instance. Clone the repository and install dependencies.

##### Webserver (gunicorn)
Running gunicorn as a systemd service (recommended for production). Create a configuration file with the following:
```
sudo vim /etc/systemd/system/personal-website.service
```
```
[Unit]
Description=Gunicorn instance to serve personal-website
After=network.target

[Service]
User=myuser
Group=myuser
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/venv/bin"
ExecStart=/path/to/your/venv/bin/gunicorn --workers 2 --bind unix:personal-website.sock -m 007 app:app --access-logfile /path/to/your/logs/access.log --error-logfile /path/to/your/logs/error.log

[Install]
WantedBy=multi-user.target
```

Ensure the log files are created, and that your app is instantiated in the app's __init__.py. If it is created in a different entrypoint, e.g. wsgi.py, use wsgi:app instead of app:app.


##### Reverse proxy (nginx)
Install nginx.
```
sudo apt-get update
sudo apt-get install nginx
```

Remove default configuration. 
`sudo rm /etc/nginx/sites-enabled/default`

Create and store an SSL/TLS certificate using certbot.
```
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot will automatically create a new configuration that should look something like this:
```
server {
    listen 80;
    server_name johnemoore.me www.johnemoore.me;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name johnemoore.me www.johnemoore.me;

    ssl_certificate /etc/letsencrypt/live/johnemoore.me/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/johnemoore.me/privkey.pem;

    location / {
        proxy_pass http://unix:personal-website.sock;  # Forward requests to Gunicorn socket
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Additional configuration...
}
```

Test nginx configuration for syntax errors.
`sudo nginx -t`
Reload if configuration is error-free.
`sudo systemctl reload nginx`

Let's Encrypt certificates are valid for 90 days. Certbot should automatically set up a cron job or systemd timer for renewing the certificates. You can test automatic renewal with:
`sudo certbot renew --dry-run`

View nginx logs:
`sudo tail -f /var/log/nginx/error.log`

Restart everything to apply changes:
```
sudo systemctl daemon-reload
sudo systemctl restart personal-website
sudo systemctl restart nginx
```

Check journal:
`sudo journalctl -u personal-website`
`sudo journalctl -n 20`

Permissions:
nginx by default is run by user www-data. Add your normal user to the www-data group, and then give access to /home and /home/project. This needs to be done so that both users can access the socket (personal-website.sock)

##### Registrar (Cloudfare)
##### DNS (Cloudfare)

