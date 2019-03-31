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


class Document(Object):
    """Attributes:
        ID: ``0x59534e4c``

    Args:
        id: ``int`` ``64-bit``
        access_hash: ``int`` ``64-bit``
        file_reference: ``bytes``
        date: ``int`` ``32-bit``
        mime_type: ``str``
        size: ``int`` ``32-bit``
        thumb: Either :obj:`PhotoSizeEmpty <pyrogram.api.types.PhotoSizeEmpty>`, :obj:`PhotoSize <pyrogram.api.types.PhotoSize>` or :obj:`PhotoCachedSize <pyrogram.api.types.PhotoCachedSize>`
        dc_id: ``int`` ``32-bit``
        attributes: List of either :obj:`DocumentAttributeImageSize <pyrogram.api.types.DocumentAttributeImageSize>`, :obj:`DocumentAttributeAnimated <pyrogram.api.types.DocumentAttributeAnimated>`, :obj:`DocumentAttributeSticker <pyrogram.api.types.DocumentAttributeSticker>`, :obj:`DocumentAttributeVideo <pyrogram.api.types.DocumentAttributeVideo>`, :obj:`DocumentAttributeAudio <pyrogram.api.types.DocumentAttributeAudio>`, :obj:`DocumentAttributeFilename <pyrogram.api.types.DocumentAttributeFilename>` or :obj:`DocumentAttributeHasStickers <pyrogram.api.types.DocumentAttributeHasStickers>`

    See Also:
        This object can be returned by :obj:`messages.GetDocumentByHash <pyrogram.api.functions.messages.GetDocumentByHash>`.
    """

    ID = 0x59534e4c

    def __init__(self, id: int, access_hash: int, file_reference: bytes, date: int, mime_type: str, size: int, thumb, dc_id: int, attributes: list):
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.file_reference = file_reference  # bytes
        self.date = date  # int
        self.mime_type = mime_type  # string
        self.size = size  # int
        self.thumb = thumb  # PhotoSize
        self.dc_id = dc_id  # int
        self.attributes = attributes  # Vector<DocumentAttribute>

    @staticmethod
    def read(b: BytesIO, *args) -> "Document":
        # No flags
        
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        file_reference = Bytes.read(b)
        
        date = Int.read(b)
        
        mime_type = String.read(b)
        
        size = Int.read(b)
        
        thumb = Object.read(b)
        
        dc_id = Int.read(b)
        
        attributes = Object.read(b)
        
        return Document(id, access_hash, file_reference, date, mime_type, size, thumb, dc_id, attributes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(Bytes(self.file_reference))
        
        b.write(Int(self.date))
        
        b.write(String(self.mime_type))
        
        b.write(Int(self.size))
        
        b.write(self.thumb.write())
        
        b.write(Int(self.dc_id))
        
        b.write(Vector(self.attributes))
        
        return b.getvalue()
