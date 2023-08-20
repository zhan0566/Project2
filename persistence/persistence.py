#Author:Xiaoping Zhang
#Date: August 05, 2023

import csv
from model.vegetableStorage import VegetableStorage

class Persistence:

    def persist(self, datas, target_file_path, column_names, src_file=''):
        """
        Write the data into a file
        :param datas: a list of in-memory records
        :param target_file_path: the name of a file to be written
        :param column_names: names of columns
        :param src_file: the name of source data
        :return:
        """
        if target_file_path == src_file:
            print('Persistence filename can not be the same as source.')
            return None
        with open(target_file_path, 'w', encoding='utf-8-sig') as file:
            # follow the stored style in original csv
            # manually add double quote
            t = []
            for i in column_names:
                t.append('"' + i + '"')
            file.write(','.join(t) + '\n')
            for i in range(len(datas)):
                record = datas[i]
                # build the persisted record string
                recordstr = ''
                for idx in range(len(column_names)):
                    col = column_names[idx]
                    recordstr += '"' + record.get(col) + '"'
                    if idx < len(column_names) - 1:
                        recordstr += ','
                # check if it is the last record to avoid redundant line break
                if i < len(datas) - 1:
                    recordstr += '\n'
                file.write(recordstr)
        print('Successfully persist data to ' + target_file_path)

    def readCSV(self, filename, n=None):
        """
        Read data from a CSV file, store each line into every object, and return a list of VegetableStorage object.
        :param filename: The file to be read.
        :param n: The first "n" of records to be parsed.
        :return: A list that stored the data from the .csv file.
        """
        try:
            res = []
            with open(filename, "r", encoding='utf-8-sig') as file:
                ''' 
                Reads the CSV file using the `csv.reader` function.
                
                Parameters:
                - file:  the CSV file to be read.
                - delimiter: The character used to separate the fields in the CSV file.
                
                Returns:
                A reader object that can be iterated over to access the CSV data row by row.
                '''
                csv_reader = csv.reader(file, delimiter=',')
                # skip but maintain the first line
                column_name = next(csv_reader)
                # Author:Xiaoping Zhang
                # Date: May 19, 2023
                for line in csv_reader:
                    '''
                    Uses a for loop to access CSV file
                    Assigns the value of each variable.
                    
                    '''
                    REF_DATE = line[0]
                    GEO = line[1]
                    DGUID = line[2]
                    Type_of_product = line[3]
                    Type_of_storage = line[4]
                    UOM = line[5]
                    UOM_ID = line[6]
                    SCALAR_FACTOR = line[7]
                    SCALAR_ID = line[8]
                    VECTOR = line[9]
                    COORDINATE = line[10]
                    VALUE = line[11]
                    STATUS = line[12]
                    SYMBOL = line[13]
                    TERMINALTED = line[14]
                    DECIMALS = line[15]

                    """
                    Author: Xiaoping Zhang
                    Create a object 'tmpveg' for class of VegetableStorage.
                    and pass a bunch of parameters.
                    """
                    tmpveg = VegetableStorage(
                        REF_DATE,
                        GEO,
                        DGUID,
                        Type_of_product,
                        Type_of_storage,
                        UOM,
                        UOM_ID,
                        SCALAR_FACTOR,
                        SCALAR_ID,
                        VECTOR,
                        COORDINATE,
                        VALUE,
                        STATUS,
                        SYMBOL,
                        TERMINALTED,
                        DECIMALS
                    )
                    res.append(tmpveg)
                    '''
                    Stop parsing when it reaches n records.
                    '''
                    if n is not None and len(res) >= n:
                        break
            return column_name, res

        except OSError as e:
            print(e.errno)

print("Program by Xiaoping Zhang")
if __name__ == '__main__':
    a, b = Persistence().readCSV('32100260.csv')
    print(a)