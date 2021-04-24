import requests
import json

from plugintype import PluginType
from uuid import uuid4

class Order:

    # class constructor, takes a dictionary, which is the JSON passed from the HTTP Post, as an argument and
    # populates class attributes
    def __init__(self, dict):
        self._id = str(dict.get("_id", uuid4()))
        self._customerId = dict["customerId"]
        self._pluginType = PluginType[dict["pluginType"]]
        self._timeStamp = dict["timeStamp"]
        self._paymentType = dict["paymentType"]
        self._orderDestination = dict["orderDestination"]

    @property
    def id(self):
        return self._id

    @property
    def customerId(self):
        return self._customerId

    @property
    def pluginType(self):
        return self._pluginType

    @pluginType.setter
    def pluginType(self, value):
        self._pluginType = value

    @property
    def timeStamp(self):
        return self._timeStamp

    @timeStamp.setter
    def timeStamp(self, value):
        self._timeStamp = value

    @property
    def paymentType(self):
        return self._paymentType

    @paymentType.setter
    def paymentType(self, value):
        self._paymentType = value

    @property
    def orderDestination(self):
        return self._orderDestination

    @orderDestination.setter
    def orderDestination(self, value):
        self._orderDestination = value

    # sends a get request to the supply backend to get a proccess into a dispatch and get vehicle tracking number
    def dispatchOrder(self, vType):
        url = "https://supply.team22.sweispring21.tk/api/v1/supply/dispatch"
        data = {
            "orderId": self.id,
            "orderDestination": self.orderDestination,
            "vehicleType": vType # TODO, send vehicle type so that supply can select a vehicle out of that type
        }
        response = requests.post(url, json=data, timeout=10)
        responseBody = json.loads(response.text)
        status = response.status_code
        return_data = {
            "status": response.status_code,
            "data": responseBody
        }
        return return_data

    def __str__(self):
        return f"Order ( \nid: {self.id} \ncustomerId: {self.customerId} \npluginName: {self.pluginType} \ntimeStamp: {self.timeStamp} \npaymentType: {self.paymentType} \norderDestination: {self.orderDestination} \n)"