# phinBridge - BLE to MQTT bridge

phinBridge is a simple BLE to MQTT bridge written in Python. I run it on a Raspberry Pi Zero near the pool encased in a outdoor rated enclosure. It reads from the pHin every 10 minutes and then publishes the data to my MQTT broker.

In order to setup the bridge, copy the sample_config.py to config.py. You should change the 'broker' to be the ip address or DNS name of your MQTT broker, as well as, the username and password to access the broker.

Just run mqtt_phin.py and it should find all of the pHin in the area and publish them to the broker.

Enjoy.

