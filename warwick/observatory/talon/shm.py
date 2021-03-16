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

"""Helpers for reading talon's shared memory segment"""

import struct

# These offsets can be found by compiling the following into one of the talon utils (e.g. xobs or getshm)
# include <stddef.h>
# printf("Key = 0x%x\n", TELSTATSHMKEY);
# printf("PID = %zu\n", offsetof(TelStatShm, teld_pid));
# printf("MJD = 0\n");
# printf("LST = %zu\n", offsetof(TelStatShm, Clst));
# printf("RAJ2000 = %zu\n", offsetof(TelStatShm, CJ2kRA));
# printf("DecJ2000 = %zu\n", offsetof(TelStatShm, CJ2kDec));
# printf("HAApparent = %zu\n", offsetof(TelStatShm, CAHA));
# printf("DecApparent = %zu\n", offsetof(TelStatShm, CADec));
# printf("Alt = %zu\n", offsetof(TelStatShm, Calt));
# printf("Az = %zu\n", offsetof(TelStatShm, Caz));
# printf("Latitude = %zu\n", offsetof(Now, n_lat));
# printf("Longitude = %zu\n", offsetof(Now, n_lng));
# printf("Elevation = %zu\n", offsetof(Now, n_elev));
# printf("TelState = %zu\n", offsetof(TelStatShm, telstate));
# printf("TelStateIdx = %zu\n", offsetof(TelStatShm, telstateidx));
# printf("RoofState = %zu\n", offsetof(TelStatShm, shutterstate));
# printf("CoverState = %zu\n", offsetof(TelStatShm, coverstate));
# printf("HeartbeatRemaining = %zu\n", offsetof(TelStatShm, domeheartbeatremaining));
# printf("RAFlags = %zu\n", offsetof(TelStatShm, minfo) + 1);
# printf("RAPosLim = %zu\n", offsetof(TelStatShm, minfo) + offsetof(MotorInfo, poslim));
# printf("RANegLim = %zu\n", offsetof(TelStatShm, minfo) + offsetof(MotorInfo, neglim));
# printf("DecFlags = %zu\n", offsetof(TelStatShm, minfo) + 1 + sizeof(MotorInfo));
# printf("DecPosLim = %zu\n", offsetof(TelStatShm, minfo) + offsetof(MotorInfo, poslim) + sizeof(MotorInfo));
# printf("DecNegLim = %zu\n", offsetof(TelStatShm, minfo) + offsetof(MotorInfo, neglim) + sizeof(MotorInfo));
# printf("FocusFlags = %zu\n", offsetof(TelStatShm, minfo) + 1 + 3 * sizeof(MotorInfo));
# printf("FocusStep = %zu\n", offsetof(TelStatShm, minfo) + offsetof(MotorInfo, step) + 3 * sizeof(MotorInfo));
# printf("FocusCPos = %zu\n", offsetof(TelStatShm, minfo) + offsetof(MotorInfo, cpos) + 3 * sizeof(MotorInfo));
# printf("FocusDF = %zu\n", offsetof(TelStatShm, minfo) + offsetof(MotorInfo, df) + 3 * sizeof(MotorInfo));


class ShmOffsets:
    Key = 0x4e56361a
    PID = 840
    MJD = 0
    LST = 152
    RAJ2000 = 88
    DecJ2000 = 96
    HAApparent = 112
    DecApparent = 120
    Alt = 128
    Az = 136
    Latitude = 8
    Longitude = 16
    Elevation = 48
    TelState = 808
    TelStateIdx = 812
    RoofState = 820
    CoverState = 824
    HeartbeatRemaining = 836
    RAFlags = 257
    RAPosLim = 312
    RANegLim = 320
    DecFlags = 377
    DecPosLim = 432
    DecNegLim = 440
    FocusFlags = 617
    FocusStep = 620
    FocusCPos = 712
    FocusDF = 696


def shm_read_double(shm, offset):
    """read a double from a specified offset in a specified shared memory segment"""
    return struct.unpack_from('d', shm.read(8, offset))[0]


def shm_read_int(shm, offset):
    """read an int from a specified offset in a specified shared memory segment"""
    return struct.unpack_from('i', shm.read(4, offset))[0]


def shm_read_ushort(shm, offset):
    """read a ushort from a specified offset in a specified shared memory segment"""
    return struct.unpack_from('H', shm.read(2, offset))[0]
