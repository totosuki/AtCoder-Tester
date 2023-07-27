#!/bin/bash

escape_slash() {
  echo "$1" | sed 's/\//\\\//g'
}

write_to_env() {
  key="$1"
  value="$2"

  if [ -n "$value" ]; then
    value=$(escape_slash "$value")
    if grep -q "^$key=" .env; then
      sed -i '' "s/^$key=.*/$key=$value/" .env
    else
      echo "$key=$value" >> .env
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

env_file=".env"
if [ ! -e "$env_file" ]; then
  touch "$env_file"
fi

read -p "AtCoder username: " username
read -p "Login password: " password
read -p "Parent path of contest folder: " path
read -p "Do you want to create a contest folder in the entered path? (yes/no): " ok

write_to_env "username" "$username"
write_to_env "password" "$password"
write_to_env "path" "$path"

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
