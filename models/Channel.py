import typing


class Channel(object):
    def __init__(self,
                 title: str,
                 link: str):
        self.channel_id: typing.Optional[int] = None

        self.title = title
        self.link = link

    def __str__(self):
        return f'{self.__class__.__name__}(' + \
               f'channel_id={self.channel_id}, ' + \
               f'title={self.title}, ' + \
               f'link={self.link})'

    def __repr__(self):
        return f'{self.__class__.__name__}(' + \
               f'channel_id={self.channel_id}, ' + \
               f'title={self.title}, ' + \
               f'link={self.link})'
