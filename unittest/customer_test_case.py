import unittest
import sys

sys.path.insert(1, "../")

from customer import Customer


class CustomerTestCase(unittest.TestCase):

    def test_customer_creation(self):
        data = {
            "firstName": "firstname",
            "lastName": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        customer = Customer(data)
        self.assertIsNotNone(customer)

    def test_customer_data_equals(self):
        data = {
            "firstName": "firstname",
            "lastName": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        customer = Customer(data)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.firstName, "firstname")
        self.assertEqual(customer.lastName, "lastname")
        self.assertEqual(customer.phoneNumber, "11111")
        self.assertEqual(customer.email, "email@email.com")
        self.assertEqual(customer.username, "user")
        self.assertEqual(customer.password, "pwdtest")

    def test_customer_data_change(self):
        data = {
            "firstName": "firstname",
            "lastName": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        customer = Customer(data)
        customer.username = "new_username"
        self.assertEqual(customer.username, "new_username")
        customer.password = "new_pwdtest"
        self.assertEqual(customer.password, "new_pwdtest")
        customer.email = "new@new.com"
        self.assertEqual(customer.email, "new@new.com")
        customer.firstName = "newfirstname"
        self.assertEqual(customer.firstName, "newfirstname")
        customer.lastName = "newlastname"
        self.assertEqual(customer.lastName, "newlastname")
        customer.phoneNumber = "00000"
        self.assertEqual(customer.phoneNumber, "00000")


if __name__ == '__main__':
    unittest.main()
