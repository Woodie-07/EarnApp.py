# EarnApp.py
PyPI Link: https://pypi.org/project/EarnApp/
## Table of contents
* [General info](#general-info)
* [Documentation](#documentation)
* [Setup](#setup)

## General info
A Python library to interact with the EarnApp API. 

## Documentation
1) First, import the library: `from earnapp import earnapp`
2) Next, you can initialize a user. You can have as many users as you like and each user can have a different token. Initialize it with something: `user = earnapp.User()`. You can also initialize a Client which allows you to interact with the client API, like so: `client = earnapp.Client(uuid, version, arch, appid)`. These options can be changed later with their variable names, for example: `client.uuid = newUUID`.
3) Log into the EarnApp account with `user.login("ENTER oauth-token HERE")`. A client object does not require any authentication.
4) The login function will return a IncorrectTokenException if the token is incorrect.
```py
try:
    user.login("ENTER oauth-token HERE")
except earnapp.IncorrectTokenException:
    print("Incorrect token")
    raise SystemExit
```
5) Now, you can use whatever functions you like, for example `print("Money: " + str(user.money()))`, or you can get information from the client API: `print("App details: " + str(client.appConfigWin()))`.

User Functions:
- setProxy - Sets the proxy for the requests. Argument is a dictionary with the proxy in requests format, for example: `{"https": "socks5://admin:P455w0rd@1.1.1.1:5442"}`.
- login - Logs in to the EarnApp account. Argument is the oauth-token string.
- userData - Get data about the logged in user.
- money - Get data about the logged in user's money.
- devices - Get data about the logged in user's devices.
- appVersions - Get the latest app version.
- paymentMethods - Get all available payment methods.
- transactions - Get past transactions and their status.
- linkDevice - Link a device to the logged in EarnApp account. Argument is the device id string.
- hideDevice - Hide a device from the logged in EarnApp account. Argument is the device id string.
- showDevice - Show a device on the logged in EarnApp account. Argument is the device id string.
- deleteDevice - Delete a device from the logged in EarnApp account. Argument is the device id string.
- renameDevice - Rename a device on the logged in EarnApp account.
- redeemDetails - Change the redeem details of the logged in EarnApp account. Argument is the new email address for payments, and optionally paymentMethod can be an available payment method, defaults to `"paypal.com"`.
- onlineStatus - Gets the online status of the devices passed. Argument is a list of device ids.
- usage - Gets the usage stats of all devices shown in the given timeframe. Argument can be daily, weekly, or monthly.

Client Functions:
- appConfigWin - Get many details about the device, including bandwidth, earnings, referral code of linked account, and available payment methods.
- appConfigNode - Think this returns the latest Linux version, not 100% sure.
- appConfig - No idea what this is, it just seems to return an empty array in my tests.
- isPiggybox - Check if the device is a piggybox. 
- ndt7 - Not sure, think it's a speedtest or something for piggybox.
- installDevice - Register the device with the server. This is called by the app when the device is first installed.
- getBWStats - Shows total bandwidth and total earnt.
- isLinked - Shows the email address of the account the device is linked to.
- isIPBlocked - Checks if the IP used for the request is blocked.

Exceptions:
- IncorrectTokenException - Raised when the token is incorrect
- RatelimitedException - Raised when the IP is ratelimited
- JSONDecodeErrorException - Raised when the JSON data returned by the EarnApp API is invalid
- XRSFErrorException - Raised when the script fails to retrieve an XRSF token
- InvalidTimeframeException - Raised when the given timeframe is invalid. Must be 'daily', 'weekly', or 'monthly'.
- InvalidArgumentsException - Raised when the given client arguments are invalid.

You can set a timeout for the requests with user.timeout or client.timeout, for example, to set the timeout to 10 seconds (default):
```py
user.timeout = 10
```

## Setup
To install/update this library, use pip:

```shell
$ pip3 install --upgrade earnapp
```


## Examples
Will tell you your current balance:
```py
from earnapp import earnapp

user = earnapp.User()
try:
    user.login("ENTER oauth-token HERE")
except earnapp.IncorrectTokenException:
    print("Incorrect token")
    raise SystemExit

print("Current balance: " + str(user.money()["balance"]))
```

Shows the total bandwidth of a device in bytes:
```py
from earnapp import earnapp

client = earnapp.Client("UUID", "VERSION", "CPU", "APPID")
try:
    data = client.appConfigWin()
    print("Total bandwidth in bytes: " + str(data["server_bw_total"]))
except earnapp.InvalidArgumentsException:
    print("Invalid arguments")
    raise SystemExit
```