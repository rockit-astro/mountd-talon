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

"""Constants and status codes used by teld"""

from warwick.observatory.common import TFmt


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
    TelescopeNotStopped = 12
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
        12: 'error: telescope is not stopped',
        14: 'error: telescope has already been initialized',

        20: 'error: requested coordinates outside HA limits',
        21: 'error: requested coordinates outside Dec limits',

        # tel specific codes
        -100: 'error: terminated by user',
        -101: 'error: unable to communicate with telescope daemon',
        -103: 'error: unable to communicate with data pipeline daemon',
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing an error code"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return 'error: Unknown error code {}'.format(error_code)


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

    _formats = {
        0: TFmt.Red + TFmt.Bold,
        1: TFmt.Red + TFmt.Bold,
        2: TFmt.Yellow + TFmt.Bold,
        3: TFmt.Green + TFmt.Bold,
        4: TFmt.Yellow + TFmt.Bold,
        5: TFmt.Yellow + TFmt.Bold,
        6: TFmt.Yellow + TFmt.Bold,
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._formats:
                return cls._formats[status] + cls._labels[status] + TFmt.Clear
            return TFmt.Red + TFmt.Bold + 'UNKNOWN' + TFmt.Clear

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
            return TFmt.Bold + label + TFmt.Clear

        return label


class CoverState:
    """Talon CoverState enum"""
    Absent, Idle, Opening, Closing, Open, Closed = range(6)

    _labels = {
        0: 'ABSENT',
        1: 'IDLE',
        2: 'OPENING',
        3: 'CLOSING',
        4: 'OPEN',
        5: 'CLOSED',
    }

    _formats = {
        0: TFmt.Red + TFmt.Bold,
        1: TFmt.Bold,
        2: TFmt.Yellow + TFmt.Bold,
        3: TFmt.Yellow + TFmt.Bold,
        4: TFmt.Green + TFmt.Bold,
        5: TFmt.Red + TFmt.Bold,
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._formats:
                return cls._formats[status] + cls._labels[status] + TFmt.Clear
            return TFmt.Red + TFmt.Bold + 'UNKNOWN' + TFmt.Clear

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'


class RoofState:
    """Talon DShState enum"""
    Absent, Idle, Opening, Closing, Open, Closed = range(6)

    _labels = {
        0: 'ABSENT',
        1: 'UNKNOWN',
        2: 'OPENING',
        3: 'CLOSING',
        4: 'OPEN',
        5: 'CLOSED',
    }

    _formats = {
        0: TFmt.Red + TFmt.Bold,
        1: TFmt.Red + TFmt.Bold,
        2: TFmt.Yellow + TFmt.Bold,
        3: TFmt.Yellow + TFmt.Bold,
        4: TFmt.Green + TFmt.Bold,
        5: TFmt.Red + TFmt.Bold,
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._formats:
                return cls._formats[status] + cls._labels[status] + TFmt.Clear
            return TFmt.Red + TFmt.Bold + 'UNKNOWN' + TFmt.Clear

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'
