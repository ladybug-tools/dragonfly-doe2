import re


def short_name(name, max_length):
    if len(name) <= max_length:
        return name

    shortened_name = ''.join(re.split('[aeiouy\-\_]', name))

    if len(shortened_name) <= max_length:
        return shortened_name

    shortened_name = ''.join(shortened_name.split())
    if len(shortened_name) > max_length:
        raise ValueError(
            f'{name} cannot be shorten to fit the eQuest limitation of 32 characters. '
            'You need to change the name manually to be shorter than 32 characters.'
        )
    return shortened_name
