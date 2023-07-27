import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--contest", default = "abc", help = "Contest Name [default = abc]")
parser.add_argument("number", help = "Contest number")
parser.add_argument("problem", help = "Problem alphabet")
parser.add_argument("-m", "--mode", default = "test", choices = ["test", "submit"], help = "Select mode [default = test] [test : Sample case test only] [submit : Automatically submit when sample case is All AC]")

args = parser.parse_args()
contest = args.contest
number = args.number
problem = args.problem
mode = args.mode

LOGIN_URL = 'https://atcoder.jp/login'
PROB_URL = "https://atcoder.jp/contests/{}{}/tasks/{}{}_{}".format(contest.lower(), number.zfill(3), contest.lower(), number.zfill(3), problem.lower())
SUBMIT_URL = "https://atcoder.jp/contests/{}{}/submit".format(contest.lower(), number.zfill(3))

TASK_SCREEN_NAME = "{}{}_{}".format(contest.lower(), number.zfill(3), problem.lower())