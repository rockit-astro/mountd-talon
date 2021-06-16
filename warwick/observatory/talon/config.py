#
# This file is part of teld.
#
# teld is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# teld is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with teld.  If not, see <http://www.gnu.org/licenses/>.

"""Helper function to validate and parse the json config file"""

import json
import sys
import traceback
import jsonschema
from warwick.observatory.common import daemons, IP

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'log_name', 'control_machines', 'virtual', 'focus_tolerance',
        'query_delay', 'initialization_timeout', 'slew_timeout', 'focus_timeout',
        'homing_timeout', 'limit_timeout', 'cover_timeout', 'roof_open_timeout',
        'roof_close_timeout', 'ping_timeout', 'park_positions',
        'has_roof', 'has_covers', 'has_focus'
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
        'focus_tolerance': {
            'type': 'number',
            'min': 0
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
        'focus_timeout': {
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
        'cover_timeout': {
            'type': 'number',
            'min': 0,
        },
        'roof_open_timeout': {
            'type': 'number',
            'min': 0,
        },
        'roof_close_timeout': {
            'type': 'number',
            'min': 0,
        },
        'ping_timeout': {
            'type': 'number',
            'min': 0,
        },
        'has_roof': {
            'type': 'boolean',
        },
        'has_covers': {
            'type': 'boolean',
        },
        'has_focus': {
            'type': 'boolean',
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
                        'max': 1.570796
                    },
                    'az': {
                        'type': 'number',
                        'min': 0,
                        'max': 6.283185
                    }
                }
            }
        },
        # Optional
        'security_system_daemon': {
            'daemon_name': True,
            'type': 'string',
        },
        'security_system_key': {
            'type': 'string',
        },
    }
}


class ConfigSchemaViolationError(Exception):
    """Exception used to report schema violations"""
    def __init__(self, errors):
        message = 'Invalid configuration:\n\t' + '\n\t'.join(errors)
        super(ConfigSchemaViolationError, self).__init__(message)


def __create_validator():
    """Returns a template validator that includes support for the
       custom schema tags used by the observation schedules:
            daemon_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.daemons address book
            machine_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.IP address book
    """
    validators = dict(jsonschema.Draft4Validator.VALIDATORS)

    # pylint: disable=unused-argument
    def daemon_name(validator, value, instance, schema):
        """Validate a string as a valid daemon name"""
        try:
            getattr(daemons, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid daemon name'.format(instance))

    def machine_name(validator, value, instance, schema):
        """Validate a string as a valid machine name"""
        try:
            getattr(IP, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid machine name'.format(instance))
    # pylint: enable=unused-argument

    validators['daemon_name'] = daemon_name
    validators['machine_name'] = machine_name
    return jsonschema.validators.create(meta_schema=jsonschema.Draft4Validator.META_SCHEMA,
                                        validators=validators)


def validate_config(config_json):
    """Tests whether a json object defines a valid environment config file
       Raises SchemaViolationError on error
    """
    errors = []
    try:
        validator = __create_validator()
        for error in sorted(validator(CONFIG_SCHEMA).iter_errors(config_json),
                            key=lambda e: e.path):
            if error.path:
                path = '->'.join([str(p) for p in error.path])
                message = path + ': ' + error.message
            else:
                message = error.message
            errors.append(message)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        errors = ['exception while validating']

    if errors:
        raise ConfigSchemaViolationError(errors)


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validate_config(config_json)

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.virtual = config_json['virtual']
        self.focus_tolerance = config_json['focus_tolerance']
        self.query_delay = config_json['query_delay']
        self.initialization_timeout = config_json['initialization_timeout']
        self.slew_timeout = config_json['slew_timeout']
        self.focus_timeout = config_json['focus_timeout']
        self.homing_timeout = config_json['homing_timeout']
        self.limit_timeout = config_json['limit_timeout']
        self.cover_timeout = config_json['cover_timeout']
        self.roof_open_timeout = config_json['roof_open_timeout']
        self.roof_close_timeout = config_json['roof_close_timeout']
        self.ping_timeout = config_json['ping_timeout']

        self.has_roof = config_json['has_roof']
        self.has_covers = config_json['has_covers']
        self.has_focus = config_json['has_focus']
        self.park_positions = config_json['park_positions']

        self.security_system_daemon = None
        self.security_system_key = None
        if 'security_system_daemon' in config_json and 'security_system_key' in config_json:
            self.security_system_daemon = getattr(daemons, config_json['security_system_daemon'])
            self.security_system_key = config_json['security_system_key']
