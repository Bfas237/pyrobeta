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


class GetLanguages(Object):
    """Attributes:
        ID: ``0x42c6978f``

    Args:
        lang_pack: ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        List of :obj:`LangPackLanguage <pyrogram.api.types.LangPackLanguage>`
    """

    ID = 0x42c6978f

    def __init__(self, lang_pack: str):
        self.lang_pack = lang_pack  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "GetLanguages":
        # No flags
        
        lang_pack = String.read(b)
        
        return GetLanguages(lang_pack)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_pack))
        
        return b.getvalue()
