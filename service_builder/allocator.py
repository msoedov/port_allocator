import click
from trafaret_config import ConfigError, read_and_validate

from validators import data_schema
from nginx import nginx_tpl, index_tpl

__all__ = ('process', )

DEST_FILENAME = 'nginx.conf'


def process(data_file, host):
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
    base = data['ports']['base']
    port_ranges = [range(pair[0] + base, pair[1] + base)
                   for pair in data['ports']['available_ranges']]
    ports = sum(map(list, port_ranges), [])
    errs = assign_ports(services=services, ports=ports)
    if errs:
        [click.secho('Port has not been allocated for : {0}:{1}'.format(*er),
                     color='red') for er in errs]

    with open(DEST_FILENAME, 'w') as n:
        n.write(nginx_tpl.render(services=services, host=host))
    with open('index.html', 'w') as n:
        n.write(index_tpl.render(services=services, host=host))
    click.secho('File: {} has been created!'.format(DEST_FILENAME),
                color='green')


def skip_duplicated_ports(services):
    """
    - components:
      - name: Decorticosis
        port: 4
      - name: Adenodermia
        port: 4
    It should return list of duplicated ports
    :param services:
    :return: List of port collision as a list(('services', service_name, component_name, port))
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
      num_ports: 3

    In the resulted spec total number of ports should be: port for A + port for B + service port = 3
    for this provided example.
    :param service:  single entry of services spec
    :return: modified service spec
    >>> rearrange_port({'components': [{'port': 1, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 10}) \
    == {'components': [{'port': 1, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 2}
    True
    >>> rearrange_port({'components': [{'port': 7, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 10}) \
    == {'components': [{'port': 1, 'name': 'Namesake'}], 'name': 'Jumpiness', 'num_ports': 2}
    True
    """
    components = [c for c in service.get('components', []) if 'skip' not in c]
    num_ports = len(components)
    service['components'] = components
    for i, component in enumerate(components):
        component['port'] = i + 1
    service['num_ports'] = num_ports + 1  # 0 port for service
    return service


def assign_ports(services, ports):
    iport = iter(ports)
    errors = []
    for service in services:
        try:
            available_port = next(iport)
        except StopIteration:
            errors.append((service['name'], ''))
            continue
        service['service_port'] = available_port
        for component in service.get('components', []):
            try:
                available_port = next(iport)
            except StopIteration:
                errors.append((service['name'], component['name']))
                continue
            component['port'] = available_port

    return errors
