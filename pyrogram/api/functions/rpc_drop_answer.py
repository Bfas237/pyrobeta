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


class RpcDropAnswer(Object):
    """Attributes:
        ID: ``0x58e4a740``

    Args:
        req_msg_id: ``int`` ``64-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`RpcAnswerUnknown <pyrogram.api.types.RpcAnswerUnknown>`, :obj:`RpcAnswerDroppedRunning <pyrogram.api.types.RpcAnswerDroppedRunning>` or :obj:`RpcAnswerDropped <pyrogram.api.types.RpcAnswerDropped>`
    """

    ID = 0x58e4a740

    def __init__(self, req_msg_id: int):
        self.req_msg_id = req_msg_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "RpcDropAnswer":
        # No flags
        
        req_msg_id = Long.read(b)
        
        return RpcDropAnswer(req_msg_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.req_msg_id))
        
        return b.getvalue()
