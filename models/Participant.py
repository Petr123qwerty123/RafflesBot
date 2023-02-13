from .User import User
from .Raffle import Raffle


class Participant(object):
    def __init__(self,
                 user: User,
                 raffle: Raffle):
        self.user = user
        self.raffle = raffle

    def __str__(self):
        return f'{self.__class__.__name__}(' + \
               f'user={self.user}, ' + \
               f'raffle={self.raffle})'

    def __repr__(self):
        return f'{self.__class__.__name__}(' + \
               f'user={self.user}, ' + \
               f'raffle={self.raffle})'
