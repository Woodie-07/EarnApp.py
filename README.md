# EarnApp.py
## Table of contents
* [General info](#general-info)
* [Documentation](#documentation)
* [Setup](#setup)

## General info
A python library to interact with the EarnApp API. 

# Known issues
- Currently, the showDevice function does not work

## Documentation
1) First, import the library: `from earnapp import earnapp`
2) Next, you can initialize a user. You can have as many users as you like and each user can have a different token. Initialize it with something: `user = earnapp.User()`
3) Log into the EarnApp account with `loggedIn = user.login("ENTER oauth-refresh-token HERE")`
4) The login function will return a boolean depending on the success. For example:
```
if loggedIn == True:
    print("Successfully logged in!")
else:
    print("Failed to log in")
```
5) Now, you can use whatever functions you like, for example `print("Money: " + str(user.money()))`

User Functions:
setProxy - Sets the proxy for the requests.
login - Logs in to the EarnApp account.
userData - Get data about the logged in user.
money - Get data about the logged in user's money
devices - Get data about the logged in user's devices
appVersions - Get the latest app version
paymentMethods - Get all available payment methods
transactions - Get past transactions and their status
linkDevice - Link a device to the logged in EarnApp account
hideDevice - Hide a device from the logged in EarnApp account
showDevice - Show a device on the logged in EarnApp account
renameDevice - Rename a device on the logged in EarnApp account
redeemDetails - Change the redeem details of the logged in EarnApp account
	
## Setup
To run this project, install it using pip:

```
$ pip3 install earnapp
```
