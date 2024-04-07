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
```
pip install gunicorn
gunicorn --workers 2 --bind 0.0.0.0:8000 app:app
```

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
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout 10m;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Additional recommended SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;

    # Additional configuration...
}
```

Test nginx configuration for syntax errors.
`sudo nginx -t`
Reload if configuration is error-free.
`sudo systemctl reload nginx`

Let's Encrypt certificates are valid for 90 days. Certbot should automatically set up a cron job or systemd timer for renewing the certificates. You can test automatic renewal with:
`sudo certbot renew --dry-run`

##### Registrar (Cloudfare)
##### DNS (Cloudfare)

