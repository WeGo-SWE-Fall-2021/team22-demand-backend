import unittest
import sys
import xmlrunner

sys.path.insert(1, "../")

from order import Order


class OrderTestCase(unittest.TestCase):

    def test_order_creation_dictionary(self):
        data = {
            "_id": "1234",
            "customerId": "9876",
            "orderDestination": "austin",
            "pluginName": "food",
            "timeStamp": "4567",
            "paymentType": "Card"
        }
        order = Order(data)
        self.assertIsNotNone(order)

    def test_order_data_equals(self):
        data = {
            "_id": "1234",
            "customerId": "9876",
            "orderDestination": "austin",
            "pluginName": "food",
            "timeStamp": "4567",
            "paymentType": "Card"
        }
        order = Order(data)
        self.assertIsNotNone(order)
        self.assertEqual(order.id, "1234")
        self.assertEqual(order.customerId, "9876")
        self.assertEqual(order.orderDestination, "austin")
        self.assertEqual(order.pluginName, "food")
        self.assertEqual(order.timeStamp, "4567")
        self.assertEqual(order.paymentType, "Card")

    def test_order_data_change(self):
        data = {
            "_id": "1234",
            "customerId": "9876",
            "orderDestination": "austin",
            "pluginName": "food",
            "timeStamp": "4567",
            "paymentType": "Card"
        }
        order = Order(data)
        with self.assertRaises(AttributeError):
            order.id = "4321"
        self.assertEqual(order.id, "1234")
        with self.assertRaises(AttributeError):
            order.customerId = "1234"
        self.assertEqual(order.customerId, "9876")
        order.orderDestination = "Houston"
        self.assertEqual(order.orderDestination, "Houston")
        order.pluginName = "medication"
        self.assertEqual(order.pluginName, "medication")
        order.timeStamp = "0:00"
        self.assertEqual(order.timeStamp, "0:00")
        order.paymentType = "Cash"
        self.assertEqual(order.paymentType, "Cash")


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))