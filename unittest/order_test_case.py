import unittest
import sys

sys.path.insert(1, sys.path[0] + "/../")

from order import Order
from plugintype import PluginType

order_data = {
    "_id": "1234",
    "customerId": "9876",
    "timeStamp": "23244",
    "paymentType": "CARD",
    "orderDestination": "3001 S Congress Ave, Austin, TX 78704",
    "plugin": PluginType.MEDICATION.name,
    "items": [{
        "id": "8039586408",
        "option": "24gm"
    }]
}

class OrderTestCase(unittest.TestCase):

    def test_order_creation_dictionary(self):
        order = Order(order_data)
        self.assertIsNotNone(order)

    def test_order_data_equals(self):
        order = Order(order_data)
        self.assertIsNotNone(order)
        self.assertEqual(order.id, order_data["_id"])
        self.assertEqual(order.customerId, order_data["customerId"])
        self.assertEqual(order.orderDestination, order_data["orderDestination"])
        self.assertEqual(order.plugin, PluginType.MEDICATION)
        self.assertEqual(order.timeStamp, order_data["timeStamp"])
        self.assertEqual(order.paymentType, order_data["paymentType"])
        self.assertEqual(order.items, order_data["items"])

    def test_order_data_change(self):
        order = Order(order_data)
        with self.assertRaises(AttributeError):
            order.id = "4321"
        self.assertEqual(order.id, order_data["_id"])
        with self.assertRaises(AttributeError):
            order.customerId = "1234"
        self.assertEqual(order.customerId, order_data["customerId"])
        order.orderDestination = "Houston"
        self.assertEqual(order.orderDestination, "Houston")
        order.plugin = PluginType.PIZZA
        self.assertEqual(order.plugin, PluginType.PIZZA)
        order.timeStamp = "0:00"
        self.assertEqual(order.timeStamp, "0:00")
        order.paymentType = "Cash"
        self.assertEqual(order.paymentType, "Cash")
        order.items = []
        self.assertEqual(order.items, [])

if __name__ == '__main__':
    unittest.main()