import argparse
import shutil
import config
import os


root_path = config.PATH


class Probrem:
  def __init__(self, contest: str, number: str, probrem: str) -> None:
    self.contest = self.adjust_contest_notation(contest)
    self.number = self.adjust_number_notation(number)
    self.probrem = self.adjust_probrem_notation(probrem)

  def adjust_contest_notation(self, contest: str):
    # 表記揺れを統一
    return contest.upper()
  
  def adjust_number_notation(self, number: str): 
    # 表記揺れを統一: 1 -> 001
    return number.zfill(3)

  def adjust_probrem_notation(self, probrem: str):
    # 表記揺れを統一
    return probrem.upper()


def config_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('contest', help='abc,arc,agc, etc...', type=str)
  arg_parser.add_argument('number', help='the contest number', type=str)
  arg_parser.add_argument('probrems', nargs="*")
  args = arg_parser.parse_args()
  return args


def copy(prob: Probrem):
  path = f"{root_path}/contest/{prob.probrem}.py"

  new_dir = f"{root_path}/{prob.contest}/{prob.probrem}"
  new_path = f"{new_dir}/{prob.number}.py"

  # ディレクトリが存在しない場合は新規作成
  if not os.path.exists(new_dir):
    os.makedirs(new_dir)

  shutil.copyfile(path, new_path)


def main():
  args = config_args()
  
  if len(args.probrems) == 0 or "all" in args.probrems:
    args.probrems = [*list("ABCDEFG"),"EX"]

  for probrem in args.probrems:
    copy(Probrem(args.contest, args.number, probrem))


if __name__ == '__main__':
  main()