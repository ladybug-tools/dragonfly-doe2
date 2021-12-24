from honeybee import typing as tp


class IpyDataClass(object):
    """WIP dataclass parent.
        TODO: override setattr to build in typing
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
