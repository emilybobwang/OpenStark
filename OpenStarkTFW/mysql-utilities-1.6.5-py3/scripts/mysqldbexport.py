#!/usr/bin/env python
#
# Copyright (c) 2010, 2016, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#

"""
This file contains the export database utility which allows users to export
metadata for objects in a database and data for tables.
"""

import os, sys

from mysql.utilities.command.dbexport import parse_options, export_db

if __name__ == '__main__':
    parser = parse_options(os.path.basename(sys.argv[0]))
    if parser: 
        res = export_db(parser)
        if res:
            sys.exit()
        else:
            sys.exit(1)
