from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChatMemberUpdated


class UserActivityFilter(BoundFilter):
    key = 'user_activity'

    def __init__(self, user_activity: str):
        self.user_activity = user_activity

    async def check(self, event: ChatMemberUpdated) -> bool:
        if self.user_activity == 'banned_by_user':
            new = event.new_chat_member
            return new.status == 'kicked'
        elif self.user_activity == 'unbanned_by_user':
            old = event.old_chat_member
            new = event.new_chat_member
            return old.status == 'kicked' and new.status == 'member'
        elif self.user_activity == 'added_to_channel':
            new = event.new_chat_member
            return new.status == 'member'
        elif self.user_activity == 'deleted_from_channel':
            old = event.old_chat_member
            new = event.new_chat_member
            return old.status == 'member' and (new.status == 'kicked' or new.status == 'left')
