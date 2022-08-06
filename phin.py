#!/usr/bin/env python3

"""python program to solve the world problems..."""

import os, sys, string, time, logging, math, argparse
from logging import debug,warning,info,error,fatal,critical; warn=warning

_version = "0.1"

class Reading:
  def __init__(self):
    self.sequence = None
    self.orp = None
    self.ph = None
    self.tk = None
    self.tc = None
    self.tf = None
    self.macaddr = None
    self.battery = None
    
  def __repr__(self):
    s = []
    s.append("sequence: %d" % self.sequence)
    s.append("orp: %d" % self.orp)
    s.append("ph: %.2f" % self.ph)
    s.append("temp: %.1f" % self.tc)
    s.append("battery: %d" % self.battery)
    s.append("macaddr: %s" % self.macaddr)

    return ",".join(s)

def decode(s):
  data = Reading()
  
  data.orp = ((s[8])<<4) | ((s[7] & 0xf0) >> 4)

  data.sequence = s[9]
  
  ## battery
  data.battery = (s[10] | (s[11] & 0x0f) << 8)

  ## PH
  vph = ((s[7] & 0x0f)<<8) | s[6]
  vcommon = (s[12] << 4) | ((s[11] & 0xf0) >> 4)
  vprobe = vph - vcommon
  data.ph = (vprobe - 414.12) / -59.16

  ## temperature
  vp4 = (s[4] << 4 | (s[3] & 0xf0) >> 4)
  vp5 = (s[2] | (s[3] & 0x0f) << 8)
  rntc = 10000. / ((1.0 * vp5 / vp4) - 1.)

  t0 = 298.15
  b = 3950.
  r0 = 10000.
  data.tk = 1.0 / (1./t0 + (1./b) * math.log(rntc / r0))
  data.tc = data.tk - 273.15
  data.tf = (data.tc * 9/5) + 32.

  ## macaddr
  macaddr = reversed(s[14:20])
  data.macaddr = ":".join([("%02x" % x) for x in macaddr])

  return data
  

def decodeMD(s):
  print ([i for i in s])
  print (["%02x" % i for i in s])
  
def start(args):
  s = b'p\xabe\xe3\xc4\x95\x18\x1e\x91\x8b[\x00\x93\xa6\xa3\x10\xd3\xff&E'
  s = [2, 231, 112, 171, 101, 227, 196, 149, 24, 30, 145, 139, 91, 0, 147, 166, 163, 16, 211, 255, 38, 69]

  decodeMD(s)
  data = decode(s)

  print(data)
  
def test():
  logging.warn("Testing")

def parse_args(argv):
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

  parser.add_argument("-t", "--test", dest="test_flag", default=False, action="store_true", help="Run test function")
  parser.add_argument("--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Desired console log level")
  parser.add_argument("-d", "--debug", dest="log_level", action="store_const", const="DEBUG", help="Activate debugging")
  parser.add_argument("-q", "--quiet", dest="log_level", action="store_const", const="CRITICAL", help="Quite mode")
  parser.add_argument("files", type=str, nargs='*')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, stdout, environ):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  logging.basicConfig(format="[%(asctime)s] %(levelname)-6s %(message)s (%(filename)s:%(lineno)d)", 
                      datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  start(args)

if __name__ == "__main__":
  main(sys.argv, sys.stdout, os.environ)
