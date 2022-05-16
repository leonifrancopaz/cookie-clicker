import argparse
import base64
import json
import sys


def pair(string, maxpair=-1):
    '''Make a list out of a string where each item is a pair characters.'''
    single_list = list(string)
    double_list = []

    if maxpair == -1:
        while len(single_list) != 0:
            double_list.append(''.join(single_list[:2]))
            del single_list[:2]
    else:
        for i in range(maxpair):
            double_list.append(''.join(single_list[:2]))
            del single_list[:2]
        else:
            double_list.append(''.join(single_list))

    return double_list


def decode(input_path, output_path=None):
    '''Decode a Cookie Clicker save code from Base64 format.'''
    # Open the save file and read it.
    with open(input_path, 'rt') as save_file:
        save = save_file.read()

    # Change some parts of the string for proper decoding.
    save = save.replace('%21END%21', '')
    save = save.replace('%3D', '=')

    # Decode from Base64 format.
    save = save.encode()
    save = base64.b64decode(save)
    save = save.decode()

    # Write the decoded save code.
    output_path = input_path if not output_path else output_path
    with open(output_path, 'wt') as save_file:
        save_file.write(save)


def encode(input_path, output_path=None):
    '''Encode a Cookie Clicker save code to Base64 format.'''
    # Open the save file and read it.
    with open(input_path, 'rt') as save_file:
        save = save_file.read()

    # Encode to Base64 format.
    save = save.encode()
    save = base64.b64encode(save)
    save = save.decode()

    # Change some parts of the string for proper encoding.
    save = save.replace('=', '%3D')
    save = save + '%21END%21'

    # Write the encoded save code and close the save file.
    output_path = input_path if not output_path else output_path
    with open(output_path, 'wt') as save_file:
        save_file.write(save)


def arrange(input_path, output_path=None):
    '''Rearrange a Base64 decoded save to a readable format.'''
    with open(input_path, 'rt') as save_file:
        data = save_file.read()

    # Data of depth 0.
    data = data.split('|')

    # Data of depth 1.
    for index in (2, 4, 5, 8, 9):
        if ((index == 8) or (index == 9)) and not data[index]:
            data[index] = []
            continue

        data[index] = data[index].split(';')

        if index in (4, 5, 8, 9):
            if (index == 8 or index == 9) and not data[index]:
                continue

            del data[index][-1]

    data[6] = pair(data[6])

    # Data of depth 2.
    data[5] = [dataset.split(',') for dataset in data[5]]

    # Pair data with its corresponding metadata.
    metadata_file = open('metadata.json', 'rt')
    metadata = json.load(metadata_file)
    metadata_file.close()

    save = {}
    for section, dataset in zip(metadata['Sections'], data):
        if section in ('Version', 'N/A', 'Buffs', 'Mod data'):
            save[section] = dataset
            continue

        if section == 'Buildings':
            save[section] = {}
            for building, dataset in zip(metadata[section], data[5]):
                package = zip(metadata['Buildings data'], dataset)
                save[section][building] = dict(package)

            continue

        package = zip(metadata[section], dataset)
        save[section] = dict(package)

    # Python dict to JSON string representation.
    save = json.dumps(save, indent=4)

    # Applying some changes for readability.
    edited_save = ''
    sections = metadata['Sections'][1:]
    for line in save.splitlines():
        if any((section in line for section in sections)):
            edited_save += '\n' + line + '\n'
        else:
            edited_save += line + '\n'

    output_path = input_path if not output_path else output_path
    with open(output_path, 'wt') as save_file:
        save_file.write(edited_save)


