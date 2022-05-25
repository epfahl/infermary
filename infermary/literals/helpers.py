'''Helper functions for type inference and casting of string literals'''

from infermary.exceptions import InvalidLiteralError


def check_and_prepare_literal(literal):
    '''Return the string after stripping leading and trailing whitespace.'''
    if not isinstance(literal, str):
        raise InvalidLiteralError(
            f"The input {literal} must be a string, not a value of type "
            f"'{type(literal).__name__}'."
        )
    return literal.strip()
