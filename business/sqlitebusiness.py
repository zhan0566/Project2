from persistence.sqlitepersistence import SQLtab
from model.vegetableFactory import *


class SQLBusiness:

    def __init__(self, csvfilepath, tabname, dbpath) -> None:
        """
        Constructs the attributes for Business object
        :param csvfilepath: the file path to be read
        """
        self.csvfilepath = csvfilepath
        self.tabname = tabname
        self.dbpath = dbpath
        self.persistence = SQLtab(tabname, dbpath)
        self.reload() # initialize data
        self.column_name = self.get_column_names()

    def reload(self):
        """
        Multithread load records from CSV file to SQLite.
        """
        # remove existed table
        self.persistence.dropTable()
        self.persistence.initDBbyCSV(self.csvfilepath)

    def getDataByGEO(self, geo, size=None):
        """
        Retrieve data from the database based on a specified value in the 'GEO' column.
        :param geo: a name of column
        :param size: the maximum number of records to retrieve and return.
        :return:a list of entities representing the vegetables
        """
        res = self.persistence.getDataByCol(
            col_name='GEO', 
            col_val=geo, 
            size=size
        )
        return self.transferToObj(res)
    
    def getDataByTypeOfProduct(self, type_of_product, size=None):
        """
        Retrieving data from database based on a specified type of vegetable,
        and then converting the retrieved data to a list of entities representing the vegetables
        :param type_of_product: the type of vegetable
        :param size:  the maximum number of records to retrieve and return
        :return: a list of entities representing the vegetables
        """
        res = self.persistence.getDataByCol(
            col_name='TYPE_OF_PRODUCT', 
            col_val=type_of_product, 
            size=size
        )
        
        return self.transferToObj(res)
    
    def getRawData(self, size=None):
        """
        Retrieve data from database, and then convert the retrieved data to a list of entities representing the vegetables
        :param size:the maximum number of records to retrieve and return
        :return:a list of entities representing the vegetables
        """
        res = self.persistence.getDataByCol(
            size=size
        )
        return self.transferToObj(res)
    
    def transferToObj(self, data_list):
        """
        Convert an list of raw data, which obtains from a database query,
        into a list of entities representing vegetables.
        :param data_list:The raw data in data_list to be in a specific order,
        where the first element is the primary key (id) and the remaining elements represent
        the attributes of vegetable
        :return: a list of entities
        """
        transferred_obj = []
        for raw_record in data_list:
            id = raw_record[0]
            obj = VegetableFactory.buildWithList(raw_record[1:]) # remove the first primary key
            transferred_obj.append((id, obj))
        return transferred_obj

    def showBySortDate(self, size=None):
        """
        Obtain the data by sorting with column "REF_DATE" from database
        :param size: the number of records to retrieve
        """
        self.persistence.showBySortCol('REF_DATE', size=size)
    
    def showBySortVALUE(self, size=None):
        """
        Obtain the data by sorting with column "VALUE" from database
        :param size: the number of records to retrieve
        """
        self.persistence.showBySortCol('VALUE', size=size)

    def showRawData(self, size=None):
        """
        Display raw data from a database table without applying any sorting.
        """
        self.persistence.showRawData(size=size)
    
    def deleteOneRow(self, id):
        """
        Delete one row from database
        :param id: the id of the row deleted
        """
        sql = 'DELETE FROM {} WHERE record_id = {}'.format(self.tabname, id)
        if self.persistence.execAndCommit(sql):
            print('Successfly delete one record.')
        else:
            print('Delete fail.')

    def updateOneColInOneRow(self, id, colname, new_val):
        """
        Update a row from database
        :param id: the id of the row
        :param colname: the column name expected to be updated.
        :param new_val: the new value of data
        """
        sql = 'UPDATE {} SET {} = \'{}\' WHERE record_id = {}'.format(self.tabname, colname, new_val, id)
        if self.persistence.execAndCommit(sql):
            print('Successfully update one record.')
        else:
            print('Update fail.')
        
    def get_column_names(self):
        """
        Obtain the names of all columns from specified table `self.tabname` within the SQLite database.
        :return: a list of column names
        """
        return self.persistence.get_column_names()[1:] # ignore the auto-increment primary key

    def add_a_record(self, record_dict:dict):
        """
        Insert one row into database
        :param record_dict: a dictionary containing column names as keys
        and corresponding values representing the data for the new record.
        :return:
        """
        val = []
        for col in self.get_column_names():
            # if 'col' is missed in record_dict, set the value with '' as default
            val.append(record_dict.get(col, '')) 
        if self.persistence.insertOneWithCommit(val):
            print('Successfully insert one record.')
        else:
            print('Insert fail.')



    def getVegetableSum(self):
        """
        Retrieve the sum of values for different types of vegetable products.
        This method calls the `getBarSum` method from the associated `persistence` object to calculate the sum of numeric
        values for different types of vegetable products.

        :return:A tuple containing two lists. The first list contains the types of vegetable products, and the second list
             contains the corresponding summed values. For example, (['carrot', 'potatoes', ...], [1000, 2222, ...])
        """
        res = self.persistence.getBarSum('Type_of_Product', 'VALUE')
        types = [i[0] for i in res]
        vals = [i[1] for i in res]
        return types, vals

    def getGeoCnt(self):
        """
        Retrieve the count for different geographical locations.
        This method calls the `getBarCnt` method from the associated `persistence` object to count the occurrences of
        different geographical locations.
        :return:A tuple containing two lists. The first list contains the geographical locations, and the second list
             contains the corresponding occurrence counts. For example, (['Canada',' Quebec', ...], [500, 500, ...])
        """
        res = self.persistence.getBarCnt('GEO')
        types = [i[0] for i in res]
        vals = [i[1] for i in res]
        return types, vals