#!/usr/bin/env python3

"""python program to solve the world problems..."""

import os, sys, string, time, logging, argparse

import asyncio
from bleak import BleakScanner

import bleak

import phin
import time
import threading
from mqttlib import mqtt_multi
import paho.mqtt.client as mqtt

class BluetoothScanner(mqtt_multi.MQTT_MultiplexClient, threading.Thread):
  def __init__(self, mp, config):
    threading.Thread.__init__(self, daemon=True)
    mqtt_multi.MQTT_MultiplexClient.__init__(self, mp, config)

  def detection_callback(self, device, advertisement_data):
    props = device.details.get('props')
    manu_data = props.get('ManufacturerData')

    vendorID = None
    manufacturerdata = None

    if manu_data:
      items = list(manu_data.items())
      vendorID, manufacturerdata = items[0]
      manufacturerdata = [x for x in manufacturerdata]
      manufacturerdata.insert(0, vendorID >> 8)
      manufacturerdata.insert(1, vendorID & 0xff)

    if vendorID == 743: ## pHin
      data = phin.decode(manufacturerdata)

      if 1:
        object_id = "%s/%s/%s" % (self.config.mqtt.discovery_prefix, self.config.mqtt.device_class, device.name)
        state = {}
        state['t'] = int(time.time())
        state['name'] = device.name
        state['macaddr'] = device.address
        state['rssi'] = device.rssi
        
        state['sequence'] = data.sequence
        state['orp'] = data.orp
        state['ph'] = data.ph
        state['temperature'] = data.tc
        state['battery'] = data.battery

        self.publish(object_id+"/state", state, retain=True)

  async def scan(self):
    scanner = BleakScanner()
    scanner.register_detection_callback(self.detection_callback)

    await scanner.start()
    await asyncio.sleep(60 * 60.0)
    await scanner.stop()

  def run(self):
    while 1:
      try:
        asyncio.run(self.scan())
      except:
        import traceback
        traceback.print_exc()

      time.sleep(1)
    
    

def start(args, config):
  mqtt_multi.writePID(config)

  mp = mqtt_multi.MQTT_Multiplex(config.mqtt)
  mp.add_client(mqtt_multi.MQTT_MultiplexControlClient(mp, config))

  client = BluetoothScanner(mp, config)
  mp.add_client(client)

  mp.setup()
  
  mp.loop_forever()

def test():
  logging.warn("Testing")

def parse_args(argv):
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=__doc__)

  parser.add_argument("-t", "--test", dest="test_flag", 
                    default=False,
                    action="store_true",
                    help="Run test function")
  parser.add_argument("--log-level", type=str,
                      choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                      help="Desired console log level")
  parser.add_argument("-d", "--debug", dest="log_level", action="store_const",
                      const="DEBUG",
                      help="Activate debugging")
  parser.add_argument("-q", "--quiet", dest="log_level", action="store_const",
                      const="CRITICAL",
                      help="Quite mode")
  #parser.add_argument("files", type=str, nargs='+')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, config):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  logging.basicConfig(format="[%(asctime)s] %(levelname)-8s %(message)s", 
                    datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  start(args, config)

if __name__ == "__main__":
  import config
  main(sys.argv, config.phin)
