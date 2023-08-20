#Author:Xiaoping Zhang
#Date: July 22, 2023

class VegetableStorage:
    """
    A class for vegetables in cold and common storage information.
    Initializes a VegetableStorage instance with the following parameters.
      Parameters:
        - REF_DATE: The reference date.
        - GEO: The geographic location.
        - DGUID: The data guide identifier.
        - Type_of_product: The type of vegetable.
        - Type_of_storage: The type of storage.
        - UOM: The unit of measure.
        - UOM_ID: The id of the  unit of measure.
        - SCALAR_FACTOR: The scalar factor.
        - SCALAR_ID: The scalar's ID.
        - VECTOR: The vector factor.
        - COORDINATE: The coordinate information.
        - VALUE: The value of the storage information.
        - STATUS: The status of the storage information.
        - SYMBOL: The symbol associated with the storage information.
        - TERMINATED: The termination status of the storage information.
        - DECIMALS: The number of decimal places in the storage value
    """
    def __init__(self, REF_DATE, GEO, DGUID,Type_of_product,
                Type_of_storage,UOM,UOM_ID,SCALAR_FACTOR,
                 SCALAR_ID, VECTOR,COORDINATE,VALUE,
                 STATUS,SYMBOL,TERMINATED,DECIMALS):
        """
        Constructs all the attributes for the vegetableStorage object.
         :param REF_DATE: str - The reference date.
        :param GEO: str - The geographic location.
        :param DGUID: str - The data guide identifier.
        :param Type_of_product: str - The type of vegetable.
        :param Type_of_storage: str - The type of storage.
        :param UOM: str - The unit of measure.
        :param UOM_ID: str - The id of the  unit of measure.
        :param SCALAR_FACTOR: str -The scalar factor.
        :param SCALAR_ID: str - The scalar's ID.
        :param VECTOR: str - The vector factor.
        :param COORDINATE: str - The coordinate information.
        :param VALUE: str - The value of the storage information.
        :param STATUS: str - The status of the storage information.
        :param SYMBOL: str - The symbol associated with the storage information.
        :param TERMINATED: str - The termination status of the storage information.
        :param DECIMALS: str - The number of decimal places in the storage value.

        """
        self.params = {}
        self.columns = [
            'REF_DATE', 'GEO', 'DGUID', 'Type of product',
            'Type of storage', 'UOM', 'UOM_ID', 'SCALAR_FACTOR',
            'SCALAR_ID', 'VECTOR', 'COORDINATE', 'VALUE', 'STATUS',
            'SYMBOL', 'TERMINATED', 'DECIMALS'
        ]
        self.params['REF_DATE'] = REF_DATE
        self.params['GEO'] = GEO
        self.params['DGUID'] = DGUID
        self.params['Type of product'] = Type_of_product
        self.params['Type of storage'] = Type_of_storage
        self.params['UOM'] = UOM
        self.params['UOM_ID'] = UOM_ID
        self.params['SCALAR_FACTOR'] = SCALAR_FACTOR
        self.params['SCALAR_ID'] = SCALAR_ID
        self.params['VECTOR'] = VECTOR
        self.params['COORDINATE'] = COORDINATE
        self.params['VALUE'] = VALUE
        self.params['STATUS'] = STATUS
        self.params['SYMBOL'] = SYMBOL
        self.params['TERMINATED'] = TERMINATED
        self.params['DECIMALS'] = DECIMALS

    def get(self, columnname):
        if columnname in self.params:
          return self.params[columnname]
        else:
          print('No such kind of column: ' + columnname)
      
    def set(self, columnname, newval):
        if columnname in self.params:
          self.params[columnname] = newval
        else:
          print('No such kind of column: ' + columnname)

    def __str__(self):
        """
        Returns a string representation of the VegetableStorage object.
        :return: a string containing the values of the object's attributes
        """
        res = ''
        for i in self.columns[:-1]:
            res += self.params[i] + ','
        res += self.params[self.columns[-1]]
        return res

    #Author:Xiaoping Zhang
    #Date: July 22, 2023
    def get_description(self):
       return '''Vegetables are parts of plants that are consumed by 
       humans or other animals as food. The original meaning is still
        commonly used and is applied to plants collectively 
        to refer to all edible plant matter, including the flowers,
         fruits, stems, leaves, roots, and seeds.'''


