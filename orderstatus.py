from enum import Enum

class OrderStatus(Enum):
    PROCESSING = 1
    SHIPPED = 2
    DELIVERED = 3
    ERROR = 4