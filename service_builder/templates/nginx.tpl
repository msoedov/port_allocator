
{% for item in services %}
  server { # simple reverse-proxy
    listen       {{port}};
    location / {
      return 200 '{{name}}';
    }
  }

{% endfor %}
