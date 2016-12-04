from trafaret_config import ConfigError, read_and_validate

from validators import data_schema


def process(data_file):
    try:
        data = read_and_validate(data_file, data_schema)
    except ConfigError as e:
        exit(e.output())
        return
    print(skip_duplicated_ports(data['services']))


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
                collisions.append(('services', service['name'], component['name'], port))
                continue
            unique_ports.add(port)
    return collisions
