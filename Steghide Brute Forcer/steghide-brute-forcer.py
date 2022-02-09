#!/usr/bin/env python

"""
@Author: wh1t3kn16ht (Stavros Gkounis)
@Project: Steghide File Brute Forcer
@Technique: Dictionary Attack
@Tested on: Ubuntu 18.04 LTS
@Description: This tool takes as input the stegfile and a dictionary containing possible passwords.
              Using the brute force technique it tries to find the password in order to crack the
              stegfile and extract the embeded message.
"""

import commands
import os
from optparse import OptionParser
import platform

def signature():
  print("\033[1;91m" +"------------------------------------------------------------------------------------------------" + "\033[0m")
  print("\033[1;91m" + "____ ___ ____ ____ _  _ _ ___  ____    ___  ____ _  _ ___ ____    ____ ____ ____ ____ ____ ____ " + "\033[0m")
  print("\033[1;91m" + "[__   |  |___ | __ |__| | |  \ |___    |__] |__/ |  |  |  |___    |___ |  | |__/ |    |___ |__/ " + "\033[0m")
  print("\033[1;91m" + "___]  |  |___ |__] |  | | |__/ |___    |__] |  \ |__|  |  |___    |    |__| |  \ |___ |___ |  \ " + "\033[0m")
  print("\033[1;91m" + "------------------------------------------------------------------------------------------------" + "\033[0m")
  print("\033[1;93m" + "                            written by wh1t3kn16ht (Stavros Gkounis)                            " + "\033[0m")

def checkIfOutputFileExistsAndRemoveIt(file):
  if(os.path.exists(file)):
    os.remove(file)

"""
| Script Usage |:
./steghide-brute-forcer.py -f [stegfile] -d [dictionary] -o [output file]
./steghide-brute-forcer.py --stegfile [stegfile] --dictionary [dictionary]  --output [output file]
python steghide-brute-forcer.py -f [stegfile] -d [dictionary] -o [output file]
python steghide-brute-forcer.py --stegfile [stegfile] --dictionary [dictionary]  --output [output file]
"""

def arguments():
  parser=OptionParser()
  parser.add_option('-f', '--stegfile', type='string', action='store', dest='StegFile',
                    help="Provide the cover file where the secret message is embeded")
  parser.add_option('-d', '--dictionary', type='string', action='store', dest='Dictionary',
                    help="Provice the dictionary file")
  parser.add_option('-o','--output', type='string', action='store', dest='OutputFile', help="Provide the output file (optional)")
  options,args=parser.parse_args()
  return options.StegFile, options.Dictionary, options.OutputFile

def ifTheMainParametersAreNonePrintColoredErrorMessageAndExitOtherwiseMoveOn(sf,df):
  moveOn=False
  if((sf is None) or (df is None)):
    print('\033[1;91m' + '[!] You have to specify the StegFile and the Dictionary' + '\033[0m')
  elif(os.path.exists(sf) and os.path.exists(df)):
    moveOn=True
  else:
    print('\033[1;91m' + '[!] One of the files you specified does not exists' + '\033[0m')
  return moveOn

def successOrFailure(out,passwd):
  if("could not" not in out):
    print('\033[1;92m' + '[+] Message Retrieved using password "{}"'.format(passwd) + '\033[0m')
  else:
    print('\033[1;91m' + '[-] Password "{}" failed'.format(passwd) + '\033[0m')

def checkPasswordFromDictionaryAndIfSuccessWriteTheOutputToAFile(sf,df,outFile):
  out=''
  with open(df,'r') as passlist:
    for passwd in passlist.readlines():
      passphrase=passwd.split('\n') # returns an array ['passwd','']
      out = commands.getoutput('steghide extract -sf {} -xf {} -p "{}"'.format(sf,outFile,passphrase[0])) # Linux command line output
      successOrFailure(out,passphrase[0])

def printColoredWarningMessage():
  print('\n' + '\033[1;93m' + "[!] Program is interrupted" + '\033[0m')

def bruteForce():
  print('\n') # Don't try to figure out why I added a newline. It's for code beauty purposes
  try:
    steghideFile, dictionaryFile, outputFile = arguments()
    if(outputFile is None):
      outputFile='secret' # Set a fixed file name in case the user does not specify a output file.
    checkIfOutputFileExistsAndRemoveIt(outputFile)
    if(ifTheMainParametersAreNonePrintColoredErrorMessageAndExitOtherwiseMoveOn(steghideFile,dictionaryFile)):
      checkPasswordFromDictionaryAndIfSuccessWriteTheOutputToAFile(steghideFile,dictionaryFile,outputFile)
  except KeyboardInterrupt:
    printColoredWarningMessage()

def main():
  signature()
  bruteForce()

if(__name__=="__main__"):
  if(platform.system() == 'Windows'):
    print("Sorry this is only for Linux machines")
  elif(platform.system() == 'Linux'):
    os.system('clear')
    main()
  else:
    main()
