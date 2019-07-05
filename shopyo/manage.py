from utils.gen_modules import generate_modules
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("command", help="command to give")
# parser.add_argument("sec_param", help="the exponent")
args = parser.parse_args()


def exec_gen_modules():
    p = os.path.abspath(__file__)
    slash = os.path.sep
    path_now = slash.join(p.split(slash)[:-1])
    generate_modules(path_now, 'all')

commands = {
    'loadmodule': exec_gen_modules
}

if __name__ == '__main__':
    try:
        commands[args.command]()
    except KeyError:
        print('...')