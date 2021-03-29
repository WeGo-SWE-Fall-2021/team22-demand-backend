import urllib.request

class Order:

    # class constructor, takes a dictionary, which is the JSON passed from the HTTP Post, as an argument and
    # populates class attributes
    def __init__(self, postData):
        self.orderID = 0000 # default ID, will be changed based on existing database entries
        #self.pluginName = postData["pluginName"]
        self.orderOrigin = postData["originLocation"]
        self.orderDestination = postData["destinationLocation"]

    # basic set methods
    def setOrderID(self, orderID):
        self.orderID = orderID

    # def setPluginName(self, pluginName):
    #     self.pluginName = pluginName

    def setOrderOrigin(self, originLocation):
        self.orderOrigin = originLocation

    def setOrderDestination(self, destinationLocation):
        self.orderDestination = destinationLocation

    # basic get methods
    def getOrderID(self):
        return self.orderID

    # def getPluginName(self):
    #     return self.pluginName

    def getOrderOrigin(self):
        return self.orderOrigin

    def getOrderDestination(self):
        return self.orderDestination

    # sends a get request to the supply backend to get a vehicle assigned to this order
    ###### Currently this just sends the orderID as a paramater and gets back the same ID to show connection between supply and demand #####
    def requestVehicle(self):
        url = "https://supply.team22.sweispring21.tk/api/v1/supply/order"
        url = url + '?orderNum=' + str(self.orderID)
        vehicleID = urllib.request.urlopen(url)
        return vehicleID