def disarrange(input_path, output_path=None):
    '''Rearrange a Base64 decoded save to its original format.'''
    with open(input_path) as save_file:
        save = save_file.read()

    # JSON string representation to Python dict.
    save = json.loads(save)

    # Join data of depth 2.
    for building in save['Buildings']:
        building_values = save['Buildings'][building].values()
        save['Buildings'][building] = ','.join(building_values)

    # Join data of depth 1.
    save['Version'] = save['Version'] + '|'
    save['N/A'] = save['N/A'] + '|'
    save['Save stats'] = ';'.join(save['Save stats'].values()) + '|'
    save['Settings'] = ''.join(save['Settings'].values()) + '|'
    save['Stats'] = ';'.join(save['Stats'].values()) + ';|'
    save['Buildings'] = ';'.join(save['Buildings'].values()) + ';|'
    save['Upgrades'] = ''.join(save['Upgrades'].values()) + '|'
    save['Achievements'] = ''.join(save['Achievements'].values()) + '|'
    save['Buffs'] = ';'.join(save['Buffs'])
    save['Mod data'] = ';'.join(save['Mod data'])

    save['Buffs'] += ';' if save['Buffs'] else '' + '|'
    save['Mod data'] += ';' if save['Mod data'] else ''

    # Join data of depth 0.
    save = ''.join(save.values())

    output_path = input_path if not output_path else output_path
    with open(output_path, 'wt') as save_file:
        save_file.write(save)


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(
        'cookie_cliker',
        description=('Python script that aims to provide simple tools to '
                     'manipulate Cookie Clicker save files.')
    )

    cli_subparsers = cli_parser.add_subparsers()

    # Decode subcommand.
    decode_parser = cli_subparsers.add_parser(
        'decode',
        help='decode a Cookie Clicker save code from Base64 format',
    )
    decode_parser.add_argument(
        'decode_input',
        type=str,
        help='name of the file to be used as input',
        metavar='INPUT'
    )
    decode_parser.add_argument(
        '-o', '--output',
        default=None,
        type=str,
        required=False,
        help='name of the file that will be output',
        metavar='',
        dest='decode_output'
    )

    # Encode subcommand.
    encode_parser = cli_subparsers.add_parser(
        'encode',
        help='encode a Cookie Clicker save code to Base64 format'
    )
    encode_parser.add_argument(
        'encode_input',
        type=str,
        help='name of the file to be used as input',
        metavar='INPUT'
    )
    encode_parser.add_argument(
        '-o','--output',
        default=None,
        type=str,
        required=False,
        help='name of the file that will be output',
        metavar='',
        dest='encode_output'
    )

    # Arrange subcommand.
    arrange_parser = cli_subparsers.add_parser(
        'arrange',
        help='rearrange a Base64 decoded save to a readable format'
    )
    arrange_parser.add_argument(
        'arrange_input',
        type=str,
        help='name of the file to be used as input',
        metavar='INPUT'
    )
    arrange_parser.add_argument(
        '-o', '--output',
        default=None,
        type=str,
        required=False,
        help='name of the file that will be output',
        metavar='',
        dest='arrange_output'
    )

    # Disarrange subcommand.
    disarrange_parser = cli_subparsers.add_parser(
        'disarrange',
        help='rearrange a Base64 decoded save to its original format'
    )
    disarrange_parser.add_argument(
        'disarrange_input',
        help='name of the file to be used as input',
        metavar='INPUT'
    )
    disarrange_parser.add_argument(
        '-o', '--output',
        default=None,
        type=str,
        required=False,
        help='name of the file that will be output',
        metavar='',
        dest='disarrange_output'
    )

    cli_parser = cli_parser.parse_args()

    if 'decode_input' in dir(cli_parser):
        decode(cli_parser.decode_input, cli_parser.decode_output)
        print('Decoding succesful.')
    elif 'encode_input' in dir(cli_parser):
        encode(cli_parser.encode_input, cli_parser.encode_output)
        print('Encoding succesful.')
    elif 'arrange_input' in dir(cli_parser):
        arrange(cli_parser.arrange_input, cli_parser.arrange_output)
        print('Arrangement succesful.')
    elif 'disarrange_input' in dir(cli_parser):
        disarrange(cli_parser.disarrange_input, cli_parser.disarrange_output)
        print('Disarrangement succesful.')
