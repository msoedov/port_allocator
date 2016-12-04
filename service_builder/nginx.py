from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('nginx', 'templates'))

nginx_tpl = env.get_template('nginx.tpl')

__all__ = ('nginx_tpl', )
