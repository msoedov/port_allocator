from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('service_builder', 'templates'))

nginx = env.get_template('nginx.tpl')
