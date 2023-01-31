# Purpose
This small program uses the Google Drive API, Google Drive Activities API, Google Contacts and People API to list information
about your files or files shared with you and perform queries given certain parameters that will display information related to your
google Drive files, who do you share them with (if the person is in your contacts), activities performed on the files and more.

## Requisites
For it to work, you need to install and configure de [gcloud tools](https://cloud.google.com/sdk/gcloud).
Here are official instructions to [install the gcloud cli](https://cloud.google.com/sdk/docs/install).
You also need python installed, [pyenv](https://github.com/pyenv/pyenv) and [virtualenv](https://virtualenv.pypa.io/en/latest/) are highly suggested, so you don't mess your python env.
Also, you need to have your own google account on drive with appropiate credentials and permissions to test.
Finally, you'll need a [google cloud account](https://console.cloud.google.com).

# How to Use
## Via CLI
It is suggested that you create a new env for this.  
For example, using pyenv, I downloaded version 3.10.7  
```pyenv install 3.10.7```  
Then I created a new Virtualenv using this python version I just downloaded with pyenv:  
```pyenv virtualenv 3.10.7 google-drive-audit-logs-3.10.7```
Execute:  
```python cli.py```
Follow the instructions in the CLI.

## Via Functions
Open the python terminal:  
```python```
```from main import main```
```main()```

You can override the default values with your own.
When you first use the solution, It will ask you to authenticate via web browser via the Google Auth site.
Login with your credentials, allow the appropiate permissions to read data from your Google Drive, Google Drive Activity and People/Contacts.
Some warnings might arise, be sure to read them and understand the implications of the access given.

You can also extend your own classes or functions, by using or modifying the `consolidateGDriveInformation()` function on `main.py`.
