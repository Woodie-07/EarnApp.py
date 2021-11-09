# EarnApp.py
## Table of contents
* [General info](#general-info)
* [Documentation](#documentation)
* [Setup](#setup)

## General info
A python library to interact with the EarnApp API. 

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
	
## Setup
To run this project, install it using pip:

```
$ pip3 install earnapp
```
