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

data_schema = t.Dict(
    ports=t.Dict(available_ranges=t.List(t.String(regex='\d+\-\d+')),
                 base=t.Int(gte=1)),
    services=services_schema)
