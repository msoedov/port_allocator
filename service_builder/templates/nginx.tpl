events {
    worker_connections  1024;
}

worker_processes  1;

http {
    server {
        listen       80;
        root /usr/share/nginx/html;
        index index.html index.htm;

        # Make site accessible from http://localhost/
        server_name localhost;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ /index.html;
                # Uncomment to enable naxsi on this location
                # include /etc/nginx/naxsi.rules
        }
    }

{% for item in services %}
    server {
        listen       {{ item.service_port }};
        location / {
            return 200 '{% include "service.tpl" ignore missing %}';
        }
    }
    {% for c in item.components %}
            server {
                listen       {{ c.port }};
                location / {
                    return 200 '{% include "component.tpl" ignore missing %}';
                }
            }
    {% endfor %}

{% endfor %}
}