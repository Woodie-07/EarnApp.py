# EarnApp.py
PyPI Link: https://pypi.org/project/EarnApp/
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
3) Log into the EarnApp account with `user.login("ENTER oauth-refresh-token HERE")`
4) The login function will return a IncorrectTokenException if the token is incorrect.
```
try:
    user.login("ENTER oauth-refresh-token HERE")
except earnapp.IncorrectTokenException:
    print("Incorrect token")
    raise SystemExit
```
5) Now, you can use whatever functions you like, for example `print("Money: " + str(user.money()))`

User Functions:
- setProxy - Sets the proxy for the requests.
- login - Logs in to the EarnApp account.
- userData - Get data about the logged in user.
- money - Get data about the logged in user's money
- devices - Get data about the logged in user's devices
- appVersions - Get the latest app version
- paymentMethods - Get all available payment methods
- transactions - Get past transactions and their status
- linkDevice - Link a device to the logged in EarnApp account
- hideDevice - Hide a device from the logged in EarnApp account
- showDevice - Show a device on the logged in EarnApp account
- renameDevice - Rename a device on the logged in EarnApp account
- redeemDetails - Change the redeem details of the logged in EarnApp account

Exceptions:
- IncorrectTokenException - Raised when the token is incorrect
- RatelimitedException - Raised when the IP is ratelimited
- JSONDecodeErrorException - Raised when the JSON data returned by the EarnApp API is invalid
- XRSFErrorException - Raised when the script fails to retrieve an XRSF token

You can set a timeout for the requests with user.timeout, for example, to set the timeout to 10 seconds:
```
user.timeout = 10
```

## Setup
To install/update this library, use pip:

```
$ pip3 install --upgrade earnapp
```


## Example
Will tell you your current balance:
```
from earnapp import earnapp

user = earnapp.User()
try:
    user.login("ENTER oauth-refresh-token HERE")
except earnapp.IncorrectTokenException:
    print("Incorrect token")
    raise SystemExit

print("Current balance: " + str(user.money()["balance"]))
```

## Donations
BTC Address: bc1qrgpcdt6ecz8fyj6c6p2x3mtlaw7yaca9jh4lqf