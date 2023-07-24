import argparse
from dataclasses import dataclass

@dataclass
class Contest:
  contest: str
  number: int


def main():
  c = get_contest()
  print(c)
  pass


def get_contest():
  args = config_args()
  return Contest(args.contest, args.number)


def config_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('contest', help='abc,arc,agc, etc...', type=str)
  arg_parser.add_argument('number', help='the contest number', type=int)
  args = arg_parser.parse_args()
  return args


if __name__ == '__main__':
  main()