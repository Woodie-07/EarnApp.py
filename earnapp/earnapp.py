"""
EarnApp.py - A python library to interact with the EarnApp API
Copyright (C) 2022  SWM Tech Industries

This file is part of EarnApp.py.

EarnApp.py is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EarnApp.py is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EarnApp.py. If not, see <https://www.gnu.org/licenses/>.
"""

import requests
from requests.structures import CaseInsensitiveDict
from http.cookies import SimpleCookie


class RatelimitedException(Exception):
    """
    Raised when the IP is ratelimited.
    """


class IncorrectTokenException(Exception):
    """
    Raised when the oauth-refresh-token is incorrect.
    """


class JSONDecodeErrorException(Exception):
    """
    Raised when the JSON response is invalid.
    """


class XSRFErrorException(Exception):
    """
    Raised when the XSRF token is incorrect.
    """


def makeEarnAppRequest(endpoint: str, reqType: str, cookies: dict, timeout: int, data: dict = None, proxy: dict = None) -> requests.Response:
    """
    Make a request to the EarnApp API to a given endpoint
    :param endpoint: the API endpoint to request
    :param reqType: GET, POST, DELETE or PUT
    :param cookies: authentication cookies to send with the request
    :param data (optional): data to send along with the requst
    :return: response object
    """
    # Wondering why I do this? See https://bit.ly/3uNINj4
    if data is None:
        data = {}
    if proxy is None:
        proxy = {}

    if reqType == "GET":  # if we need to do a GET request
        resp = requests.get(
            "https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard",
            cookies=cookies,
            proxies=None if proxy == {} else proxy,
            timeout=timeout
        )  # do the GET request with the cookies required to the correct endpoint using proxy
    elif reqType == "POST":  # if we need to do a POST request
        resp = requests.post(
            "https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard",
            cookies=cookies,
            json=data,
            proxies=None if proxy == {} else proxy,
            timeout=timeout
        )  # do the POST request with the cookies required to the correct endpoint with the data using proxy
    elif reqType == "DELETE":  # if we need to do a DELETE request
        resp = requests.delete(
            "https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard",
            cookies=cookies,
            proxies=None if proxy == {} else proxy,
            timeout=timeout
        )  # do the DELETE request with the cookies required to the correct endpoint using proxy
    elif reqType == "PUT":  # if we need to do a PUT request
        resp = requests.put(
            "https://earnapp.com/dashboard/api/" + endpoint + "?appid=earnapp_dashboard",
            cookies=cookies,
            json=data,
            proxies=None if proxy == {} else proxy,
            timeout=timeout
        )  # do the PUT request with the cookies required to the correct endpoint with the data using proxy
    else:
        return None
    return resp


def getXSRFToken(timeout: int, proxy: dict = None):
    """
    A function to retrieve the XSRF token from the EarnApp API.
    This token is required for some endpoints to work.
    :param timeout: the amount of time to wait for a response from the server
    :param proxy (optional): a dictionary containing the proxy to use
    """
    # Wondering why I do this? See https://bit.ly/3uNINj4
    if proxy is None:
        proxy = {}

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
        "https://earnapp.com/dashboard/api/sec/rotate_xsrf?appid=earnapp_dashboard&version=1.281.185",
        headers=headers,
        proxies=None if proxy == {} else proxy,
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


def getReturnData(resp: requests.Response, token: str):
    """
    A function to get the JSON data from the response object.
    This function may also raise an exception if an error is encountered.
    :param resp: the response object to get the data from
    :param token: the EarnApp oauth-refresh-token used for the request.
    This token may be used when a IncorrectTokenException is raised.
    """
    if resp.status_code == 429:  # if the user is ratelimited
        raise RatelimitedException("You are being ratelimited")  # raise an exception
    if resp.status_code == 403:  # if the user is unauthorized
        raise IncorrectTokenException(token + " is not correct")  # raise an exception

    try:
        jsonData = resp.json()  # attempt to get the JSON data
    except requests.exceptions.JSONDecodeError:
        raise JSONDecodeErrorException("Failed to decode JSON data returned from server: " + resp.text)  # if the JSON data was invalid, raise an exception
    return jsonData


