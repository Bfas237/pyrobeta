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

from functools import partial
from typing import List, Match, Union

import pyrogram
from pyrogram.api import types
from pyrogram.api.errors import MessageIdsEmpty
from pyrogram.client.ext import ChatAction, ParseMode
from pyrogram.client.types.input_media import InputMedia
from .contact import Contact
from .location import Location
from .message_entity import MessageEntity
from ..messages_and_media.photo import Photo
from ..pyrogram_type import PyrogramType
from ..update import Update
from ..user_and_chats.chat import Chat
from ..user_and_chats.user import User

class Str(str):
    def __init__(self, *args):
        super().__init__()

        self.client = None
        self.entities = None

    def init(self, client, entities):
        self.client = client
        self.entities = entities

        return self

    @property
    def text(self):
        return self

    @property
    def markdown(self):
        return self.client.markdown.unparse(self, self.entities)

    @property
    def html(self):
        return self.client.html.unparse(self, self.entities)


class Message(PyrogramType, Update):
    """This object represents a message.

    Args:
        message_id (``int``):
            Unique message identifier inside this chat.

        date (``int``, *optional*):
            Date the message was sent in Unix time.

        chat (:obj:`Chat <pyrogram.Chat>`, *optional*):
            Conversation the message belongs to.

        from_user (:obj:`User <pyrogram.User>`, *optional*):
            Sender, empty for messages sent to channels.

        forward_from (:obj:`User <pyrogram.User>`, *optional*):
            For forwarded messages, sender of the original message.

        forward_from_chat (:obj:`Chat <pyrogram.Chat>`, *optional*):
            For messages forwarded from channels, information about the original channel.

        forward_from_message_id (``int``, *optional*):
            For messages forwarded from channels, identifier of the original message in the channel.

        forward_signature (``str``, *optional*):
            For messages forwarded from channels, signature of the post author if present.

        forward_date (``int``, *optional*):
            For forwarded messages, date the original message was sent in Unix time.

        reply_to_message (:obj:`Message <pyrogram.Message>`, *optional*):
            For replies, the original message. Note that the Message object in this field will not contain
            further reply_to_message fields even if it itself is a reply.

        mentioned (``bool``, *optional*):
            The message contains a mention.

        empty (``bool``, *optional*):
            The message is empty.
            A message can be empty in case it was deleted or you tried to retrieve a message that doesn't exist yet.

        service (``bool``, *optional*):
            The message is a service message.
            A service message has one and only one of these fields set: left_chat_member, new_chat_title,
            new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created, channel_chat_created,
            migrate_to_chat_id, migrate_from_chat_id, pinned_message.

        media (``bool`` *optional*):
            The message is a media message.
            A media message has one and only one of these fields set: audio, document, photo, sticker, video, animation,
            voice, video_note, contact, location, venue.

        edit_date (``int``, *optional*):
            Date the message was last edited in Unix time.

        media_group_id (``str``, *optional*):
            The unique identifier of a media message group this message belongs to.

        author_signature (``str``, *optional*):
            Signature of the post author for messages in channels.

        text (``str``, *optional*):
            For text messages, the actual UTF-8 text of the message, 0-4096 characters.
            If the message contains entities (bold, italic, ...) you can access *text.markdown* or
            *text.html* to get the marked up message text. In case there is no entity, the fields
            will contain the same text as *text*.

        entities (List of :obj:`MessageEntity <pyrogram.MessageEntity>`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        caption_entities (List of :obj:`MessageEntity <pyrogram.MessageEntity>`, *optional*):
            For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear
            in the caption.

        audio (:obj:`Audio <pyrogram.Audio>`, *optional*):
            Message is an audio file, information about the file.

        document (:obj:`Document <pyrogram.Document>`, *optional*):
            Message is a general file, information about the file.

        photo (:obj:`Photo <pyrogram.Photo>`, *optional*):
            Message is a photo, information about the photo.

        sticker (:obj:`Sticker <pyrogram.Sticker>`, *optional*):
            Message is a sticker, information about the sticker.

        animation (:obj:`Animation <pyrogram.Animation>`, *optional*):
            Message is an animation, information about the animation.

        game (:obj:`Game <pyrogram.Game>`, *optional*):
            Message is a game, information about the game.

        video (:obj:`Video <pyrogram.Video>`, *optional*):
            Message is a video, information about the video.

        voice (:obj:`Voice <pyrogram.Voice>`, *optional*):
            Message is a voice message, information about the file.

        video_note (:obj:`VideoNote <pyrogram.VideoNote>`, *optional*):
            Message is a video note, information about the video message.

        caption (``str``, *optional*):
            Caption for the audio, document, photo, video or voice, 0-1024 characters.
            If the message contains caption entities (bold, italic, ...) you can access *caption.markdown* or
            *caption.html* to get the marked up caption text. In case there is no caption entity, the fields
            will contain the same text as *caption*.

        contact (:obj:`Contact <pyrogram.Contact>`, *optional*):
            Message is a shared contact, information about the contact.

        location (:obj:`Location <pyrogram.Location>`, *optional*):
            Message is a shared location, information about the location.

        venue (:obj:`Venue <pyrogram.Venue>`, *optional*):
            Message is a venue, information about the venue.

        web_page (``bool``, *optional*):
            Message was sent with a webpage preview.
            **Note:** Support for web pages is still basic; a simple boolean is set in case the message contains a
            web page preview. In future versions this property could turn into a full web page object that contains
            more details.

        new_chat_members (List of :obj:`User <pyrogram.User>`, *optional*):
            New members that were added to the group or supergroup and information about them
            (the bot itself may be one of these members).

        left_chat_member (:obj:`User <pyrogram.User>`, *optional*):
            A member was removed from the group, information about them (this member may be the bot itself).

        new_chat_title (``str``, *optional*):
            A chat title was changed to this value.

        new_chat_photo (:obj:`Photo <pyrogram.Photo>`, *optional*):
            A chat photo was change to this value.

        delete_chat_photo (``bool``, *optional*):
            Service message: the chat photo was deleted.

        group_chat_created (``bool``, *optional*):
            Service message: the group has been created.

        supergroup_chat_created (``bool``, *optional*):
            Service message: the supergroup has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            supergroup when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a directly created supergroup.

        channel_chat_created (``bool``, *optional*):
            Service message: the channel has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            channel when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a channel.

        migrate_to_chat_id (``int``, *optional*):
            The group has been migrated to a supergroup with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        migrate_from_chat_id (``int``, *optional*):
            The supergroup has been migrated from a group with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        pinned_message (:obj:`Message <pyrogram.Message>`, *optional*):
            Specified message was pinned.
            Note that the Message object in this field will not contain further reply_to_message fields even if it
            is itself a reply.

        game_high_score (:obj:`GameHighScore <pyrogram.GameHighScore>`, *optional*):
            The game score for a user.
            The reply_to_message field will contain the game Message.

        views (``int``, *optional*):
            Channel post views.

        via_bot (:obj:`User <pyrogram.User>`):
            The information of the bot that generated the message from an inline query of a user.

        outgoing (``bool``, *optional*):
            Whether the message is incoming or outgoing.
            Messages received from other chats are incoming (*outgoing* is False).
            Messages sent from yourself to other chats are outgoing (*outgoing* is True).
            An exception is made for your own personal chat; messages sent there will be incoming.

        matches (List of regex Matches, *optional*):
            A list containing all `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ that match
            the text of this message. Only applicable when using :obj:`Filters.regex <pyrogram.Filters.regex>`.

        command (List of ``str``, *optional*):
            A list containing the command and its arguments, if any.
            E.g.: "/start 1 2 3" would produce ["start", "1", "2", "3"].
            Only applicable when using :obj:`Filters.command <pyrogram.Filters.command>`.

        reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
            Additional interface options. An object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.
    """

    # TODO: Add game missing field. Also invoice, successful_payment, connected_website

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 message_id: int,
                 date: int = None,
                 chat: Chat = None,
                 from_user: User = None,
                 forward_from: User = None,
                 forward_from_chat: Chat = None,
                 forward_from_message_id: int = None,
                 forward_signature: str = None,
                 forward_date: int = None,
                 reply_to_message: "Message" = None,
                 mentioned: bool = None,
                 empty: bool = None,
                 service: bool = None,
                 media: bool = None,
                 edit_date: int = None,
                 media_group_id: str = None,
                 author_signature: str = None,
                 text: str = None,
                 entities: List["pyrogram.MessageEntity"] = None,
                 caption_entities: List["pyrogram.MessageEntity"] = None,
                 audio: "pyrogram.Audio" = None,
                 document: "pyrogram.Document" = None,
                 photo: "pyrogram.Photo" = None,
                 sticker: "pyrogram.Sticker" = None,
                 animation: "pyrogram.Animation" = None,
                 game: "pyrogram.Game" = None,
                 video: "pyrogram.Video" = None,
                 voice: "pyrogram.Voice" = None,
                 video_note: "pyrogram.VideoNote" = None,
                 caption: str = None,
                 contact: "pyrogram.Contact" = None,
                 location: "pyrogram.Location" = None,
                 venue: "pyrogram.Venue" = None,
                 web_page: bool = None,
                 poll: "pyrogram.Poll" = None,
                 new_chat_members: List[User] = None,
                 left_chat_member: User = None,
                 new_chat_title: str = None,
                 new_chat_photo: "pyrogram.Photo" = None,
                 delete_chat_photo: bool = None,
                 group_chat_created: bool = None,
                 supergroup_chat_created: bool = None,
                 channel_chat_created: bool = None,
                 migrate_to_chat_id: int = None,
                 migrate_from_chat_id: int = None,
                 pinned_message: "Message" = None,
                 game_high_score: int = None,
                 views: int = None,
                 via_bot: User = None,
                 outgoing: bool = None,
                 matches: List[Match] = None,
                 command: List[str] = None,
                 reply_markup: Union["pyrogram.InlineKeyboardMarkup",
                                     "pyrogram.ReplyKeyboardMarkup",
                                     "pyrogram.ReplyKeyboardRemove",
                                     "pyrogram.ForceReply"] = None):
        super().__init__(client)

        self.message_id = message_id
        self.date = date
        self.chat = chat
        self.from_user = from_user
        self.forward_from = forward_from
        self.forward_from_chat = forward_from_chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_date = forward_date
        self.reply_to_message = reply_to_message
        self.mentioned = mentioned
        self.empty = empty
        self.service = service
        self.media = media
        self.edit_date = edit_date
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.text = text
        self.entities = entities
        self.caption_entities = caption_entities
        self.audio = audio
        self.document = document
        self.photo = photo
        self.sticker = sticker
        self.animation = animation
        self.game = game
        self.video = video
        self.voice = voice
        self.video_note = video_note
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.web_page = web_page
        self.poll = poll
        self.new_chat_members = new_chat_members
        self.left_chat_member = left_chat_member
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = pinned_message
        self.game_high_score = game_high_score
        self.views = views
        self.via_bot = via_bot
        self.outgoing = outgoing
        self.matches = matches
        self.command = command
        self.reply_markup = reply_markup

    @staticmethod
    def _parse(client, message: types.Message or types.MessageService or types.MessageEmpty, users: dict, chats: dict,
               replies: int = 1):
        if isinstance(message, types.MessageEmpty):
            return Message(message_id=message.id, empty=True, client=client)

        if isinstance(message, types.MessageService):
            action = message.action

            new_chat_members = None
            left_chat_member = None
            new_chat_title = None
            delete_chat_photo = None
            migrate_to_chat_id = None
            migrate_from_chat_id = None
            group_chat_created = None
            channel_chat_created = None
            new_chat_photo = None

            if isinstance(action, types.MessageActionChatAddUser):
                new_chat_members = [User._parse(client, users[i]) for i in action.users]
            elif isinstance(action, types.MessageActionChatJoinedByLink):
                new_chat_members = [User._parse(client, users[message.from_id])]
            elif isinstance(action, types.MessageActionChatDeleteUser):
                left_chat_member = User._parse(client, users[action.user_id])
            elif isinstance(action, types.MessageActionChatEditTitle):
                new_chat_title = action.title
            elif isinstance(action, types.MessageActionChatDeletePhoto):
                delete_chat_photo = True
            elif isinstance(action, types.MessageActionChatMigrateTo):
                migrate_to_chat_id = action.channel_id
            elif isinstance(action, types.MessageActionChannelMigrateFrom):
                migrate_from_chat_id = action.chat_id
            elif isinstance(action, types.MessageActionChatCreate):
                group_chat_created = True
            elif isinstance(action, types.MessageActionChannelCreate):
                channel_chat_created = True
            elif isinstance(action, types.MessageActionChatEditPhoto):
                new_chat_photo = Photo._parse(client, action.photo)

            parsed_message = Message(
                message_id=message.id,
                date=message.date,
                chat=Chat._parse(client, message, users, chats),
                from_user=User._parse(client, users.get(message.from_id, None)),
                service=True,
                new_chat_members=new_chat_members,
                left_chat_member=left_chat_member,
                new_chat_title=new_chat_title,
                new_chat_photo=new_chat_photo,
                delete_chat_photo=delete_chat_photo,
                migrate_to_chat_id=int("-100" + str(migrate_to_chat_id)) if migrate_to_chat_id else None,
                migrate_from_chat_id=-migrate_from_chat_id if migrate_from_chat_id else None,
                group_chat_created=group_chat_created,
                channel_chat_created=channel_chat_created,
                client=client
                # TODO: supergroup_chat_created
            )

            if isinstance(action, types.MessageActionPinMessage):
                try:
                    parsed_message.pinned_message = client.get_messages(
                        parsed_message.chat.id,
                        reply_to_message_ids=message.id,
                        replies=0
                    )
                except MessageIdsEmpty:
                    pass

            if isinstance(action, types.MessageActionGameScore):
                parsed_message.game_high_score = pyrogram.GameHighScore._parse_action(client, message, users)

                if message.reply_to_msg_id and replies:
                    try:
                        parsed_message.reply_to_message = client.get_messages(
                            parsed_message.chat.id,
                            reply_to_message_ids=message.id,
                            replies=0
                        )
                    except MessageIdsEmpty:
                        pass

            return parsed_message

        if isinstance(message, types.Message):
            entities = [MessageEntity._parse(client, entity, users) for entity in message.entities]
            entities = list(filter(lambda x: x is not None, entities))

            forward_from = None
            forward_from_chat = None
            forward_from_message_id = None
            forward_signature = None
            forward_date = None

            forward_header = message.fwd_from

            if forward_header:
                forward_date = forward_header.date

                if forward_header.from_id:
                    forward_from = User._parse(client, users[forward_header.from_id])
                else:
                    forward_from_chat = Chat._parse_channel_chat(client, chats[forward_header.channel_id])
                    forward_from_message_id = forward_header.channel_post
                    forward_signature = forward_header.post_author

            photo = None
            location = None
            contact = None
            venue = None
            game = None
            audio = None
            voice = None
            animation = None
            video = None
            video_note = None
            sticker = None
            document = None
            web_page = None
            poll = None

            media = message.media

            if media:
                if isinstance(media, types.MessageMediaPhoto):
                    photo = Photo._parse(client, media.photo)
                elif isinstance(media, types.MessageMediaGeo):
                    location = Location._parse(client, media.geo)
                elif isinstance(media, types.MessageMediaContact):
                    contact = Contact._parse(client, media)
                elif isinstance(media, types.MessageMediaVenue):
                    venue = pyrogram.Venue._parse(client, media)
                elif isinstance(media, types.MessageMediaGame):
                    game = pyrogram.Game._parse(client, message)
                elif isinstance(media, types.MessageMediaDocument):
                    doc = media.document

                    if isinstance(doc, types.Document):
                        attributes = {type(i): i for i in doc.attributes}

                        file_name = getattr(
                            attributes.get(
                                types.DocumentAttributeFilename, None
                            ), "file_name", None
                        )

                        if types.DocumentAttributeAudio in attributes:
                            audio_attributes = attributes[types.DocumentAttributeAudio]

                            if audio_attributes.voice:
                                voice = pyrogram.Voice._parse(client, doc, audio_attributes)
                            else:
                                audio = pyrogram.Audio._parse(client, doc, audio_attributes, file_name)
                        elif types.DocumentAttributeAnimated in attributes:
                            video_attributes = attributes.get(types.DocumentAttributeVideo, None)

                            animation = pyrogram.Animation._parse(client, doc, video_attributes, file_name)
                        elif types.DocumentAttributeVideo in attributes:
                            video_attributes = attributes[types.DocumentAttributeVideo]

                            if video_attributes.round_message:
                                video_note = pyrogram.VideoNote._parse(client, doc, video_attributes)
                            else:
                                video = pyrogram.Video._parse(client, doc, video_attributes, file_name)
                        elif types.DocumentAttributeSticker in attributes:
                            sticker = pyrogram.Sticker._parse(
                                client, doc,
                                attributes.get(types.DocumentAttributeImageSize, None),
                                attributes[types.DocumentAttributeSticker],
                                file_name
                            )
                        else:
                            document = pyrogram.Document._parse(client, doc, file_name)
                elif isinstance(media, types.MessageMediaWebPage):
                    web_page = True
                    media = None
                elif isinstance(media, types.MessageMediaPoll):
                    poll = pyrogram.Poll._parse(client, media)
                else:
                    media = None

            reply_markup = message.reply_markup

            if reply_markup:
                if isinstance(reply_markup, types.ReplyKeyboardForceReply):
                    reply_markup = pyrogram.ForceReply.read(reply_markup)
                elif isinstance(reply_markup, types.ReplyKeyboardMarkup):
                    reply_markup = pyrogram.ReplyKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, types.ReplyInlineMarkup):
                    reply_markup = pyrogram.InlineKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, types.ReplyKeyboardHide):
                    reply_markup = pyrogram.ReplyKeyboardRemove.read(reply_markup)
                else:
                    reply_markup = None

            parsed_message = Message(
                message_id=message.id,
                date=message.date,
                chat=Chat._parse(client, message, users, chats),
                from_user=User._parse(client, users.get(message.from_id, None)),
                text=Str(message.message).init(client, entities) or None if media is None else None,
                caption=Str(message.message).init(client, entities) or None if media is not None else None,
                entities=entities or None if media is None else None,
                caption_entities=entities or None if media is not None else None,
                author_signature=message.post_author,
                forward_from=forward_from,
                forward_from_chat=forward_from_chat,
                forward_from_message_id=forward_from_message_id,
                forward_signature=forward_signature,
                forward_date=forward_date,
                mentioned=message.mentioned,
                media=bool(media) or None,
                edit_date=message.edit_date,
                media_group_id=message.grouped_id,
                photo=photo,
                location=location,
                contact=contact,
                venue=venue,
                audio=audio,
                voice=voice,
                animation=animation,
                game=game,
                video=video,
                video_note=video_note,
                sticker=sticker,
                document=document,
                web_page=web_page,
                poll=poll,
                views=message.views,
                via_bot=User._parse(client, users.get(message.via_bot_id, None)),
                outgoing=message.out,
                reply_markup=reply_markup,
                client=client
            )

            if message.reply_to_msg_id and replies:
                try:
                    parsed_message.reply_to_message = client.get_messages(
                        parsed_message.chat.id,
                        reply_to_message_ids=message.id,
                        replies=replies - 1
                    )
                except MessageIdsEmpty:
                    pass

            return parsed_message

    def reply(self,
              text: str,
              quote: bool = None,
              parse_mode: str = "",
              disable_web_page_preview: bool = None,
              disable_notification: bool = None,
              reply_to_message_id: int = None,
              reply_markup=None):
        """Bound method *reply* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_message(
                chat_id=message.chat.id,
                text="hello",
                reply_to_message_id=message.message_id
            )

        Example:
            .. code-block:: python

                message.reply("hello", quote=True)

        Args:
            text (``str``):
                Text of the message to be sent.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your message.
                Defaults to Markdown.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )
    def reply_animation(
        self,
        animation: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: str = "",
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: str = None,
        disable_notification: bool = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        reply_to_message_id: int = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_animation* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_animation(
                chat_id=message.chat.id,
                animation=animation
            )

        Example:
            .. code-block:: python

                message.reply_animation(animation)

        Args:
            animation (``str``):
                Animation to send.
                Pass a file_id as string to send an animation that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an animation from the Internet, or
                pass a file path as string to upload a new animation that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Animation caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (``int``, *optional*):
                Duration of sent animation in seconds.

            width (``int``, *optional*):
                Animation width.

            height (``int``, *optional*):
                Animation height.

            thumb (``str``, *optional*):
                Thumbnail of the animation file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 90 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>`
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_animation(
            chat_id=self.chat.id,
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    def reply_audio(
        self,
        audio: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: str = "",
        duration: int = 0,
        performer: str = None,
        title: str = None,
        thumb: str = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_audio* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_audio(
                chat_id=message.chat.id,
                audio=audio
            )

        Example:
            .. code-block:: python

                message.reply_audio(audio)

        Args:
            audio (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio file from the Internet, or
                pass a file path as string to upload a new audio file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Audio caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (``int``, *optional*):
                Duration of the audio in seconds.

            performer (``str``, *optional*):
                Performer.

            title (``str``, *optional*):
                Track name.

            thumb (``str``, *optional*):
                Thumbnail of the music file album cover.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 90 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>`
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_audio(
            chat_id=self.chat.id,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    def reply_cached_media(
        self,
        file_id: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: str = "",
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_cached_media* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_id
            )

        Example:
            .. code-block:: python

                message.reply_cached_media(file_id)

        Args:
            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``bool``, *optional*):
                Media caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>`
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_cached_media(
            chat_id=self.chat.id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

    def reply_chat_action(
        self,
        action: Union[ChatAction, str],
        progress: int = 0
    ) -> "Message":
        """Bound method *reply_chat_action* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_chat_action(
                chat_id=message.chat.id,
                action="typing"
            )

        Example:
            .. code-block:: python

                message.reply_chat_action("typing")

        Args:
            action (:obj:`ChatAction <pyrogram.ChatAction>` | ``str``):
                Type of action to broadcast.
                Choose one from the :class:`ChatAction <pyrogram.ChatAction>` enumeration,
                depending on what the user is about to receive.
                You can also provide a string (e.g. "typing", "upload_photo", "record_audio", ...).

            progress (``int``, *optional*):
                Progress of the upload process.
                Currently useless because official clients don't seem to be handling this.

        Returns:
            On success, True is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
            ``ValueError`` if the provided string is not a valid ChatAction.
        """
        return self._client.send_chat_action(
            chat_id=self.chat.id,
            action=action,
            progress=progress
        )

    def reply_document(
        self,
        document: str,
        quote: bool = None,
        thumb: str = None,
        caption: str = "",
        parse_mode: str = "",
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_document* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_document(
                chat_id=message.chat.id,
                document=document
            )

        Example:
            .. code-block:: python

                message.reply_document(document)

        Args:
            document (``str``):
                File to send.
                Pass a file_id as string to send a file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a file from the Internet, or
                pass a file path as string to upload a new file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            thumb (``str``, *optional*):
                Thumbnail of the file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 90 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            caption (``str``, *optional*):
                Document caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_document(
            chat_id=self.chat.id,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )


    def reply_inline_bot_result(
        self,
        query_id: int,
        result_id: str,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        hide_via: bool = None
    ) -> "Message":
        """Bound method *reply_inline_bot_result* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=query_id,
                result_id=result_id
            )

        Example:
            .. code-block:: python

                message.reply_inline_bot_result(query_id, result_id)

        Args:
            query_id (``int``):
                Unique identifier for the answered query.

            result_id (``str``):
                Unique identifier for the result that was chosen.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``bool``, *optional*):
                If the message is a reply, ID of the original message.

            hide_via (``bool``):
                Sends the message with *via @bot* hidden.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_inline_bot_result(
            chat_id=self.chat.id,
            query_id=query_id,
            result_id=result_id,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            hide_via=hide_via
        )

    def reply_location(
        self,
        latitude: float,
        longitude: float,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_location* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_location(
                chat_id=message.chat.id,
                latitude=41.890251,
                longitude=12.492373
            )

        Example:
            .. code-block:: python

                message.reply_location(41.890251, 12.492373)

        Args:
            latitude (``float``):
                Latitude of the location.

            longitude (``float``):
                Longitude of the location.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_location(
            chat_id=self.chat.id,
            latitude=latitude,
            longitude=longitude,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

    def reply_media_group(
        self,
        media: List[Union["pyrogram.InputMediaPhoto", "pyrogram.InputMediaVideo"]],
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_media_group* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_media_group(
                chat_id=message.chat.id,
                media=list_of_media
            )

        Example:
            .. code-block:: python

                message.reply_media_group(list_of_media)

        Args:
            media (``list``):
                A list containing either :obj:`InputMediaPhoto <pyrogram.InputMediaPhoto>` or
                :obj:`InputMediaVideo <pyrogram.InputMediaVideo>` objects
                describing photos and videos to be sent, must include 2–10 items.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

        Returns:
            On success, a :obj:`Messages <pyrogram.Messages>` object is returned containing all the
            single messages sent.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_media_group(
            chat_id=self.chat.id,
            media=media,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id
        )

    def reply_photo(
        self,
        photo: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: str = "",
        ttl_seconds: int = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_photo* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_photo(
                chat_id=message.chat.id,
                photo=photo
            )

        Example:
            .. code-block:: python

                message.reply_photo(photo)

        Args:
            photo (``str``):
                Photo to send.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet, or
                pass a file path as string to upload a new photo that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``bool``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            ttl_seconds (``int``, *optional*):
                Self-Destruct Timer.
                If you set a timer, the photo will self-destruct in *ttl_seconds*
                seconds after it was viewed.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            ttl_seconds=ttl_seconds,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    def reply_poll(
        self,
        question: str,
        options: List[str],
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_poll* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_poll(
                chat_id=message.chat.id,
                question="Is Pyrogram the best?",
                options=["Yes", "Yes"]
            )

        Example:
            .. code-block:: python

                message.reply_poll("Is Pyrogram the best?", ["Yes", "Yes"])

        Args:
            question (``str``):
                The poll question, as string.

            options (List of ``str``):
                The poll options, as list of strings (2 to 10 options are allowed).

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_poll(
            chat_id=self.chat.id,
            question=question,
            options=options,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

    def reply_sticker(
        self,
        sticker: str,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_sticker* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_sticker(
                chat_id=message.chat.id,
                sticker=sticker
            )

        Example:
            .. code-block:: python

                message.reply_sticker(sticker)

        Args:
            sticker (``str``):
                Sticker to send.
                Pass a file_id as string to send a sticker that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a .webp sticker file from the Internet, or
                pass a file path as string to upload a new sticker that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_sticker(
            chat_id=self.chat.id,
            sticker=sticker,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )


    def reply_video(
        self,
        video: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: str = "",
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: str = None,
        supports_streaming: bool = True,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_video(
                chat_id=message.chat.id,
                video=video
            )

        Example:
            .. code-block:: python

                message.reply_video(video)

        Args:
            video (``str``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet, or
                pass a file path as string to upload a new video that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 90 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_video(
            chat_id=self.chat.id,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    def reply_video_note(
        self,
        video_note: str,
        quote: bool = None,
        duration: int = 0,
        length: int = 1,
        thumb: str = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video_note* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_video_note(
                chat_id=message.chat.id,
                video_note=video_note
            )

        Example:
            .. code-block:: python

                message.reply_video_note(video_note)

        Args:
            video_note (``str``):
                Video note to send.
                Pass a file_id as string to send a video note that exists on the Telegram servers, or
                pass a file path as string to upload a new video note that exists on your local machine.
                Sending video notes by a URL is currently unsupported.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            length (``int``, *optional*):
                Video width and height.

            thumb (``str``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 90 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_video_note(
            chat_id=self.chat.id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    def reply_voice(
        self,
        voice: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: str = "",
        duration: int = 0,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_voice* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.send_voice(
                chat_id=message.chat.id,
                voice=voice
            )

        Example:
            .. code-block:: python

                message.reply_voice(voice)

        Args:
            voice (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio from the Internet, or
                pass a file path as string to upload a new audio that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Voice message caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (``int``, *optional*):
                Duration of the voice message in seconds.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the upload progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes uploaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`Message <pyrogram.Message>` is returned.
            In case the upload is deliberately stopped with :meth:`stop_transmission`, None is returned instead.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id

        return self._client.send_voice(
            chat_id=self.chat.id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            duration=duration,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )


    def edit(self, text: str, parse_mode: str = "", disable_web_page_preview: bool = None, reply_markup=None):
        """Bound method *edit* of :obj:`Message <pyrogram.Message>`

        Use as a shortcut for:

        .. code-block:: python

            client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text="hello",
            )

        Example:
            .. code-block:: python

                message.edit("hello")

        Args:
            text (``str``):
                New text of the message.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your message.
                Defaults to Markdown.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        return self._client.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )
    def edit_caption(
        self,
        caption: str,
        parse_mode: str = "",
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *edit_caption* of :obj:`Message <pyrogram.Message>`

        Use as a shortcut for:

        .. code-block:: python

            client.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.message_id,
                caption="hello"
            )

        Example:
            .. code-block:: python

                message.edit_caption("hello")

        Args:
            caption (``str``):
                New caption of the message.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your message.
                Defaults to Markdown.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        return self._client.edit_message_caption(
            chat_id=self.chat.id,
            message_id=self.message_id,
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )

    def edit_media(self, media: InputMedia, reply_markup: "pyrogram.InlineKeyboardMarkup" = None) -> "Message":
        """Bound method *edit_media* of :obj:`Message <pyrogram.Message>`

        Use as a shortcut for:

        .. code-block:: python

            client.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.message_id,
                media=media
            )

        Example:
            .. code-block:: python

                message.edit_media(media)

        Args:
            media (:obj:`InputMediaAnimation` | :obj:`InputMediaAudio` | :obj:`InputMediaDocument` | :obj:`InputMediaPhoto` | :obj:`InputMediaVideo`)
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        return self._client.edit_message_media(
            chat_id=self.chat.id,
            message_id=self.message_id,
            media=media,
            reply_markup=reply_markup
        )

    def edit_reply_markup(self, reply_markup: "pyrogram.InlineKeyboardMarkup" = None) -> "Message":
        """Bound method *edit_reply_markup* of :obj:`Message <pyrogram.Message>`

        Use as a shortcut for:

        .. code-block:: python

            client.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=inline_reply_markup
            )

        Example:
            .. code-block:: python

                message.edit_reply_markup(inline_reply_markup)

        Args:
            reply_markup (:obj:`InlineKeyboardMarkup`):
                An InlineKeyboardMarkup object.

        Returns:
            On success, if edited message is sent by the bot, the edited
            :obj:`Message <pyrogram.Message>` is returned, otherwise True is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        return self._client.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup
        )

    def forward(self,
                chat_id: int or str,
                disable_notification: bool = None):
        """Bound method *forward* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.forward_messages(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.message_id,
            )

        Example:
            .. code-block:: python

                message.forward(chat_id)

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

        Returns:
            On success, the forwarded Message is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        return self._client.forward_messages(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_ids=self.message_id,
            disable_notification=disable_notification
        )

    def delete(self, revoke: bool = True):
        """Bound method *delete* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.delete_messages(
                chat_id=chat_id,
                message_ids=message.message_id
            )

        Example:
            .. code-block:: python

                message.delete()

        Args:
            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        self._client.delete_messages(
            chat_id=self.chat.id,
            message_ids=self.message_id,
            revoke=revoke
        )

        return True

    def click(self, x: int or str, y: int = None, quote: bool = None):
        """Bound method *click* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for clicking a button attached to the message instead of.

        - Clicking inline buttons:

        .. code-block:: python

            client.request_callback_answer(
                chat_id=message.chat.id,
                message_id=message.message_id,
                callback_data=message.reply_markup[i][j].callback_data
            )

        - Clicking normal buttons:

        .. code-block:: python

            client.send_message(
                chat_id=message.chat.id,
                text=message.reply_markup[i][j].text
            )

        Example:
            This method can be used in three different ways:

            1.  Pass one integer argument only (e.g.: ``.click(2)``, to click a button at index 2).
                Buttons are counted left to right, starting from the top.

            2.  Pass two integer arguments (e.g.: ``.click(1, 0)``, to click a button at position (1, 0)).
                The origin (0, 0) is top-left.

            3.  Pass one string argument only (e.g.: ``.click("Settings")``, to click a button by using its label).
                Only the first matching button will be pressed.

        Args:
            x (``int`` | ``str``):
                Used as integer index, integer abscissa (in pair with y) or as string label.

            y (``int``, *optional*):
                Used as ordinate only (in pair with x).

            quote (``bool``, *optional*):
                Useful for normal buttons only, where pressing it will result in a new message sent.
                If ``True``, the message will be sent as a reply to this message.
                Defaults to ``True`` in group chats and ``False`` in private chats.

        Returns:
            -   The result of *request_callback_answer()* in case of inline callback button clicks.
            -   The result of *reply()* in case of normal button clicks.
            -   A string in case the inline button is an URL, switch_inline_query or switch_inline_query_current_chat
                button.

        Raises:
            :class:`Error <pyrogram.Error>`
            ``ValueError``: If the provided index or position is out of range or the button label was not found
            ``TimeoutError``: If, after clicking an inline button, the bot fails to answer within 10 seconds
        """
        if isinstance(self.reply_markup, pyrogram.ReplyKeyboardMarkup):
            return self.reply(x)
        elif isinstance(self.reply_markup, pyrogram.InlineKeyboardMarkup):
            if isinstance(x, int) and y is None:
                try:
                    button = [
                        button
                        for row in self.reply_markup.inline_keyboard
                        for button in row
                    ][x]
                except IndexError:
                    raise ValueError("The button at index {} doesn't exist".format(x)) from None
            elif isinstance(x, int) and isinstance(y, int):
                try:
                    button = self.reply_markup.inline_keyboard[y][x]
                except IndexError:
                    raise ValueError("The button at position ({}, {}) doesn't exist".format(x, y)) from None
            elif isinstance(x, str):
                x = x.encode("utf-16", "surrogatepass").decode("utf-16")

                try:
                    button = [
                        button
                        for row in self.reply_markup.inline_keyboard
                        for button in row
                        if x == button.text
                    ][0]
                except IndexError:
                    raise ValueError(
                        "The button with label '{}' doesn't exists".format(
                            x.encode("unicode_escape").decode()
                        )
                    ) from None
            else:
                raise ValueError("Invalid arguments")

            if button.callback_data:
                return self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.message_id,
                    callback_data=button.callback_data
                )
            elif button.url:
                return button.url
            elif button.switch_inline_query:
                return button.switch_inline_query
            elif button.switch_inline_query_current_chat:
                return button.switch_inline_query_current_chat
            else:
                raise ValueError("This button is not supported yet")
        else:
            raise ValueError("The message doesn't contain any keyboard")

    def download(self, file_name: str = "", block: bool = True, progress: callable = None, progress_args: tuple = ()):
        """Bound method *download* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.download_media(message)

        Example:
            .. code-block:: python

                message.download()

        Args:
            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            progress (``callable``):
                Pass a callback function to view the download progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Returns:
            On success, the absolute path of the downloaded file as string is returned, None otherwise.

        Raises:
            :class:`Error <pyrogram.Error>`
            ``ValueError``: If the message doesn't contain any downloadable media
        """
        return self._client.download_media(
            message=self,
            file_name=file_name,
            block=block,
            progress=progress,
            progress_args=progress_args,
        )
    def pin(self, disable_notification: bool = None) -> "Message":
        """Bound method *pin* of :obj:`Message <pyrogram.Message>`.

        Use as a shortcut for:

        .. code-block:: python

            client.pin_chat_message(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                message.pin()

        Args:
            disable_notification (``bool``):
                Pass True, if it is not necessary to send a notification to all chat members about the new pinned
                message. Notifications are always disabled in channels.

        Returns:
            True on success.

        Raises:
            :class:`RPCError <pyrogram.RPCError>`
        """
        return self._client.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
            disable_notification=disable_notification
        )

