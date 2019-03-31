# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.api.core import *


class InvokeWithTakeout(Object):
    """Attributes:
        ID: ``0xaca9fd2e``

    Args:
        takeout_id: ``int`` ``64-bit``
        query: Any method from :obj:`pyrogram.api.functions`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Any object from :obj:`pyrogram.api.types`
    """

    ID = 0xaca9fd2e

    def __init__(self, takeout_id: int, query):
        self.takeout_id = takeout_id  # long
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args) -> "InvokeWithTakeout":
        # No flags
        
        takeout_id = Long.read(b)
        
        query = Object.read(b)
        
        return InvokeWithTakeout(takeout_id, query)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.takeout_id))
        
        b.write(self.query.write())
        
        return b.getvalue()
