"""
EarnApp.py - A Python library to interact with the EarnApp API
Copyright (C) 2022  Woodie

This file is part of EarnApp.py.

EarnApp.py is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EarnApp.py is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EarnApp.py. If not, see <https://www.gnu.org/licenses/>.
"""

from http import client
import requests
from requests.structures import CaseInsensitiveDict
from http.cookies import SimpleCookie
import time
from json.decoder import JSONDecodeError

apiURL = "https://earnapp.com/dashboard/api/"
clientAPIURL = "https://client.earnapp.com/"
appID = "earnapp_dashboard"


class RatelimitedException(Exception):
    """Raised when the IP is ratelimited."""


class IncorrectTokenException(Exception):
    """Raised when the oauth-token is incorrect."""


class JSONDecodeErrorException(Exception):
    """Raised when the JSON response is invalid."""


class XSRFErrorException(Exception):
    """Raised when the XSRF token is incorrect."""


class InvalidTimeframeException(Exception):
    """
    Raised when the given timeframe is invalid.
    Must be 'daily', 'weekly', or 'monthly'.
    """

class InvalidArgumentsException(Exception):
    """Raised when the given client arguments are invalid."""


def _makeClientRequest(
    endpoint: str,
    method: str,
    data: dict = None,
    proxy: dict = None
) -> requests.Response:
    """
    Make a request to the EarnApp Client API to a given endpoint
    :param endpoint: the API endpoint to request
    :param method: GET, POST, DELETE or PUT
    :param data (optional): data to send along with the requst
    :param proxy (optional): a dictionary containing the proxy to use
    :return: response object
    """

    url = clientAPIURL + endpoint

    resp = requests.request(
        method,
        url,
        json=data,
        proxies=proxy
    )

    return resp


def _makeEarnAppRequest(
    endpoint: str,
    method: str,
    cookies: dict,
    timeout: int,
    headers: dict,
    data: dict = None,
    proxy: dict = None,
    queryParams: str = ""
) -> requests.Response:
    """
    Make a request to the EarnApp API to a given endpoint
    :param endpoint: the API endpoint to request
    :param method: GET, POST, DELETE or PUT
    :param cookies: authentication cookies to send with the request
    :param timeout: the amount of time to wait for a response
    :param data (optional): data to send along with the requst
    :param proxy (optional): a dictionary containing the proxy to use
    :param queryParams (optional): query parameters to send along with the request
    :return: response object
    """

    queryParams = "?appid=" + appID + queryParams

    url = apiURL + endpoint + queryParams

    resp = requests.request(
        method,
        url,
        cookies=cookies,
        json=data,
        proxies=proxy,
        timeout=timeout,
        headers=headers
    )

    return resp


def getXSRFToken(timeout: int, proxy: dict = None):
    """
    A function to retrieve the XSRF token from the EarnApp API.
    This token is required for some endpoints to work.
    :param timeout: the amount of time to wait for a response from the server
    :param proxy (optional): a dictionary containing the proxy to use
    """

    headers = CaseInsensitiveDict()
    headers["Host"] = "earnapp.com"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-GB,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "none"
    headers["Sec-Fetch-User"] = "?1"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"
    headers["TE"] = "trailers"

    resp = requests.get(
        apiURL + "/sec/rotate_xsrf?appid=" + appID + "&version=1.281.185",
        headers=headers,
        proxies=proxy,
        timeout=timeout
    )

    if resp.status_code == 429:  # if the user is ratelimited
        raise RatelimitedException("You are being ratelimited")  # raise an exception

    cookie = SimpleCookie()
    cookie.load(resp.headers['Set-Cookie'])

    token = None

    for key, morsel in cookie.items():
        if key == "xsrf-token":
            token = morsel.value

    if token is None:
        raise XSRFErrorException("Could not get XSRF token")

    return token

