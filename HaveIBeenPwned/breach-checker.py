"""
@Author: wh1t3kn16ht (Stavros Gkounis)
@Tool: Breach-Checker
@Version: v1.2
@Description: This is a security tool that uses the "Have I Been Pawned? python library" in order to determined
              if the password or the email account of the user has been breached.

@Tested On: Parrot OS, Windows 10
@Python version: Python 2.7.16rc1, Python 3.7.2
@Library needed: pyhibp
"""

"""
|TODOs|:
"""

# |LIBRARIES|
import pyhibp
from pyhibp import pwnedpasswords
import json
import re
import os
import time
from optparse import OptionParser

"""
Data that the end user we want to see.
The knowledge of such information comes from the API itself.
"""
Data = ["Name","Title", "Domain", "DataClasses", "IsVerified", "IsFabricated", "IsSensitive", "IsRetired", "IsSpamList","Description"] # < --- Global list.

# |DECLARATION OF FUNCTION|
"""
@Function_Name: signature
@Parameters: None
@Description: This function just prints a ascii art and the author of the tool
"""
def signature():
  print("     .--------.                                                                                           ")
  print("    / .------. \                                                                                          ")
  print("   / /        \ \                                                                                         ")
  print("   | |        | |                                                                                         ")
  print("  _| |________| |_         ***************************************************************************    ")
  print(".' |_|        |_| '.        ___  ____ ____ ____ ____ _  _          ____ _  _ ____ ____ _  _ ____ ____     ")
  print("'._____ ____ _____.'        |__] |__/ |___ |__| |    |__|    __    |    |__| |___ |    |_/  |___ |__/     ")
  print("|     .'____'.     |        |__] |  \ |___ |  | |___ |  |          |___ |  | |___ |___ | \_ |___ |  \     ")
  print("'.__.'.'    '.'.__.'                                                                                      ")
  print("'.__  |      |  __.'                     written by wh1t3kn16ht (Stavros Gkounis)                         ")
  print("|   '.'.____.'.'   |       ***************************************************************************    ")
  print("'.____'.____.'____.'                                                                                      ")
  print("'.________________.'                                                                                      ")

"""
@Function_Name: trim_HTML_Tag
@Parameters: html
@Description: This function takes a string and trims the HTML tags and HTML symbols
"""
def trim_HTML_Tag(html):
    clean_html_tag = re.compile('<.*?>') # REGEX: Clean everything inside < >
    clean_html_symbols = re.compile('&.*?;') # REGEX: In case of copyright symbol (&copy;)
    no_html_tags = re.sub(clean_html_tag, '', html) # Substitute the tag with '' in the string provided by html variable.
    return re.sub(clean_html_symbols, '', no_html_tags)

"""
@Function_Name: haveTheEmailAccountBreached
@Parameters: email
@Description: The function takes a email account as a parameter and checks if the email account has been
              pwned using "Have I Been Pwned python library".
"""
def haveTheEmailAccountBeenBreached(email):
    resp = pyhibp.get_account_breaches(email) # It returns an json array of size 1 IF the account has been breached otherwise returns the boolean value false.
    if(resp):
        dictionary = resp[0] # Assign the simple json data to variable dictionary
        for detail in Data:
            if(isinstance(dictionary[detail],list)):
                print("    [+] {}:".format(detail))
                for item in dictionary[detail]: # Print every item of the list with tab character.
                    print("\t[>] {}".format(item))
            else:
                if(detail == "Description"):
                    print("    [+] {}: {}".format(detail,trim_HTML_Tag(dictionary[detail])))
                    continue # Do not print it again in the next statement. Say to for-loop to move on.
                print("    [+] {}: {}".format(detail,dictionary[detail]))
    else:
        print("    [ :) ] Your email account has not been pwned")

"""
@Function_Name: haveThePasswordBeenBreached
@Parameters: passwd
@Description: The function takes a password as a parameter and checks if the password has been pwned
              using the "Have I Been Pwned python library"
"""
def haveThePasswordBeenBreached(passwd):
    resp = pwnedpasswords.is_password_breached(passwd)
    if resp: # If the password has not been pwned, resp have the value false.
        print("    [+] Password Breached !!!")
        print("    [*] This password was used {} time(s) before.".format(resp))
    else:
        print("    [ :) ] You password has not been pwned")

"""
@Function_Name: arguments
@Parameters: None
@Description: The usage of this function is to give the functionality of giving values for the parameter
              of the other function from the command line interface (CLI)
"""
def arguments():
    parser = OptionParser()

    parser.add_option("-e", "--email", type='string', action='store', dest='Email',
                    help='Give the email account that you want to check if it has been pwned')

    parser.add_option("-p", "--pass", type='string', action='store', dest='Passwd',
                    help='Give the password that you want to check if it has been pwned')

    parser.add_option("--emaillist", type='string', action='store', dest='EmailList',
                    help='Give the a list of email accounts')

    parser.add_option("--passlist", type='string', action='store', dest='PassList',
                    help='Give a list of passwords')

    options,args = parser.parse_args()

    return options.Email, options.Passwd, options.EmailList, options.PassList

"""
@Function_Name: check_arguments
@Parameters: None
@Description: This function checks whether the user want to test a single email account or password, or a list of email accounts or passwords.
"""
def check_arguments():
    email, passwd, emailList, passList = arguments()
    # | Check Files |
    if(emailList is not None):
        check_email_list(emailList)

    if(passList is not None):
        check_password_list(passList)

    # | Check Email or Password |
    if(email is not None):
        print("\n[*] Checking Email")
        haveTheEmailAccountBeenBreached(email)

    if(passwd is not None):
        print("\n[*] Checking Password")
        haveThePasswordBeenBreached(passwd)

    if((email is None) and (passwd is None) and (emailList is None) and (passList is None)):
        print("\n[!] You have to specify at least one argument")
        print("[*] Usage : python breach-check.py -h")


"""
@Function_Name: check_email_list
@Parameters: emailList
@Description: This function checks the email accounts, that are provided by a file as a list, if they have been pwned.
"""
def check_email_list(emailList):
    with open(emailList,'r') as emailaccounts:
        email = emailaccounts.readline().strip() # strip newline character
        while(email):
            print(" \n[*] Checking Email: {}".format(email))
            haveTheEmailAccountBeenBreached(email)
            print('\n')
            email = emailaccounts.readline().strip()



"""
@Function_Name: check_password_list
@Parameters: passList
@Description: This function checks the passwords, that are provided by a file as a list, if they have been pwned.
"""
def check_password_list(passList):
    with open(passList,'r') as passwords:
        passwd = passwords.readline().strip()
        while(passwd):
            print(" \n[*] Checking Password: {}".format(passwd))
            haveThePasswordBeenBreached(passwd)
            print('\n')
            passwd = passwords.readline().strip()


"""
@Function_Name: main
@Parameters: None
@Description: This function checks the variables email and passwd that the user gave and if the
              corresponding variables are set the corresponding functions are called.
"""
def main():
    signature()
    check_arguments()

# |END OF DECLACTION OF FUNCTIONS|
# |SCRIPT EXECUTION SCOPE|
if(__name__ == "__main__"):
    main()
    #check_password_list("test00.txt")
else:
    print("[!] It is not supposed to be imported")
# |END OF SCRIPT EXECUTION SCOPE|
