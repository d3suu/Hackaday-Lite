# Hackaday-Lite
Flask-bs4 proxy for lightweight Hackaday reader

## Why
My mobile internet sucks, but I want to read hackaday. This proxy makes absolute basic html from articles and /blog pages. For comparison, [this article](https://hackaday.com/2020/03/04/raising-the-titanics-radio-room/) needs to download 1.7MB of data, while on my proxy it's only 79.30kB. With internet speed in <0.1Mb/s range, it works pretty well.

## Support Hackaday
I guess most of their income comes from ad revenue. When not reading with proxy, read with standard website.

## Hosting
I host this project on minimal VPS server, 1GB of RAM, 20GB of HDD, behind nginx, with absolute simplest configuration (also not really safe for production).
 - python3 virtual environment for sanity
 - app.py with flask in development mode (http port 5000)
 - nginx proxy_pass on hackaday.yourdomain:80
```
# Virtualenv
virtualenv -p $(which python3) hackaday
cd hackaday && source bin/activate
pip3 install flask bs4 lxml

# Flask
export FLASK_RUN=app
export FLASK_ENV=development
flask run

# Nginx: /etc/nginx/sites-enabled/default
server {
        listen 80;
        server_name hackaday.yourdomain;
        location / {
                proxy_pass http://127.0.0.1:5000/;
        }
}
```

## Docker image
```
docker build -t hackaday-lite .
docker run -d -p 127.0.0.1:5000:5000/tcp --restart unless-stopped hackaday-lite
```

