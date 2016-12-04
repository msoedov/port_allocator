import trafaret as t

# services:
# - components:
#   - name: Belltopperdom
#     port: 5
#   name: Uncriticised
#   num_ports: 7

services_schema = t.List(t.Dict(components=t.List(t.Dict(name=t.String,
                                                         port=t.Int(gte=1))),
                                name=t.String,
                                num_ports=t.Int(gte=1)))

extact_ports = lambda x: tuple(map(int, x.group(0).split('-')))

data_schema = t.Dict(
    ports=t.Dict(available_ranges=t.List(t.String(regex='\d+\-\d+') >> extact_ports),
                 base=t.Int(gte=1)),
    services=services_schema)
