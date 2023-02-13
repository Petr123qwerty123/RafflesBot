import datetime

from .User import User


class Admin(User):
    def __init__(self,
                 first_name: str,
                 registration_datetime: datetime.datetime,
                 last_name: str = None,
                 username: str = None,
                 alive: bool = True,
                 blocked: bool = False):
        super().__init__(first_name, registration_datetime, last_name, username, alive, blocked)

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
