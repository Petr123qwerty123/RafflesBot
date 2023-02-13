import datetime
import typing


class User(object):
    def __init__(self,
                 first_name: str,
                 registration_datetime: datetime.datetime,
                 last_name: str = None,
                 username: str = None,
                 alive: bool = True,
                 blocked: bool = False):
        self.user_id: typing.Optional[int] = None

        self.registration_datetime = registration_datetime
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.alive = alive
        self.blocked = blocked

    def __str__(self):
        return f'{self.__class__.__name__}(' + \
               f'user_id={self.user_id}, ' + \
               f'first_name={self.first_name}, ' + \
               f'registration_datetime={self.registration_datetime}, ' + \
               f'last_name={self.last_name}, ' + \
               f'username={self.username}, ' + \
               f'alive={self.alive}, ' + \
               f'blocked={self.blocked})'

    def __repr__(self):
        return f'{self.__class__.__name__}(' + \
               f'user_id={self.user_id}, ' + \
               f'first_name={self.first_name}, ' + \
               f'registration_datetime={self.registration_datetime}, ' + \
               f'last_name={self.last_name}, ' + \
               f'username={self.username}, ' + \
               f'alive={self.alive}, ' + \
               f'blocked={self.blocked})'
