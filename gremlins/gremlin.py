#!/usr/bin/env python
import random
import time
from gremlins import faults
import signal
import logging

logging.basicConfig(level=logging.INFO)

active_faults = []
fault_weights=[

# kill -9s
  (1, faults.kill_daemon("HRegionServer", signal.SIGKILL, 20)),
  (1, faults.kill_daemon("DataNode", signal.SIGKILL, 20)),

# pauses (simulate GC?)
  (1, faults.pause_daemon("HRegionServer", 60)),
  (1, faults.pause_daemon("DataNode", 10)),

# drop packets (simulate network outage)
  (1, faults.drop_packets_to_daemon("DataNode", 20)),
  (1, faults.drop_packets_to_daemon("HRegionServer", 20)),

  ]

fault_frequency = 1

def inject_a_fault():
  fault = pick_fault()
  fault()

def pick_fault():
  total_weight = sum( wt for wt,fault in fault_weights )
  pick = random.random() * total_weight
  accrued = 0
  for wt, fault in fault_weights:
    accrued += wt
    if pick <= accrued:
      return fault

  assert "should not get here, pick=" + pick

def main():
  while True:
    time.sleep(fault_frequency)
    inject_a_fault()


if __name__ == "__main__":
  main()


