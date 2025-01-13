# purpose:
#     this file contains the entity class for this entity with its methods. There are no CRUD methods in this class,
#     only the entity class and its attributes are defined here, and methods based on already having the entity object.

class TestEntity:
    attribute1:int = None
    attribute2:str = None
    attribute3:float = None
    __privateattribute:str = None
    
    def __init__(self, attribute1, attribute2, attribute3, privateattribute):
        self.attribute1 = attribute1
        self.attribute2 = attribute2
        self.attribute3 = attribute3
        self.__privateattribute = privateattribute
        
    def get_privateattribute(self):
        return self.__privateattribute
