#!/usr/bin/env python3

################################################################
#                                                              #
#  Name:    satellite_health_check                             #
#                                                              #
#  Version: 1.0.0                                              #
#  Created: 2025-03-24                                         #
#  Last Update: 2025-05-15                                     #
#  License: GPL - http://www.gnu.org/licenses                  #
#  Copyright: (c)2025 René Koch                                #
#  Author:  Rene Koch <rkoch@rk-it.at>                         #
#  URL: https://github.com/rk-it-at/cmk_satellite_health_check #
#                                                              #
################################################################

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .agent_based_api.v1 import check_levels, Metric, register, Result, Service, State

def parse_satellite_health_check(string_table):
  parsed = {}
  column_names = [
    "check",
    "result"
  ]
  for line in string_table:
    parsed[line[0]] = {}
    for n in range(1, len(column_names)):
      parsed[line[0]][column_names[n]] = line[n]
  return parsed

def discover_satellite_health_check(section):
  for check in section:
    yield Service(item=check)

def check_satellite_health(item, section):
  attr = section.get(item)
  if attr['result'] == "ok":
    yield Result(state=State.OK, summary=f"OK")
  else:
    yield Result(state=State.CRIT, summary=f"Failed components: {attr['result']}")

register.agent_section(
  name = "satellite_health_check",
  parse_function = parse_satellite_health_check
)

register.check_plugin(
  name = "satellite_health_check",
  sections = ["satellite_health_check"],
  service_name = "Satellite Health %s",
  discovery_function = discover_satellite_health_check,
  check_function = check_satellite_health
)
