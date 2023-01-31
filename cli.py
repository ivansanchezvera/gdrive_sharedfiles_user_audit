import sys
import datetime

from main import main
from corpora import CorporaEnum

def googleDriveAuditCLI():
    print("***GDrive Audit file Activities***")
    print("First We'll need some arguments from you to get the Activities from your Google Drive")
    print("Let's start with an initial date (earliest date) to start the filtering of GDrive Activities.")
    print()
    try:
        # Dates
        print("Please insert the initial date in the ddmmyyyy format (ex 22112010): ")
        startDate = input()
        formatedStartDate = datetime.datetime.strptime(startDate, "%d%m%Y") #.date()
        print(f"Great, initial date is {formatedStartDate}")
        print()
        print("Nice, now please provide the end date in the ddmmyyyy format (ex 22112010) to filter the GDrive Activity: ")
        endDate = input()
        formatedEndDate = datetime.datetime.strptime(endDate, "%d%m%Y") #.date()
        print(f"Ok, End date is {formatedEndDate}")
        if(formatedStartDate>formatedEndDate):
            print("Sorry your End Date is earlier than the Start date", file=sys.stderr)
            print("\n\n\n")
            googleDriveAuditCLI()
        # End of Dates

        print("Finally, provide an integer number for the number of files to provide (default value is 10, max supported is 1000) ")
        numberOfFiles = int(input())
        corporaAsEnum = CorporaEnum.user
        owner = None
        print()

        while True:
            print("Do you wish to add further constrains? (y/n)")
            furtherConstrains = input()
            if(furtherConstrains == "y"):
                # Corpora
                print("Do you want to change the scope of the search (my user, my drive, my domain, all drives)? (y/n)")
                filterBySearchScope = input()
                if(filterBySearchScope == "y"):
                    print(f"Please provide a scope for the search as int, options are: {[member for member in CorporaEnum]}. Currently only options 1 and 4 are supported. Defualt is 1.")
                    corpora = int(input())
                    corporaAsEnum = CorporaEnum(corpora)
                    print(f"Corpora chosen is: {corporaAsEnum}")
                    print()
                
                print("Do you want to search or filter by owner (using gdrive email address)? (y/n)")
                filterByOwner = input()
                if(filterByOwner == "y"):
                    print(f"""Please provide a file owner to filter by. If you want to filter your own files, enter your own email associated to this google drive. 
                    If you want to filter by other possible file owners, please provide their emails.
                    Note that this feature works only if you and the other profile both have ownership of the file""")
                    print("Now enter the email to filter by:")
                    owner = input()
                    print(f"Owner is: {owner}")
                    print()
            else:
                break

        main(formatedStartDate, formatedEndDate, numberOfFiles, corporaAsEnum, owner)
        
    except ValueError as valueError:
        print("Value error, please try again conforming the input to the type constraints indicated in the prompt.", file=sys.stderr)
        print(f"Error is: {valueError}")
    except Exception as error:
        print("Unhandled error, please contact developer.", file=sys.stderr)
        print(f"Error is: {error}")


def CLImain():
    googleDriveAuditCLI()

if __name__ == '__main__':
    CLImain()