def _getClientReturnData(resp: requests.Response) -> dict:
    """
    A function to get the JSON data from the response object from the client API.
    This function may also raise an exception if an error is encountered.
    :param resp: the response object to get the data from
    """
    if resp.request.url.endswith("/ndt7"):
        return resp.text

    if resp.text == "Too Many Requests":
        raise RatelimitedException(resp.text)
    
    if resp.text == "Invalid arguments":
        raise InvalidArgumentsException("Invalid arguments")

    try:
        return resp.json()
    except JSONDecodeError:
        raise JSONDecodeErrorException("Failed to decode JSON data: " + resp.text)


def _getReturnData(resp: requests.Response) -> dict:
    """
    A function to get the JSON data from the response object.
    This function may also raise an exception if an error is encountered.
    :param resp: the response object to get the data from
    """
    if resp.status_code == 429:  # if the user is ratelimited
        raise RatelimitedException("You are being ratelimited")  # raise an exception
    if resp.status_code == 403:  # if the user is unauthorized
        raise IncorrectTokenException("Token is not correct")  # raise an exception

    try:
        jsonData = resp.json()  # attempt to get the JSON data
    except JSONDecodeError:
        raise JSONDecodeErrorException("Failed to decode JSON data: " + resp.text)  # if the JSON data was invalid, raise an exception
    return jsonData


class Client:
    """
    A class that represents a EarnApp client session
    This holds the client settings/proxy
    """

    proxy = {}
    timeout = 10

    def __init__(self, uuid: str, version: str, arch: str, appid: str, proxy: dict = None, timeout: int = 10):
        """
        Initialise the client
        :param uuid: the uuid of the client
        :param version: the version of the client
        :param arch: the architecture of the client
        :param appid: the appid of the client
        :param proxy: the proxy to use
        :param timeout: the amount of time to wait for a response from the server
        """
        self.uuid = uuid
        self.version = version
        self.arch = arch
        self.appid = appid
        if proxy is None:
            proxy = {}
        self.proxy = proxy
        self.timeout = timeout

    def setProxy(self, proxy: dict) -> bool:
        """
        Set the proxy for the requests
        :param proxy: proxy dictionary
        :return: True
        """
        self.proxy = proxy  # set the proxy
        return True

    def simpleClientRequest(
        self,
        endpoint: str,
        method: str,
    ) -> dict:
        """
        A function to call a given endpoint. It handles return data, no XSRF for client.
        :param endpoint: the endpoint to call
        :param method: the method to use (GET, POST, DELETE or PUT)
        :param data (optional): JSON data to send
        """

        if method == "GET":
            endpoint += "?uuid=" + self.uuid + "&version=" + self.version + "&arch=" + self.arch + "&appid=" + self.appid
            data = None
        else:
            data = {"uuid": self.uuid, "version": self.version, "arch": self.arch, "appid": self.appid}

        resp = _makeClientRequest(
            endpoint,
            method,
            data=data,
            proxy=self.proxy
        )

        return _getClientReturnData(resp)

    def appConfigWin(self):
        """
        Get many details about the device, including:
        Bandwidth
        Earnings
        Referral code of linked account
        Available payment methods

        :return: JSON data
        """
        return self.simpleClientRequest("app_config_win.json", "POST")

    def appConfigNode(self):
        """
        Think this returns the latest Linux version, not 100% sure.

        :return: JSON data
        """
        return self.simpleClientRequest("app_config_node.json", "GET")

    def appConfig(self):
        """
        No idea what this is, it just seems to return an empty array in my tests.

        :return: JSON data
        """
        return self.simpleClientRequest("app_config.json", "GET")

    def isPiggybox(self):
        """
        Checks if the device is a piggybox.

        :return: JSON data
        """
        return self.simpleClientRequest("is_piggybox", "GET")

    def ndt7(self):
        """
        Not sure, think it's a speedtest or something for piggybox.

        :return: String that is just 'OK' in my tests
        """
        return self.simpleClientRequest("ndt7", "POST")

    def installDevice(self):
        """
        Register the device with the server.
        This is called by the app when the device is first installed.

        :return: JSON data showing success or fail
        """
        return self.simpleClientRequest("install_device", "POST")

    def getBWStats(self):
        """
        Shows total bandwidth and total earnt.

        :return: JSON data
        """
        return self.simpleClientRequest("get_bw_stats", "GET")

    def isLinked(self):
        """
        Shows the email address of the account the device is linked to.

        :return: JSON data
        """
        return self.simpleClientRequest("is_linked", "GET")

    def isIPBlocked(self):
        """
        Checks if the IP used for the request is blocked.

        :return: JSON data
        """
        return self.simpleClientRequest("is_ip_blocked", "GET")

