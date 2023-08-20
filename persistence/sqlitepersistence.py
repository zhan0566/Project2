import csv
import re
import sqlite3
from multiprocessing.pool import Pool
import time
#Author:Xiaoping Zhang
#Date: August 05, 2023

class SQLtab:

    def __init__(self, tabname, dbpath) -> None:
        """
        Constructor method of the class, that create and initialize objects of class SQLtab.
        :param tabname: table name
        :param dbpath: database path
        """
        self.tabname = tabname
        self.dbpath = dbpath
        self.connection = sqlite3.connect(self.dbpath)
        self.column_names = self.get_column_names()
    
    def dropTable(self):
        """
        Drop a table from database
        :return:
        """
        sql = 'DROP TABLE {}'.format(self.tabname)
        try:
            self.connection.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(e)

    # Author:Xiaoping Zhang
    # Date: July 22, 2023
    def createTable(self, tablename:str, columnlist:list) -> bool:
        """
        Create a new table in an SQLite database with specified table name and column list.
        :param tablename: A string representing the name of the table to be created.
        :param columnlist: A List containing the name of the columns for a new table.
        :return:
        """
        cols = ''
        'This is a loop that iterates through each element in the columnlist.'
        for i in columnlist:
            if len(cols) > 0:
                cols += ',\n'
            cols += i + ' text'
        sql = '''
            CREATE TABLE {} (
                record_id INTEGER PRIMARY KEY, 
                {}
            )
        '''.format(tablename, cols)
        try:
            self.connection.execute(sql)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def commit(self):
        self.connection.commit()

    # Author:Xiaoping Zhang
    # Date: July 22, 2023

    def get_column_names(self) -> list:
        """
         Obtain the names of all the columns in a specific table within the SQLite database.
        :return: a list of column name
        """
        info = self.connection.execute('PRAGMA table_info({})'.format(self.tabname))
        columnname = []
        for arr in info.fetchall():
            columnname.append(arr[1])
        return columnname
    
    def insertOneWithCommit(self, vallist):

        vallist = ['\'{}\''.format(i) for i in vallist]
        sql = 'INSERT INTO {}({})\n VALUES({})'.format(
            self.tabname, 
            ', '.join(self.column_names[:len(vallist)]), 
            ', '.join(vallist)
        )
        print('    SQL for insert is:\n    {}'.format(sql))
        try:
            self.connection.execute(sql)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def insertOne(self, vallist):
        vallist = ['\'{}\''.format(i) for i in vallist]
        sql = 'INSERT INTO {}({}) VALUES({})'.format(
            self.tabname, 
            ', '.join(self.column_names[:len(vallist)]), 
            ', '.join(vallist)
        )
        try:
            self.connection.execute(sql)
        except Exception as e:
            print(e)


    def initDBbyCSV(self, filename):
        '''
        loading the data into database from CSV file using multithread.
        :param filename : a csv file with column names as its first line
        '''
        res = []
        # read the csv
        csv_reader = csv.reader(open(filename, "r", encoding='utf-8'), delimiter=',')
        # skip but maintain the first line
        column_name = next(csv_reader)
        
        # trim the file prefix, get column name by re module.
        for i in range(len(column_name)):
            if '"' in column_name[i]:
                column_name[i] = re.search(r'"(.*?)"', column_name[i]).group(1)
            # replace the space with '_'
            if len(column_name[i].split()) > 0:
                column_name[i] = '_'.join(column_name[i].split())
        # call createTable method
        isCreated = self.createTable(tablename=self.tabname, columnlist=column_name)
        if not isCreated: # this means that the table is created or has other problems, stop reading data
            return 
        else:
            self.column_names = column_name
            # multithreading load the data into the table.
            p = Pool(3)
            params = [(filename, 1, 2500), (filename, 2500, 5000), (filename, 5000, 10000)]
            res = p.starmap(self.readCSV, params)
            p.close()
            p.join()
            finalRes = []
            for i in res:
                finalRes.extend(i)
            for vallist in finalRes:
                self.insertOne(vallist)
            self.commit()
            print('Successfully load {} records from {}.'.format(len(finalRes), filename))
    
    @staticmethod
    def readCSV(filename, start, end):
        """
        Read CSV file into list.
        :param filename: a csv file
        :param start:
        :param end:
        :return:
        """
        csv_reader = csv.reader(open(filename, "r", encoding='utf-8'), delimiter=',')
        # skip but the first column line
        next(csv_reader)
        raws = []
        cnt = 0
        for i in csv_reader:
            cnt += 1
            if start <= cnt <= end:
                raws.append(i)
        return raws
    
    def getDataByCol(self, col_name=None, col_val=None, size=None):
        sql = 'SELECT * FROM {}'.format(self.tabname)
        if col_name is not None:
            sql += ' WHERE {} = \'{}\''.format(col_name, col_val)
        if size is not None:
            sql += ' LIMIT {}'.format(size)
        try:
            res = []
            for i in self.connection.execute(sql):
                res.append(i) # remove the record_id
            return res
        except Exception as e:
            print(e)
            return None

    # Author:Xiaoping Zhang
    # Date: August 05, 2023
    def getBarSum(self, main_col_name, val_col_name):
        """
        Retrieve the sum of values in a value_column grouped by a main_column from a database table.
        :param main_col_name: The name of the main column to group by.
        :param val_col_name:The name of the value column for which the sum will be calculated.
        :return:A list of tuples, each containing a value from the main column and the corresponding sum of values
            from the value column. For example, [('carrot', sum1), ('potatoes', sum2), ...]
        """
        sql = 'SELECT {0}, SUM(CAST({1} AS DECIMAL)) FROM {2} GROUP BY {0}'.format(main_col_name, val_col_name, self.tabname)
        try:
            res = []
            for i in self.connection.execute(sql):
                res.append(i)
            return res
        except Exception as e:
            print(e)
            return None

    def getBarCnt(self, col_name):
        """
        Retrieve the count of occurrences for distinct values in a specified column from a database table.
        This method executes an SQL query to count the number of occurrences of each distinct value in the given column,
        grouping the results by the distinct values themselves.

        :param col_name:The name of the column for which the occurrence count will be calculated.
        :return: A list of tuples, each containing a distinct value from the column and its corresponding occurrence count.
                 For example, [('British Columnbia', count1), ('Quebec', count2), ...]
        """
        sql = 'SELECT {0}, COUNT() FROM {1} GROUP BY {0}'.format(col_name, self.tabname)
        try:
            res = []
            for i in self.connection.execute(sql):
                res.append(i)
            return res
        except Exception as e:
            print(e)
            return None

    def execAndCommit(self, sql):
        try:
            self.connection.execute(sql)
            self.commit()
            return True
        except Exception as e:
            print(e, 'sql=', '"{}"'.format(sql))
        return False


    def showBySortCol(self, colname, size=None):
        """
        Display data from a database table.
        :param colname:The name of the column by which the data should be sorted.
        :param size: An optional parameter that specifies the maximum number of records to retrieve and display.
        :return:
        """
        sql = 'SELECT * FROM {0} WHERE {1} != \'\' ORDER BY {1} DESC'.format(self.tabname, colname)
        if size is not None:
            sql += ' LIMIT {}'.format(size)
        try:
            for record in self.connection.execute(sql):
                print(record)
            print('**********')
        except Exception as e:
            print(e)

    def showRawData(self, size=None):
        """
        Display raw data from a database table without applying any sorting.
        :param size: An optional parameter that specifies the maximum number of records to retrieve and display
        :return:
        """
        sql='SELECT * FROM {}'.format(self.tabname)
        if size is not None:
            sql += ' LIMIT {}'.format(size)
        try:
            for record in self.connection.execute(sql):
                print(record)
            print('**********')
        except Exception as e:
            print(e)

    @staticmethod
    def readOneByOne(dbpath, tabname, start, end):
        """
        Read data from an SQLite database table using single thread.
        :param dbpath:
        :param tabname:
        :param start:
        :param end:
        :return:
        """

        now = time.time()
        conn = sqlite3.connect(dbpath)
        for i in range(start, end):
            sql = 'SELECT * FROM {} WHERE record_id = {}'.format(tabname, i)
            try:
                conn.execute(sql)
            except Exception as e:
                print(e)
        print('Read {} records with single thread cost: {}s'.format(end - start + 1, time.time() - now))
        return time.time() - now



    def readByMultiThread(self, start, end):
        """
         Read data from an SQLite database table using multiple threads to improve performance.
        :param start: The starting index or ID from which data will be read.
        :param end:The ending index or ID up to which data will be read.
        :return:
        """
        now = time.time()
        thread = 3
        p = Pool(thread)
        params = []
        for i in range(thread):
            params.append((self.dbpath, self.tabname, start + i * (end - start) // thread, start + (i + 1) * (end - start) // thread))
        p.starmap(self.readOneByOne, params)
        p.close()
        p.join()
        print('Read {} records with {} threads cost: {}s'.format(end - start + 1, thread, time.time() - now))
        return time.time() - now