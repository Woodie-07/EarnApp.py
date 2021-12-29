import requests
from requests.structures import CaseInsensitiveDict

def makeEarnAppRequest(endpoint: str, reqType: str, cookies: dict, data: dict = {}, proxy: dict = {}) -> requests.Response:
    """
    Make a request to the EarnApp API to a given endpoint
    :param endpoint: the API endpoint to request
    :param reqType: GET, POST, DELETE or PUT
    :param cookies: authentication cookies to send with the request
    :param data (optional): data to send along with the requst
    :return: response object
    """
    
    if reqType == "GET": # if we need to do a GET request
        if proxy != {}: # if we need to use a proxy
            resp = requests.get("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies, proxies=proxy) # do the GET request with the cookies required to the correct endpoint using proxy
        else:
            resp = requests.get("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies) # do the GET request with the cookies required to the correct endpoint
    elif reqType == "POST": # if we need to do a POST request
        if proxy != {}: # if we need to use a proxy
            resp = requests.post("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies, data=data, proxies=proxy) # do the POST request with the cookies required to the correct endpoint with the data using proxy
        else:
            resp = requests.post("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies, data=data) # do the POST request with the cookies required to the correct endpoint with the data
    elif reqType == "DELETE": # if we need to do a DELETE request
        if proxy != {}: # if we need to use a proxy
            resp = requests.delete("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies, proxies=proxy) # do the DELETE request with the cookies required to the correct endpoint using proxy
        else:
            resp = requests.delete("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies) # do the DELETE request with the cookies required to the correct endpoint
    elif reqType == "PUT": # if we need to do a PUT request
        if proxy != {}: # if we need to use a proxy
            resp = requests.put("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies, data=data, proxies=proxy) # do the PUT request with the cookies required to the correct endpoint with the data using proxy
        else:
            resp = requests.put("https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard", cookies=cookies, data=data) # do the PUT request with the cookies required to the correct endpoint with the data
    else:
        return None
    return resp

class User:
    cookies = {}
    proxy = {}

    def setProxy(self, proxy: dict) -> bool:
        """
        Set the proxy for the requests
        :param proxy: proxy dictionary
        :return: True
        """
        
        self.proxy = proxy # set the proxy
        return True

    def login(self, token: str, method: str="google") -> bool:
        """
        Attempt to log in to the EarnApp account by requesting the user_data endpoint and if it succeeds, it will write that data to the cookies variable
        :param token: oauth-refresh-token from the EarnApp dashboard
        :param method (optional): login method, only current option is google.
        :return: True on successful login, False otherwise
        """
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("user_data", "GET", {"auth-method": method, "oauth-refresh-token": token}, proxy=self.proxy) # test the login data with the user_data endpoint with the proxy
        else:
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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("user_data", "GET", self.cookies, proxy=self.proxy) # get the user data with the proxy
        else:
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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("money", "GET", self.cookies, proxy=self.proxy) # get the money data with the proxy
        else:
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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("devices", "GET", self.cookies, proxy=self.proxy) # get the device data with the proxy
        else:
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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("app_versions", "GET", self.cookies, proxy=self.proxy) # get the app version with the proxy
        else:
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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("payment_methods", "GET", self.cookies, proxy=self.proxy) # get the payment methods with the proxy
        else:
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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("transactions", "GET", self.cookies, proxy=self.proxy) # get the transactions with the proxy
        else:
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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("link_device", "POST", self.cookies, {"uuid": deviceID}, proxy=self.proxy) # send request with proxy
        else:
            resp = makeEarnAppRequest("link_device", "POST", self.cookies, {"uuid": deviceID}) # send request
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData

    def unlinkDevice(self, deviceID: str) -> dict:
        """
        Unlink a device from the logged in EarnApp account
        :param deviceID: EarnApp device ID to unlink from account
        :return: a dictionary containing error message/success
        """
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("device/" + deviceID, "DELETE", self.cookies, proxy=self.proxy) # send request with proxy
        else:
            resp = makeEarnAppRequest("device/" + deviceID, "DELETE", self.cookies) # send request

        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData

    def renameDevice(self, deviceID: str, name: str) -> dict:
        """
        Rename a device
        :param deviceID: EarnApp device ID to rename
        :param name: new name for the device
        :return: a dictionary containing error message/success
        """
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("device/" + deviceID, "PUT", self.cookies, {"name": name}, proxy=self.proxy) # send request with proxy
        else:
            resp = makeEarnAppRequest("device/" + deviceID, "PUT", self.cookies, {"name": name}) # send request

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
        
        if self.proxy != {}: # if we have a proxy
            resp = makeEarnAppRequest("redeem_details", "POST", self.cookies, {"to_email": toEmail, "payment_method": paymentMethod}, proxy=self.proxy) # send request with proxy
        else:
            resp = makeEarnAppRequest("redeem_details", "POST", self.cookies, {"to": toEmail, "payment_method": paymentMethod}) # send request
        
        try:
            jsonData = resp.json() # attempt to get the JSON data
        except:
            return None # if it failed return NoneType
        return jsonData