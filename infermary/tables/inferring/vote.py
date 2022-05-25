'''Library for voting for the most likely column types.'''


def _pop(dct, key, default=None):
    '''Pop a value from a dictionary and return both the popped value and the
    updated dictionary.  The original dictionary is unchanged.'''
    cdct = dct.copy()
    value = cdct.pop(key, default)
    return value, cdct


def vote(counter):
    '''Return the non-missing type with the most counts, or the missing type
    if the "missing" type is present.'''
    _, counter = _pop(counter, 'missing', default=0)
    if not counter:
        return 'missing'
    return counter.most_common(1)[0][0]
