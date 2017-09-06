#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# TimeSeriesProcessing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TimeSeriesProcessing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

class MemoryReader:
    def __init__(self, myFilename):
        self.filename = myFilename

    def read_metadata(self):
        return {};

    def read_data(self):
        return None
