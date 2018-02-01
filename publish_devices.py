#!/usr/bin/python
# coding: utf-8

"""
Publish all lights.
Make a cron job that runs every so often (every 5 minutes):
0/5 * * * * /usr/bin/python /path/to/publish_devices.py
"""

import os
main_base = os.path.dirname(__file__)
config_file = os.path.join(main_base, "config", "prod.cfg")

from src import lights

light = lights.Lights(config_file)
