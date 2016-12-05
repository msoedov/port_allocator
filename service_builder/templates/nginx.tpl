events {
    worker_connections  1024;
}

worker_processes  1;

http {
    server {
        listen       80;
        location / {
            try_files $uri $uri/index.html;
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