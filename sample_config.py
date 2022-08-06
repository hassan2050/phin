class site_mqtt:
  broker = "ip address"
  brokerPort = 9001
  discovery_prefix = "homeassistant"

class phin:
  class mqtt(site_mqtt):
    username = "phin" 
    password = "password"
    
    device_class = "sensor"
    object = "phin"

    object_id = "%s/%s/%s" % (site_mqtt.discovery_prefix, device_class, object)

