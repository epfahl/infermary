'''Custom exceptions.
'''


class CastError(Exception):
    pass


class InvalidLiteralError(Exception):
    pass


class UnregisteredTypeError(Exception):
    pass


class TableFormatError(Exception):
    pass


class FatalCastError(Exception):
    pass
