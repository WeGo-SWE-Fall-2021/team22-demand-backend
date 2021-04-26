import requests
import json
import datetime

from plugintype import PluginType
from uuid import uuid4

class Order:
    # class constructor, takes a dictionary, which is the JSON passed from the HTTP Post, as an argument and
    # populates class attributes
    def __init__(self, dict):
        self._id = str(dict.get("_id", uuid4()))
        self._customerId = dict["customerId"]
        self._pluginType = PluginType[dict.get("pluginType", "").upper()]
        self._timeStamp = dict.get("timeStamp", datetime.datetime.utcnow()) # Only set by mongo
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

    def __str__(self):
        return f"Order ( \nid: {self.id} \ncustomerId: {self.customerId} \npluginName: {self.pluginType} \ntimeStamp: {self.timeStamp} \npaymentType: {self.paymentType} \norderDestination: {self.orderDestination} \n)"

    def __eq__(self, value):
        return isinstance(value, Order) and \
            self.id == value.id and \
            self.customerId == value.customerId and \
            self.pluginType == value.pluginType and \
            self.timeStamp == value.timeStamp and \
            self.paymentType == value.paymentType and \
            self.orderDestination == value.orderDestination

    def __hash__(self):
        return hash((self.id, self.customerId, self.pluginType, self.timeStamp, self.paymentType, self.orderDestination))