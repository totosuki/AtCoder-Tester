import argparse
import config


root_path = config.PATH


def config_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('probrems', nargs="*")
  args = arg_parser.parse_args()
  return args


def clear(probrem: str):
  path = f"{root_path}/contest/{probrem}.py"

  with open(path, 'w') as file:
    file.write('')


def main():
  args = config_args()
  
  if len(args.probrems) == 0 or "all" in args.probrems:
    args.probrems = [*list("ABCDEFG"),"EX"]

  for probrem in args.probrems:
    clear(probrem.upper())

  print(f"{','.join(args.probrems)}をクリアしました。")


if __name__ == '__main__':
  main()