Service: {{ item.name }}
Components:

{% for c in item.components %}
    {{c.name}} serving on http://127.0.0.1:{{c.port}}
{% endfor %}