class User:
    """
    A class that represents an EarnApp user.
    This holds the user's token and settings.
    """

    cookies = {}
    proxy = {}
    headers = {}
    timeout = 10  # default timeout for requests

    xsrfToken = ""
    xsrfTokenTime = 0

    def setProxy(self, proxy: dict) -> bool:
        """
        Set the proxy for the requests
        :param proxy: proxy dictionary
        :return: True
        """
        self.proxy = proxy  # set the proxy
        return True

    def _updateXSRFTokenIfNecessary(self):
        """
        Will update the XSRF token if it is older than 60 seconds.
        :return: the XSRF token
        """
        currentTime = int(time.time())
        if currentTime - 60 < self.xsrfTokenTime:  # 60 second token expiration
            return self.xsrfToken

        xsrfToken = getXSRFToken(self.timeout, proxy=self.proxy)
        self.xsrfTokenTime = currentTime  # set the update time
        self.xsrfToken = xsrfToken
        self.cookies["xsrf-token"] = xsrfToken
        self.headers["xsrf-token"] = xsrfToken

        return self.xsrfToken

    def simpleEarnAppRequest(
        self,
        endpoint: str,
        method: str,
        data: dict = None,
        queryParams: str = ""
    ) -> requests.Response:
        """
        A function to call a given endpoint. It handles XSRF and return data.
        :param endpoint: the endpoint to call
        :param method: the method to use (GET, POST, DELETE or PUT)
        :param data (optional): JSON data to send
        :param queryParams (optional): URL query parameters to send
        """
        self._updateXSRFTokenIfNecessary()
        resp = _makeEarnAppRequest(
            endpoint,
            method,
            self.cookies,
            self.timeout,
            self.headers,
            data=data,
            proxy=self.proxy,
            queryParams=queryParams
        )

        return _getReturnData(resp)


    def login(self, token: str, method: str="google") -> bool:
        """
        Attempt to log in to the account by requesting /user_data
        If it succeeds, it will write that data to the cookies variable
        :param token: oauth-token from the EarnApp dashboard
        :param method (optional): login method, only current option is google.
        :return: True on successful login, False otherwise
        """
        self._updateXSRFTokenIfNecessary()
        resp = _makeEarnAppRequest(
            "user_data",
            "GET",
            {
                "auth-method": method,
                "oauth-token": token,
                "xsrf-token": self.xsrfToken
            },
            self.timeout,
            self.headers,
            proxy=self.proxy
        )

        if resp.status_code == 200:  # if the cookies were valid
            self.cookies = {  # save the cookies to the variable
                "auth-method": method,
                "oauth-token": token,
                "xsrf-token": self.xsrfToken
            }
            # return the right value depending on succeeding/failing
            return True
        if resp.status_code == 403:
            raise IncorrectTokenException("Token is not correct")

        raise RatelimitedException("Error when logging in, probably ratelimited.")

    def userData(self) -> dict:
        """
        Get data about the logged in user
        :return: a dictionary containing the user data
        """
        return self.simpleEarnAppRequest("user_data", "GET")

    def money(self) -> dict:
        """
        Get info such as current balance, payment method, etc.
        :return: a dictionary containing the user's money data
        """
        return self.simpleEarnAppRequest("money", "GET")

    def devices(self) -> dict:
        """
        Get info such as device IDs, rate, amount earnt, etc.
        :return: a dictionary containing the user's device data
        """
        return self.simpleEarnAppRequest("devices", "GET")

    def appVersions(self) -> dict:
        """
        Get the latest app version
        :return: a dictionary containing the latest version
        """
        return self.simpleEarnAppRequest("downloads", "GET")

    def paymentMethods(self) -> dict:
        """
        Get all available payment methods
        :return: a dictionary containing all available payment methods
        """
        return self.simpleEarnAppRequest("payment_methods", "GET")

    def transactions(self) -> dict:
        """
        Get past transactions and their status
        :return: a dictionary containing past transactions
        """
        return self.simpleEarnAppRequest("transactions", "GET")

    def linkDevice(self, deviceID: str) -> dict:
        """
        Link a device to the logged in EarnApp account
        :param deviceID: EarnApp device ID to link to account
        :return: a dictionary containing error message/success
        """
        return self.simpleEarnAppRequest(
            "link_device",
            "POST",
            data={"uuid": deviceID}
        )

    def hideDevice(self, deviceID: str) -> dict:
        """
        Hide a device from the logged in EarnApp account
        :param deviceID: EarnApp device ID to hide from account
        :return: a dictionary containing error message/success
        """
        return self.simpleEarnAppRequest(
            "hide_device",
            "PUT",
            data={"uuid": deviceID}
        )

    def showDevice(self, deviceID: str) -> dict:
        """
        Show a device on the logged in EarnApp account
        :param deviceID: EarnApp device ID to show on account
        :return: a dictionary containing error message/success
        """
        return self.simpleEarnAppRequest(
            "show_device",
            "PUT",
            data={"uuid": deviceID}
        )

    def deleteDevice(self, deviceID: str) -> dict:
        """
        Delete a device from the logged in EarnApp account
        :param deviceID: EarnApp device ID to delete from account
        :return: a dictionary containing error message/success
        """
        return self.simpleEarnAppRequest("device/" + deviceID, "DELETE")

    def renameDevice(self, deviceID: str, name: str) -> dict:
        """
        Rename a device
        :param deviceID: EarnApp device ID to rename
        :param name: new name for the device
        :return: a dictionary containing error message/success
        """
        return self.simpleEarnAppRequest(
            "edit_device/" + deviceID,
            "PUT",
            data={"name": name}
        )

    def redeemDetails(self, toEmail: str, paymentMethod: str="paypal.com") -> dict:
        """
        Change the redeem details of the logged in account
        :param toEmail: The email address to send payment to
        :param paymentMethod: optional payment method to send via
        :return: a dictionary containing error message/success
        """
        return self.simpleEarnAppRequest(
            "redeem_details",
            "POST",
            data={
                "to_email": toEmail,
                "payment_method": paymentMethod
            }
        )

    def onlineStatus(self) -> dict:
        """
        Get the online status of device
        :return: a dictionary containing any online devices
        """
        return self.simpleEarnAppRequest("device_statuses", "GET")

    def counters(self) -> dict:
        """
        Get some info about next refresh/withdraw
        :return: a dictionary containing some sort of info about next refresh/withdraw
        """
        return self.simpleEarnAppRequest("counters", "GET")

    def usage(self, step: str = "daily") -> dict:
        """
        Get the usage of all devices on the logged in account, including deleted devices
        :param step: the timeframe of usage (daily, weekly, monthly), default daily
        :return: a dictionary containing the usage
        """
        if step not in ["daily", "weekly", "monthly"]:
            raise InvalidTimeframeException

        return self.simpleEarnAppRequest(
            "usage",
            "GET",
            queryParams="&step=" + step
        )
