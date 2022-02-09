"""
@Author: wh1t3kn16ht (Stavros Gkounis)
@Tool: Profiler
@Version: v1.0
@Description: This tool asks the user to give some details about a person-user (as input) and produces possible password list (as output)
@Tested On: Ubuntu 18.04 LTS
"""

"""
Some Hypotheses:
1) I assume that if the user uses special symbols then these are located in the beginning or the end of the possible password.
2) I assume that if the user uses special symbols then he/she uses the same special character.
3) The assumption " 1) " is true for digits as well.
4) There is one entry for every key in the dictionary.
5) The additional information is only for one category.
6) It's 5-hour (max) project. So it's not going to be a full and practical custom wordlist creator.
"""

from datetime import datetime
import os

def signature():
    print(" ************************************************************")
    print("                   ╔═╗┬─┐┌─┐┌─┐┬┬  ┌─┐┬─┐                    ")
    print("                   ╠═╝├┬┘│ │├┤ ││  ├┤ ├┬┘                    ")
    print("                   ╩  ┴└─└─┘└  ┴┴─┘└─┘┴└─                    ")
    print(" ************************************************************")
    print("          written by wh1t3kn16ht (Stavros Gkounis)           ")


def giveDetailsAboutTheUser():
    """
    This function ask the user to add basic information about the target user.
    :return: the dictionary which contains the basic information about the target user.
    """
    userDetails = {} # Dictionary initialization

    # Start of Basic Information
    print("\n[!] Press Enter if you don't know the answer")
    userDetails['Name'] = input("[*] Enter the name of the user: ").lower()
    userDetails['Surname'] = input("[*] Enter the surname of the user: ").lower()
    userDetails['Birthday'] = input("[*] Enter the birth day of the user (Example DDMMYYYY): ")
    userDetails['Wife'] = input("[*] Enter the wife's name: ")
    userDetails['Kid'] = input("[*] Enter the name of the kid: ")
    userDetails['Pet'] = input("[*] Enter the name of the pet: ")
    # End of Basic Information

    return userDetails

def createThePossiblePasswordsAndAddThemInAFile(userDetails):
    """
    This function takes as parameter
    :param : userDetails, which is the dictionary provided by the giveDetailsAboutTheUser function
    and produces possible passwords for the target user and in the end writes them to a file.
    The passwords are a combination of digits, special symbols and additional word with the basic information
    about the target target.
    """
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    common_special_symbols = ["!", "@", "#", "$", "%", "^", "&", "*"]

    additionalWords = {} # dictionary initialization
    askUser = input("[*] Do you want to add any additional words such as adjectives etc ? (y/N): ")
    if( askUser == 'y' or askUser == 'Y'):
        print("\t[!] Enter any adjectives or words to be appended to specific user's detail\n\t(For Example enter 'sweet' if you want a password such as sweet[Pet's Name]")
        print("\t[!] The entry format must be (sweet sweetie ... Pet), that is the last word must indicate the category of user's detail")
        anyAdjectivesOrAdditionalWordsToBeAppended = input("\t[*] Enter the additional words: ").split(' ') # we using this line due to the format (sweet sweetie ... Pet) in order to prodcuce ['sweet', 'sweetie', ..., 'Pet'] list
        additionalWords[anyAdjectivesOrAdditionalWordsToBeAppended[-1]] = anyAdjectivesOrAdditionalWordsToBeAppended[:-1] # Populate the dictionary
        del anyAdjectivesOrAdditionalWordsToBeAppended # anyAdjectivesOrAdditionalWordsToBeAppended variable was a temporarily variable to help create the additionalWords dictionary

    fileName = 'wordlist_' + userDetails["Name"] + '.txt' # The filename would be, if the user's name is Adam, wordlist_Adam.txt
    if (os.path.exists(fileName)): # If the file exists delete it.
        os.remove(fileName)

    with open(fileName, 'w') as file: # opens the file and once the block is finished, it's going to close it.
        details = ['Name', 'Surname', 'Birthday', 'Birthday', 'Wife', 'Kid', 'Pet'] # Keys in the dictionary
        print("[+] File {} is created".format(fileName))
        print("[+] Creating & Writing the wordlist process has been started")
        startTime = datetime.now()

        # Just add the details, as they are, in the file:
        for detail in details:
            if(userDetails[detail] != ''):
                file.write(userDetails[detail] + '\n')

        #Let's combine the details we have we digits, special symbols and any additional words:
        for detail in details:
            if(userDetails[detail] != ''):
                for digit in digits:
                    file.write(digit + userDetails[detail] + '\n') # put the digit in the beginning
                    file.write(userDetails[detail] + digit + '\n') # put the digit in the end

                for specialSymbol in common_special_symbols:
                    file.write(specialSymbol + userDetails[detail] + '\n') # put the special symbol in the beginning
                    file.write(userDetails[detail] + specialSymbol + '\n') # put the special symbol in the end
                    file.write(specialSymbol + userDetails[detail] + specialSymbol + '\n') # surround the word with the special symbol

                for key in additionalWords:
                    if(detail == key.capitalize()): # Capitalize the key in order to match the userDetail dictionary's key
                        if(isinstance(additionalWords[key],list)): # Check if the value of the key is a list, because if it is we must to iterate it.
                            for value in additionalWords[key]:
                                file.write(value + userDetails[detail] + '\n')
                                file.write(userDetails[detail] + value + '\n')
                        else:
                            file.write(additionalWords[key] + userDetails[detail] + '\n')
                            file.write(userDetails[detail] + additionalWords[key] + '\n')
    finishTime = datetime.now()
    totalTime = finishTime - startTime
    print("[*] Creating & Writing process finished in: {}",format(totalTime))

def main():
    signature()
    createThePossiblePasswordsAndAddThemInAFile(giveDetailsAboutTheUser())

if(__name__ == "__main__"):
    main()