import requests
from requests.structures import CaseInsensitiveDict

def makeEarnAppRequest(endpoint: str, reqType: str, cookies: dict, data: dict = {}) -> requests.Response:
    """
    Make a request to the EarnApp API to a given endpoint
    :param endpoint: the API endpoint to request
    :param reqType: GET or POST
    :param cookies: authentication cookies to send with the request
    :param data (optional): data to send along with the requst
    :return: response object
    """
    
    if reqType == "GET": # if we need to do a GET request
        resp = requests.get("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies) # do the GET request with the cookies required to the correct endpoint
    elif reqType == "POST": # if we need to do a POST request
        resp = requests.post("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies, data=data) # do the POST request with the cookies required to the correct endpoint with the data
    else:
        return None
    return resp

class User:
    cookies = {}

    def login(self, token: str, method: str="google") -> bool:
        """
        Attempt to log in to the EarnApp account by requesting the user_data endpoint and if it succeeds, it will write that data to the cookies variable
        :param token: oauth-refresh-token from the EarnApp dashboard
        :param method (optional): login method, only current option is google.
        :return: True on successful login, False otherwise
        """
        
        resp = makeEarnAppRequest("user_data", "GET", {"auth-method": method, "oauth-refresh-token": token}) # test the login data with the user_data endpoint
        
        if resp.status_code == 200: # if the cookies were valid
            self.cookies = {"auth-method": method, "oauth-refresh-token": token} # save the cookies to the variable
            # return the right value depending on succeeding/failing
            return True
        return False
        
    def userData(self) -> dict:
        """
        Get data about the logged in user
        :return: a dictionary containing the user data
        """
        
        resp = makeEarnAppRequest("user_data", "GET", self.cookies) # get the user data
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData
        
    def money(self) -> dict:
        """
        Get data about the logged in user's money (current balance, payment method, etc)
        :return: a dictionary containing the user's money data
        """
        
        resp = makeEarnAppRequest("money", "GET", self.cookies) # get the devuce data
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData
        
    def devices(self) -> dict:
        """
        Get data about the logged in user's devices (device IDs, rate, amount earnt, etc)
        :return: a dictionary containing the user's device data
        """
        
        resp = makeEarnAppRequest("devices", "GET", self.cookies) # get the device data
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData
        
    def appVersions(self) -> dict:
        """
        Get the latest app version
        :return: a dictionary containing the latest version
        """
        
        resp = makeEarnAppRequest("app_versions", "GET", self.cookies) # get the version
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData
        
    def paymentMethods(self) -> dict:
        """
        Get all available payment methods
        :return: a dictionary containing all available payment methods
        """
        
        resp = makeEarnAppRequest("payment_methods", "GET", self.cookies) # get payment methods
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData
        
    def transactions(self) -> dict:
        """
        Get past transactions and their status
        :return: a dictionary containing past transactions
        """
        
        resp = makeEarnAppRequest("transactions", "GET", self.cookies) # get all transactions
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData
        
    def linkDevice(self, deviceID: str) -> dict:
        """
        Link a device to the logged in EarnApp account
        :param deviceID: EarnApp device ID to link to account
        :return: a dictionary containing error message/success
        """
        
        resp = makeEarnAppRequest("link_device", "POST", self.cookies, {"uuid": deviceID}) # send request
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData
        
    def redeemDetails(self, toEmail: str, paymentMethod: str="paypal.com") -> dict:
        """
        Change the redeem details of the logged in account
        :param toEmail: The email address to send payment to
        :param paymentMethod: optional payment method to send via
        :return: a dictionary containing error message/success
        """
        
        resp = makeEarnAppRequest("redeem_details", "POST", self.cookies, {"to": toEmail, "payment_method": paymentMethod}) # send request
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData