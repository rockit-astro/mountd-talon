#!/usr/bin/env python3
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

import distutils.core

distutils.core.setup(name='onemetre-teld',
    version='1.0',
    author="Paul Chote",
    author_email="P.Chote@warwick.ac.uk",
    url="https://github.com/warwick-one-metre/teld",
    description="Daemon for controlling the Warwick one-metre telescope via Pyro.",
    long_description="Daemon for controlling the Warwick one-metre telescope via Pyro.",
    license="GPL3",

    options = {'bdist_rpm': {
      'post_install' : 'postinstall.sh',
      'group' : 'Unspecified',
      'requires' : 'python3, onemetre-talon'
    }},

    scripts=['teld', 'tel'],
    data_files=[
        ('/usr/lib/systemd/system', ['teld.service']),
    ],
)