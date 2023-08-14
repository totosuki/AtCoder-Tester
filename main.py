import requests
from bs4 import BeautifulSoup
import config
import os.path
import tempfile
import subprocess
import data
import re

login_info = dict()
submit_info = dict()

# Start session
session = requests.session()

def login():
  res = session.get(data.LOGIN_URL)
  soup = BeautifulSoup(res.text, 'lxml')
  csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')

  login_info["csrf_token"] = csrf_token
  login_info["username"] = config.USERNAME
  login_info["password"] = config.PASSWORD

  # Login
  session.post(data.LOGIN_URL, data = login_info).raise_for_status()
  
  print("Login!", end = "\n\n")

def get_source_path():
  source_path = f"{config.PATH}/contest/{data.problem.upper()}.py"
  return source_path

def get_source_code(source_path):
  if os.path.exists(source_path):
      # read source path
      f = open(source_path)
      source_code = f.read()
      return source_code
  else:
      print("File to submit is not found.")
      quit()

def get_data():
  res = session.get(data.PROB_URL)
  soup = BeautifulSoup(res.content, "lxml")
  samples = [tag.text.strip() for tag in soup.find_all("pre")]
  samples = samples[:len(samples)//2]
  inputs = [re.sub("\r", "", input) for input in samples[1::2]]
  outputs = [re.sub("\r", "", output) for output in samples[2::2]]
  return inputs, outputs

def test(inputs, outputs, source_path) -> bool:
  wa_case = list()
  number_of_case = len(inputs)

  def display_result(number, input, output, result, is_ac):
    print(f"----- Example {number+1} -----")
    print("AC") if is_ac else print("WA")
    print("<Input>")
    print(input.strip())
    print("<Output>")
    print(output.strip())
    print("<Result>")
    print(result.strip())
    print("")

  for i, (input, output) in enumerate(zip(inputs, outputs)):
    with tempfile.TemporaryFile(mode = "w") as f:
      f.write(input)
      f.seek(0)
      try:
        result = subprocess.run(
          ["python3", source_path],
          stdin = f,
          encoding = "UTF-8",
          stdout = subprocess.PIPE,
          check = True
        ).stdout
      except subprocess.CalledProcessError:
        raise Exception("The code has an error")
    
    input, output, result = map(str.strip, [input, output, result])
    is_ac = output == result

    if not is_ac:
      wa_case.append(i+1)
    
    display_result(i, input, output, result, is_ac)
  
  if len(wa_case) == 0:
    print("All AC!!", end = "\n\n")
    return True
  else:
    for case in wa_case:
      print(f"Example {case} is WA...")
    return False

def submit(source_code):
  header_info = {
    "User-Agent": "Mozilla/5.0"
  }
  submit_info["csrf_token"] = login_info["csrf_token"]
  submit_info["data.TaskScreenName"] = data.TASK_SCREEN_NAME
  submit_info["data.LanguageId"] = config.LANGUAGE
  submit_info["sourceCode"] = source_code
  
  session.post(data.SUBMIT_URL, data = submit_info, headers = header_info).raise_for_status()

  print("Submit!")

def main():
  login()
  source_path = get_source_path()
  source_code = get_source_code(source_path)
  inputs, outputs = get_data()
  can_submit = test(inputs, outputs, source_path)
  if can_submit and data.mode == "submit":
    submit(source_code)
  elif data.mode == "submit":
    print("\nExample is not All AC\nSo submit is not possible...")

main()