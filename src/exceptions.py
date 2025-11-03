class GWBaseException(Exception): ...


class GWAlreadyInitiatedException(GWBaseException):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('GodWest already initiated!', *args, **kwargs)


class GWNotSetupedException(GWBaseException):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('Cannot run bot without setup', *args, **kwargs)
