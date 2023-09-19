#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Helper function to validate and parse the json config file"""

import json
from rockit.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'log_name', 'control_machines', 'virtual',
        'query_delay', 'initialization_timeout', 'slew_timeout',
        'ha_soft_limits', 'dec_soft_limits',
        'homing_timeout', 'limit_timeout', 'ping_timeout',
        'park_positions'
    ],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'virtual': {
            'type': 'boolean',
        },
        'telescope': {
            'type': 'string',
            'enum': ['SuperWASP', 'W1m'],
        },
        'query_delay': {
            'type': 'number',
            'min': 0
        },
        'initialization_timeout': {
            'type': 'number',
            'min': 0,
        },
        'slew_timeout': {
            'type': 'number',
            'min': 0,
        },
        'homing_timeout': {
            'type': 'number',
            'min': 0,
        },
        'limit_timeout': {
            'type': 'number',
            'min': 0,
        },
        'ping_timeout': {
            'type': 'number',
            'min': 0,
        },
        'ha_soft_limits': {
            'type': 'array',
            'maxItems': 2,
            'minItems': 2,
            'items': {
                'type': 'number',
                'min': -180,
                'max': 180
            }
        },
        'dec_soft_limits': {
            'type': 'array',
            'maxItems': 2,
            'minItems': 2,
            'items': {
                'type': 'number',
                'min': -90,
                'max': 90
            }
        },
        'park_positions': {
            'type': 'object',
            'additionalProperties': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['desc', 'alt', 'az'],
                'properties': {
                    'desc': {
                        'type': 'string',
                    },
                    'alt': {
                        'type': 'number',
                        'min': 0,
                        'max': 90
                    },
                    'az': {
                        'type': 'number',
                        'min': 0,
                        'max': 360
                    }
                }
            }
        },
        # W1m only
        'security_system_daemon': {
            'daemon_name': True,
            'type': 'string',
        },
        'security_system_key': {
            'type': 'string',
        },
        'focus_tolerance': {
            'type': 'number',
            'min': 0
        },
        'focus_timeout': {
            'type': 'number',
            'min': 0,
        },
        'cover_timeout': {
            'type': 'number',
            'min': 0,
        },
    },
    'anyOf': [
        {
            'properties': {
                'telescope': {
                    'enum': ['W1m']
                }
            },
            'required': ['security_system_daemon', 'security_system_key', 'focus_tolerance', 'focus_timeout', 'cover_timeout']
        },
        {
            'properties': {
                'telescope': {
                    'enum': ['SuperWASP']
                }
            },
            'required': []
        },
    ]
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validation.validate_config(config_json, CONFIG_SCHEMA, {
            'daemon_name': validation.daemon_name_validator,
            'machine_name': validation.machine_name_validator
        })

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.virtual = config_json['virtual']
        self.query_delay = config_json['query_delay']
        self.initialization_timeout = config_json['initialization_timeout']
        self.slew_timeout = config_json['slew_timeout']
        self.homing_timeout = config_json['homing_timeout']
        self.limit_timeout = config_json['limit_timeout']
        self.ping_timeout = config_json['ping_timeout']
        self.ha_soft_limits = config_json['ha_soft_limits']
        self.dec_soft_limits = config_json['dec_soft_limits']
        self.park_positions = config_json['park_positions']

        self.is_onemetre = config_json['telescope'] == 'W1m'
        if self.is_onemetre:
            self.focus_tolerance = config_json['focus_tolerance']
            self.focus_timeout = config_json['focus_timeout']
            self.cover_timeout = config_json['cover_timeout']

            self.security_system_daemon = getattr(daemons, config_json['security_system_daemon'])
            self.security_system_key = config_json['security_system_key']
