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

"""Constants and status codes used by talond"""


class CommandStatus:
    """Numeric return codes"""
    # General error codes
    Succeeded = 0
    Failed = 1
    Blocked = 2

    InvalidControlIP = 5
    CannotCommunicateWithSecuritySystem = 6
    SecuritySystemTripped = 7

    # Command-specific codes
    TelescopeNotInitialized = 10
    TelescopeNotHomed = 11
    TelescopeNotUninitialized = 14

    OutsideHALimits = 20
    OutsideDecLimits = 21

    _messages = {
        # General error codes
        1: 'error: command failed',
        2: 'error: another command is already running',
        5: 'error: command not accepted from this IP',
        6: 'error: telescope failed to communicate with security system daemon',
        7: 'error: hard limits (security system) have been tripped',

        # Command-specific codes
        10: 'error: telescope has not been initialized',
        11: 'error: telescope has not been homed',
        14: 'error: telescope has already been initialized',

        20: 'error: requested coordinates outside HA limits',
        21: 'error: requested coordinates outside Dec limits',

        # tel specific codes
        -100: 'error: terminated by user',
        -101: 'error: unable to communicate with telescope daemon',
        -102: 'error: command not available for this telescope'
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing an error code"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return f'error: Unknown error code {error_code}'


class TelState:
    """Talon TelState enum"""
    Absent, Stopped, Hunting, Tracking, Slewing, Homing, Limiting = range(7)

    _labels = {
        0: 'DISABLED',
        1: 'STOPPED',
        2: 'HUNTING',
        3: 'TRACKING',
        4: 'SLEWING',
        5: 'HOMING',
        6: 'LIMITING',
    }

    _colors = {
        0: 'red',
        1: 'red',
        2: 'yellow',
        3: 'green',
        4: 'yellow',
        5: 'yellow',
        6: 'yellow'
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._labels and status in cls._colors:
                return f'[b][{cls._colors[status]}]{cls._labels[status]}[/{cls._colors[status]}][/b]'
            return '[b][red]UNKNOWN[/red][/b]'

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'


class FocusState:
    """Focus status built from talon motor flags"""
    Absent, NotHomed, Homing, Limiting, Ready = range(5)

    _labels = {
        0: 'ABSENT',
        1: 'NOT_HOMED',
        2: 'HOMING',
        3: 'LIMITING',
        4: 'READY',
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if status in cls._labels:
            label = cls._labels[status]
        else:
            label = 'UNKNOWN'

        if formatting:
            return f'[b]{label}[/b]'

        return label
