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
        self._timeStamp = dict.get("timeStamp", datetime.datetime.utcnow()) # Only set by mongo
        self._paymentType = dict["paymentType"]
        self._orderDestination = dict["orderDestination"]
        self._plugin = PluginType[dict["plugin"]]
        self._items = dict["items"]

    @property
    def id(self):
        return self._id

    @property
    def customerId(self):
        return self._customerId

    @property
    def plugin(self):
        return self._plugin

    @plugin.setter
    def plugin(self, value):
        self._plugin = value

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

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    def __str__(self):
        return f"Order ( \nid: {self.id} \ncustomerId: {self.customerId} \nplugin: {self.plugin} \ntimeStamp: {self.timeStamp} \npaymentType: {self.paymentType} \norderDestination: {self.orderDestination} \nitems: {self.items} \n)"

    def __eq__(self, value):
        return isinstance(value, Order) and \
            self.id == value.id and \
            self.customerId == value.customerId and \
            self.plugin == value.plugin and \
            self.timeStamp == value.timeStamp and \
            self.paymentType == value.paymentType and \
            self.orderDestination == value.orderDestination and \
            self.items == value.items

    def __hash__(self):
        return hash((self.id, self.customerId, self.pluginType, self.timeStamp, self.paymentType, self.orderDestination, self.items))