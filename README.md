# User-Gen
User generation in the form of username, password and email formated in JSON.

The objective of this script is to meke the usernames as legitimate as possible.
This is achivable by using a complex probability tree in the creation of the string.

In terms of the password, a consistent algorithm is used and given only the username 
as input. It is recommended to change the password generation function if this script 
is intended to be used for personal reasons.

positional arguments:
  Count                 the number of generated users

optional arguments:
  -h, --help            show this help message and exit
  -p USERNAME, --passwd USERNAME
                        check the password of the inputed user name
  -o PATH, --output PATH
                        file to output the users in JSON format
  -n PATH, --names PATH
                        JSON file with various names and surnames
  -j PATH, --joiner PATH
                        JSON file with joiners of names and surnames
  -su PATH, --suffix PATH
                        file with various suffixes added to the usernames
  -pre PATH, --prefix PATH
                        file with various prefixes added to the usernames
