import urllib.request
import json

from uuid import uuid4

class Order:

    # class constructor, takes a dictionary, which is the JSON passed from the HTTP Post, as an argument and
    # populates class attributes
    def __init__(self, dict):
        self._id = str(dict.get("_id", uuid4()))
        self._customerId = dict["customerId"]
        self._pluginName = dict["pluginName"]
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
    def pluginName(self):
        return self._pluginName

    @pluginName.setter
    def pluginName(self, value):
        self._pluginName = value

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

    # sends a get request to the supply backend to get a proccess into a dispatch and get order number
    ###### Currently this just sends the orderID as a paramater and gets back the same ID to show connection between supply and demand #####
    def requestVehicle(self):
        url = "https://supply.team22.sweispring21.tk/api/v1/supply/dispatch"
        url = url + '?orderNum=' + str(self.orderID)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        responseBody = json.loads(response)
        vehicleID = int(responseBody["orderNum"])
        return vehicleID

    def __str__(self):
        return f"Order ( \nid: {self.id} \ncustomerId: {self.customerId} \npluginName: {self.pluginName} \ntimeStamp: {self.timeStamp} \npaymentType: {self.paymentType} \norderDestination: {self.orderDestination} \n)"