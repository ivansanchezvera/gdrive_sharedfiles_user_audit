import sys
import datetime

from main import main

def googleDriveAuditCLI():
    print("***GDrive Audit file Activities***")
    print("First We'll need some arguments from you to get the Activities from your Google Drive")
    print("Let's start with an initial date (earliest date) to start the filtering of GDrive Activities.")
    print()
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
    else:
        main(formatedStartDate, formatedEndDate)


def CLImain():
    googleDriveAuditCLI()

if __name__ == '__main__':
    CLImain()