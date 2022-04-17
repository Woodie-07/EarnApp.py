"""
EarnApp.py - A python library to interact with the EarnApp API
Copyright (C) 2022  SWM Tech Industries

This file is part of EarnApp.py.

EarnApp.py is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EarnApp.py is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EarnApp.py. If not, see <https://www.gnu.org/licenses/>.
"""

# EarnApp.py testing script

from earnapp import earnapp

token = "OAUTH-REFRESH-TOKEN"
deviceID = "DEVICE ID TO ADD"
hideDeviceID = "DEVICE ID TO HIDE/SHOW"
proxy = {'https': 'socks5://user:pass@ip:port'}
payoutEmail = "ENTER TEST PAYOUT EMAIL"

print("Initializing user class")
user = earnapp.User()
print("Got user class")

user.setProxy(proxy)

print("Attempting to log in with token " + token)
try:
    loggedIn = user.login(token)
except earnapp.IncorrectTokenException:
    print("Incorrect token")
    raise earnapp.IncorrectTokenException

print("Successfully logged in!")

print("User data: " + str(user.userData()))
print("Money: " + str(user.money()))
print("Devices: " + str(user.devices()))
print("App version: " + str(user.appVersions()))
print("Payment methods: " + str(user.paymentMethods()))
print("Transactions: " + str(user.transactions()))
print("Attempting to link device ID " + deviceID)
print(str(user.linkDevice(deviceID)))
print("Attempting to hide device ID " + hideDeviceID)
print(str(user.hideDevice(hideDeviceID)))
print("Attempting to show device ID " + hideDeviceID)
print(str(user.showDevice(hideDeviceID)))
print("Attempting to change payout email to " + payoutEmail)
print(str(user.redeemDetails(payoutEmail)))
