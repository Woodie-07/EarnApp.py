# EarnApp.py testing script

from earnapp import earnapp

token = "ENTER TOKEN HERE"
deviceID = "ENTER TEST DEVICE ID"
payoutEmail = "ENTER TEST PAYOUT EMAIL"

print("Initializing user class")
user = earnapp.User()
print("Got user class")

print("Attempting to log in with token " + token)
loggedIn = user.login(token)

if loggedIn == True:
    print("Successfully logged in!")
else:
    print("Failed to log in")
    
print("User data: " + str(user.userData()))
print("Money: " + str(user.money()))
print("Devices: " + str(user.devices()))
print("App version: " + str(user.appVersions()))
print("Payment methods: " + str(user.paymentMethods()))
print("Transactions: " + str(user.transactions()))
print("Attempting to link device ID " + deviceID)
print(str(user.linkDevice(deviceID)))
print("Attempting to change payout email to " + payoutEmail)
print(str(user.redeemDetails(payoutEmail)))