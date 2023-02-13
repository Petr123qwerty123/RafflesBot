import datetime
import typing

from . import Channel, Participant


class Raffle(object):
    def __init__(self,
                 start_datetime: datetime.datetime,
                 end_datetime: datetime.datetime,
                 number_of_winners: int,
                 description: str = None,
                 image_url: str = None):
        self.raffle_id: typing.Optional[int] = None

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.number_of_winners = number_of_winners
        self.description = description
        self.image_url = image_url

        self.channels: typing.List[Channel] = []
        self.participants: typing.List[Participant] = []

    @property
    def full_description(self):
        end_datetime = f'Дата завершения розыгрыша: <i>{self.end_datetime + datetime.timedelta(hours=3)} МСК</i>'
        number_of_winners = f'Количество победителей: <i>{self.number_of_winners}</i>'
        instruction = '<b>Чтобы принять участие в розыгрыше подпишитесь на каналы из списка ниже ' \
                      'и перейдите по кнопке:</b>'
        channels = '\n'.join([f'{i}. <a href="{channel.link}">{channel.title}</a>'
                              for i, channel in enumerate(self.channels, 1)])

        return '\n\n'.join(
            list(
                filter(
                    lambda x: x is not None,
                    [self.description, end_datetime, number_of_winners, instruction, channels]
                )
            )
        )

    def __str__(self):
        return f'{self.__class__.__name__}(' + \
               f'raffle_id={self.raffle_id}, ' + \
               f'start_datetime={self.start_datetime}, ' + \
               f'end_datetime={self.end_datetime}, ' + \
               f'number_of_winners={self.number_of_winners}, ' + \
               f'description={self.description}, ' + \
               f'image_url={self.image_url}, ' + \
               f'channels={self.channels}, ' + \
               f'participants={self.participants})'

    def __repr__(self):
        return f'{self.__class__.__name__}(' + \
               f'raffle_id={self.raffle_id}, ' + \
               f'start_datetime={self.start_datetime}, ' + \
               f'end_datetime={self.end_datetime}, ' + \
               f'number_of_winners={self.number_of_winners}, ' + \
               f'description={self.description}, ' + \
               f'image_url={self.image_url}, ' + \
               f'channels={self.channels}, ' + \
               f'participants={self.participants})'
