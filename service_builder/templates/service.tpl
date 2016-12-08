Service: {{ item.name }}
Components:

{% for c in item.components %}
    {{c.name}} serving on http://{{ host }}:{{c.port}}
{% endfor %}
