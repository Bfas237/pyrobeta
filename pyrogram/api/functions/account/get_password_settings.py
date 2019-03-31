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


class GetPasswordSettings(Object):
    """Attributes:
        ID: ``0x9cd4eaf9``

    Args:
        password: Either :obj:`InputCheckPasswordEmpty <pyrogram.api.types.InputCheckPasswordEmpty>` or :obj:`InputCheckPasswordSRP <pyrogram.api.types.InputCheckPasswordSRP>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`account.PasswordSettings <pyrogram.api.types.account.PasswordSettings>`
    """

    ID = 0x9cd4eaf9

    def __init__(self, password):
        self.password = password  # InputCheckPasswordSRP

    @staticmethod
    def read(b: BytesIO, *args) -> "GetPasswordSettings":
        # No flags
        
        password = Object.read(b)
        
        return GetPasswordSettings(password)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.password.write())
        
        return b.getvalue()