class User:
    """
    A class that represents an EarnApp user.
    This holds the user's token and settings.
    """
    cookies = {}
    proxy = {}
    timeout = 10  # default timeout for requests

    def setProxy(self, proxy: dict) -> bool:
        """
        Set the proxy for the requests
        :param proxy: proxy dictionary
        :return: True
        """
        self.proxy = proxy  # set the proxy
        return True

    def login(self, token: str, method: str="google") -> bool:
        """
        Attempt to log in to the account by requesting /user_data
        If it succeeds, it will write that data to the cookies variable
        :param token: oauth-refresh-token from the EarnApp dashboard
        :param method (optional): login method, only current option is google.
        :return: True on successful login, False otherwise
        """
        resp = makeEarnAppRequest(
            "user_data",
            "GET",
            {
                "auth-method": method,
                "oauth-refresh-token": token
            },
            self.timeout,
            proxy=self.proxy
        )

        if resp.status_code == 200:  # if the cookies were valid
            self.cookies = {"auth-method": method, "oauth-refresh-token": token}  # save the cookies to the variable
            # return the right value depending on succeeding/failing
            return True
        if resp.status_code == 403:
            raise IncorrectTokenException(token + " is not correct")  # if the token was invalid, raise an exception

        raise RatelimitedException("Some kind of an error when logging in, probably ratelimited.")

    def userData(self) -> dict:
        """
        Get data about the logged in user
        :return: a dictionary containing the user data
        """
        resp = makeEarnAppRequest(
            "user_data",
            "GET",
            self.cookies,
            self.timeout,
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def money(self) -> dict:
        """
        Get info such as current balance, payment method, etc.
        :return: a dictionary containing the user's money data
        """
        resp = makeEarnAppRequest(
            "money",
            "GET",
            self.cookies,
            self.timeout,
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def devices(self) -> dict:
        """
        Get info such as device IDs, rate, amount earnt, etc.
        :return: a dictionary containing the user's device data
        """
        resp = makeEarnAppRequest(
            "devices",
            "GET",
            self.cookies,
            self.timeout,
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def appVersions(self) -> dict:
        """
        Get the latest app version
        :return: a dictionary containing the latest version
        """
        resp = makeEarnAppRequest(
            "downloads",
            "GET",
            self.cookies,
            self.timeout,
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def paymentMethods(self) -> dict:
        """
        Get all available payment methods
        :return: a dictionary containing all available payment methods
        """
        resp = makeEarnAppRequest(
            "payment_methods",
            "GET",
            self.cookies,
            self.timeout,
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def transactions(self) -> dict:
        """
        Get past transactions and their status
        :return: a dictionary containing past transactions
        """
        resp = makeEarnAppRequest(
            "transactions",
            "GET",
            self.cookies,
            self.timeout,
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def linkDevice(self, deviceID: str) -> dict:
        """
        Link a device to the logged in EarnApp account
        :param deviceID: EarnApp device ID to link to account
        :return: a dictionary containing error message/success
        """
        xsrfToken = getXSRFToken(self.timeout, self.proxy)  # get the XSRF token

        headers = CaseInsensitiveDict()
        headers["xsrf-token"] = xsrfToken
        headers["Content-Type"] = "application/json"

        xsrfCookies = self.cookies.copy()
        xsrfCookies["xsrf-token"] = xsrfToken

        resp = requests.post(
            "https://earnapp.com/dashboard/api/link_device?appid=earnapp_dashboard",
            headers=headers,
            cookies=xsrfCookies,
            data='{"uuid":"' + deviceID + '"}',
            proxies=None if self.proxy == {} else self.proxy,
            timeout=self.timeout
        )  # do the POST request with the XSRF token

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def hideDevice(self, deviceID: str) -> dict:
        """
        Hide a device from the logged in EarnApp account
        :param deviceID: EarnApp device ID to hide from account
        :return: a dictionary containing error message/success
        """
        resp = makeEarnAppRequest(
            "hide_device",
            "PUT",
            self.cookies,
            self.timeout,
            {"uuid": deviceID},
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def showDevice(self, deviceID: str) -> dict:
        """
        Show a device on the logged in EarnApp account
        :param deviceID: EarnApp device ID to show on account
        :return: a dictionary containing error message/success
        """
        resp = makeEarnAppRequest(
            "show_device",
            "PUT",
            self.cookies,
            self.timeout,
            {
                "uuid": deviceID
            },
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def deleteDevice(self, deviceID: str) -> dict:
        """
        Delete a device from the logged in EarnApp account
        :param deviceID: EarnApp device ID to delete from account
        :return: a dictionary containing error message/success
        """
        resp = makeEarnAppRequest(
            "device/" + deviceID,
            "DELETE",
            self.cookies,
            self.timeout,
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def renameDevice(self, deviceID: str, name: str) -> dict:
        """
        Rename a device
        :param deviceID: EarnApp device ID to rename
        :param name: new name for the device
        :return: a dictionary containing error message/success
        """
        resp = makeEarnAppRequest(
            "edit_device/" + deviceID,
            "PUT",
            self.cookies,
            self.timeout,
            {
                "name": name
            },
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def redeemDetails(self, toEmail: str, paymentMethod: str="paypal.com") -> dict:
        """
        Change the redeem details of the logged in account
        :param toEmail: The email address to send payment to
        :param paymentMethod: optional payment method to send via
        :return: a dictionary containing error message/success
        """
        resp = makeEarnAppRequest(
            "redeem_details",
            "POST", self.cookies,
            self.timeout,
            {
                "to_email": toEmail,
                "payment_method": paymentMethod
            },
            proxy=self.proxy
        )

        return getReturnData(resp, self.cookies["oauth-refresh-token"])

    def onlineStatus(self, deviceIDs: list) -> dict:
        """
        Get the online status of a list of devices
        :param deviceIDs: list of device ID dicts to check (uuid and appid in each dict)
        :return: a dictionary containing the online status of the devices
        """
        resp = makeEarnAppRequest(
            "device_statuses",
            "POST",
            self.cookies,
            self.timeout,
            {"list": deviceIDs},
            proxy=self.proxy
        )
        return getReturnData(resp, self.cookies["oauth-refresh-token"])
