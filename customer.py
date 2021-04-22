import sys

if any('unittest/../' in string for string in sys.path):
    # Current working directory is unittest so go back from cwd twice
    sys.path.insert(2, sys.path[0] + '/../../team22-common-services-backend')
    sys.path.insert(2, sys.path[0] + '/../../common-services-backend')

else:
    # Current working directory is demand-backend so go back from cwd once
    sys.path.insert(2, sys.path[0] + '/../team22-common-services-backend')
    sys.path.insert(2, sys.path[0] + '/../common-services-backend')

from user import User


class Customer(User):
    # class constructor, receives a dictionary and populates class attributes
    # inherents parent attributes
    def __init__(self, dict):
        super().__init__(dict)

    def placeOrder(self):
        raise NotImplementedError
    
    def fetchOrderStatus(self):
        raise NotImplementedError

    def __str__(self):
        return f"Customer (\nid: {self.id} \nfirstName: {self.firstName} \nlastName: {self.lastName} \nphoneNumber: {self.phoneNumber} \nemail: {self.email} \nusername: {self.username} \npassword: {self.password} \n)"


