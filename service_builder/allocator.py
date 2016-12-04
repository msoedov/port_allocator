import click
from trafaret_config import ConfigError, read_and_validate

from validators import data_schema


def process(data_file):
    try:
        data = read_and_validate(data_file, data_schema)
    except ConfigError as e:
        exit(e.output())
        return
    services = data['services']
    collisions = skip_duplicated_ports(services)
    if collisions:
        click.secho('Port collisions:')
        [click.secho('Warning: {0}:{1}.{2} port={3}'.format(*coll),
                     color='red') for coll in collisions]
    services = list(map(rearrange_port, services))


def skip_duplicated_ports(services):
    """
    - components:
      - name: Decorticosis
        port: 4
      - name: Adenodermia
        port: 4
    It should return list of duplicated ports
    :param services:
    :return:
    """
    collisions = []
    for service in services:
        unique_ports = set()
        for component in service.get('components', []):
            port = component['port']
            if port in unique_ports:
                # Mark it to skip for the next steps
                component['skip'] = True
                collisions.append(('services', service['name'], component[
                    'name'], port))
                continue
            unique_ports.add(port)
    return collisions


def rearrange_port(service):
    """
    It visits every component definition
    - components:
      - name: A
        port: 5
      - name: B
        port: 1
      name: Uncriticised
      num_ports: 7

    and transform port definitions to use as less resources as possible

    - components:
      - name: A
        port: 2
      - name: B
        port: 1
      name: Uncriticised
      num_ports: 2

    :param service:
    :return:
    >>> rearrange_port({'components': [{'port': 1, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 10}) \
    == {'components': [{'port': 1, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 1}
    True
    >>> rearrange_port({'components': [{'port': 7, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 10}) \
    == {'components': [{'port': 1, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 1}
    True
    """
    components = [c for c in service.get('components', []) if 'skip' not in c]
    num_ports = len(components)
    service['components'] = components
    for i, component in enumerate(components):
        component['port'] = i + 1
    service['num_ports'] = num_ports
    return service
