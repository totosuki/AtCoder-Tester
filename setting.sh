#!/bin/bash

parent_dir=$1

escape_slash() {
  echo "$1" | sed 's/\//\\\//g'
}

write_to_env() {
  key="$1"
  value="$2"

  if [ -n "$value" ]; then
    value=$(escape_slash "$value")
    if grep -q "^$key=" $parent_dir/.env; then
      sed -i '' "s/^$key=.*/$key=$value/" $parent_dir/.env
    else
      echo "$key=$value" >> $parent_dir/.env
    fi
  fi
}

create_folder() {
  folder_name="$1"
  if [ ! -d "$folder_name" ]; then
    mkdir "$folder_name"
    echo "Create '$folder_name'"
  else
    echo "'$folder_name' already exists"
  fi
}

create_python_file() {
  folder_name="$1"
  file_name="$2"

  if [ ! -f "$folder_name/$file_name.py" ]; then
    touch "$folder_name/$file_name.py"
    echo "Create '$folder_name/$file_name.py'"
  else
    echo "'$folder_name/$file_name.py' already exists"
  fi
}

env_file=$parent_dir/.env
if [ ! -e "$env_file" ]; then
  touch "$env_file"
fi

read -p "AtCoder username: " username
read -p "Login password: " password
read -p "Parent path of contest folder: " path
read -p "Do you want to create a contest folder in the entered path? (yes/no): " ok
read -p "Type of Python (cpython/pypy): " python

write_to_env "username" "$username"
write_to_env "password" "$password"
write_to_env "path" "$path"

if test "$python" = "cpython" ; then
  read -p "Which of CPython do you use? (old/new): " version
  if test "$version" = "old" ; then
    write_to_env "language" "4006"
  elif test "$version" = "new" ; then
    write_to_env "language" "5055"
  fi
elif test "$python" = "pypy" ; then
  read -p "Which of PyPy do you use? (old/new): " version
  if test "$version" = "old" ; then
    write_to_env "language" "4047"
  elif test "$version" = "new" ; then
    write_to_env "language" "5078"
  fi
fi

if test "$ok" = "yes" ; then
  create_folder "$path/contest"

  create_python_file "$path/contest" "A"
  create_python_file "$path/contest" "B"
  create_python_file "$path/contest" "C"
  create_python_file "$path/contest" "D"
  create_python_file "$path/contest" "E"
  create_python_file "$path/contest" "F"
  create_python_file "$path/contest" "G"
  create_python_file "$path/contest" "EX"
fi

echo "Setup complete"
