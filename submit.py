import requests
from bs4 import BeautifulSoup
import config
import os.path
import tempfile
import subprocess
import data

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
  # Get source path
  # source_path = f"../{name}/contest/{prob.upper()}.py"
  source_path = "test.py"
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
  inputs = samples[1::2]
  outputs = samples[2::2]
  return inputs, outputs

def test(inputs, outputs, source_path):
  def display_result(number, input, output, result):
    print(f"---Example{number+1}---")
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
    
    display_result(i, input, output, result)

def submit(source_code):
  header_info = {
    "User-Agent": "Mozilla/5.0"
  }
  submit_info["csrf_token"] = login_info["csrf_token"]
  submit_info["data.TaskScreenName"] = data.TASK_SCREEN_NAME
  submit_info["data.LanguageId"] = 4006 # This is Python language id
  submit_info["sourceCode"] = source_code
  
  session.post(data.SUBMIT_URL, data = submit_info, headers = header_info).raise_for_status()

  print("Submit!")

def main():
  login()
  source_path = get_source_path()
  source_code = get_source_code(source_path)
  inputs, outputs = get_data()
  test(inputs, outputs, source_path)
  submit(source_code)

main()