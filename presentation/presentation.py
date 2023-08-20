import os
# from business.business import Business
from business.sqlitebusiness import SQLBusiness
import matplotlib.pyplot as plt


class Presentation:

    def getcond(self):
        """
        Get a user input column name and corresponding value.
        :return: a dic that has the column name and needed value.
        """
        cond = {}
        col = val = ''
        while col != '#end' and val != '#end':
            print('Enter the column name: ')
            col = input()
            if col == '#end':
                break
            print('Enter the value: ')
            val = input()
            cond[col] = val
        return cond

    def interact(self):
        """
        Interact with users
        """
        print('filename = "data/32100260.csv"')
        print('tablename = "vegetable"')
        print('dbpath = "data/vegetable.db"')
        print('Enter a filename:')
        # filename = "data/32100260.csv"
        # tabname = "vegetable"
        # dbpath = "data/vegetable.db"
        filename = input()
        while not os.path.exists(filename):
            print('No such file: ' + filename)
            filename = input()
        print('Enter the name of the table.')
        tabname = input()
        print('Enter the path of the database.')
        dbpath = input()

        business = SQLBusiness(filename, tabname, dbpath)
        cmd = ''
        while cmd.upper() != 'E':
            print('--CST8333 Project 4 ')
            print('--Program by Xiaoping Zhang')
            print('**********************************')
            print('-- R for reload.')
            print('-- I for create.')
            print('-- U for update.')
            print('-- D for delete.')
            # print('-- sort for persist')
            print('--bar for a bar chart')
            print('-- E for exit.')
            print('--show for output the data in terminal using the following option')
            cmd = input()
            try:
                if cmd.upper() == 'D':
                    print('    Please enter the `id` of deleted record.')
                    id = input()
                    business.deleteOneRow(id)
                elif cmd.upper() == 'U':
                    print('    Please enter the `id` of the updatted record:')
                    id = int(input())
                    print('    Please enter the column name:')
                    updated_column = input()
                    print('    Please enter the new value of the column:')
                    updated_value = input()
                    business.updateOneColInOneRow(id, updated_column, updated_value)
                elif cmd.upper() == 'R':
                    # print('For reload the data from a memory')
                    print('Reaload data from csv to database.')
                    business.reload()
                    print('*******************************************************')
                elif cmd.upper() == 'I':
                    print('For create, please follow the following instructions to fill in the column value one by one.')
                    record_dict = {}
                    for col in business.column_name:
                        print('Please enter the value of column:' + col)
                        val = input()
                        record_dict[col] = val
                    business.add_a_record(record_dict)
                elif cmd == 'show':
                    print('    Choose an option for showing:')
                    print('    - R for raw data;')
                    print('    - G by specific GEO;')
                    print('    - T by specific Type of Product')
                    opt = input()
                    while opt not in 'RGT':
                        print('No such option: {}. please re-enter'.format(opt))
                        opt = input()
                    print('Please enter the number of records you want to show on the terminal:')
                    number = input()
                    while not str(number).isdigit:
                        print('Not a valid number: {}. Please re-enter.'.format(number))
                    if opt == 'R':
                        res = business.getRawData(size=number)
                    elif opt == 'G':
                        print('Please enter the GEO you want:')
                        geo = input()
                        res = business.getDataByGEO(geo, size=number)
                    elif opt == 'T':
                        print('Please enter the type of product you want:')
                        type_of_product = input()
                        res = business.getDataByTypeOfProduct(type_of_product, size=number)
                    for id, obj in res:
                        print(id, obj)
                    print('***************')
                elif cmd == 'sort':
                    print('''    Please choose an sorting type''')
                    print('    - D by Date;')
                    print('    - V by Value.')
                    sorttype = input()
                    while sorttype not in 'DV':
                        print('Get a unexpected input for sorttype: {}, please re-enter.'.format(sorttype))
                        sorttype = input()
                    print('    Please enter the number of records you want to get:')
                    number = input()
                    if sorttype == 'D':
                        business.showBySortDate(number)
                    elif sorttype == 'V':
                        business.showBySortDate(number)
                elif cmd == 'bar':
                    print('--vegetable for generating a bar chart between type of product and value')
                    print('--geo for generating a bar chart of counting the column of "GEO"')
                    cmd = input()
                    if cmd == 'vegetable':
                        axisx, axisy = business.getVegetableSum()
                        xlabel, ylabel = cmd, 'sum'
                    elif cmd == 'geo':
                        axisx, axisy = business.getGeoCnt()
                        xlabel, ylabel = cmd, 'cnt'
                    plt.bar(axisx, axisy)
                    plt.xticks(rotation=45)
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.show()
            except Exception as e:
                print(e)


# if __name__ == '__main__':
#     instance = Presentation()
#     instance.interact()