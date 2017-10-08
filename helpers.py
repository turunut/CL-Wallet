import sys
from pretty_print import colors, PrettyPrint
from replay import Replay

_ver = sys.version_info

is_py2 = (_ver[0] == 2)

is_py3 = (_ver[0] == 3)


def fetch_user_input(text):
    if is_py2:
        return raw_input(text)

    return input(text)


def pretty_print(text, *args, **kwargs):
    if 'color' in kwargs:
        # Might need to check if its a supported color
        return PrettyPrint(text, *args, **dict(kwargs, color=colors[kwargs['color']]))

    return PrettyPrint(text, *args, **kwargs)


def handle_replay(node, seed, command, transfers, **kwargs):
    # Check if a valid command
    arguments = command.split(' ', 1)
    t_id = None

    try:
        t_id = arguments[1]
    except IndexError:
        return pretty_print('Invalid command - See example usage.')

    bundle = None
    t_id = t_id.strip()

    for transfer in transfers:
        if transfer['short_transaction_id'] == t_id:
            bundle = transfer['bundle']
            break

    if bundle is None:
        return pretty_print(
            'Looks like there is no bundle associated with your specified short transaction id. Please try again'
        )

    pretty_print('Starting to replay your specified bundle. This might take a few second...', color='green')
    return Replay(
        node,
        seed,
        bundle,
        replay_callback=lambda: pretty_print('Successfully replayed your specified bundle!', color='blue')
    )