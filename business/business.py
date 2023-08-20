from persistence.persistence import Persistence
from model.vegetableStorage import VegetableStorage


class Business:

    def __init__(self, csvfilename, size=100) -> None:
        """
        Constructs the attributes for Business object
        :param csvfilename: the file name to be read
        :param size: the size of file name
        """
        self.csvfilename = csvfilename
        self.size = size
        self.persistence = Persistence()
        self.reload() # initialize data


    def persist(self, target_file_path):
        """
        Write a list of in-memory records into a CSV file
        :param target_file_path:  CSV filename
         
        """
        self.persistence.persist(datas=self.records, target_file_path=target_file_path, column_names=self.column_name, src_file=self.csvfilename)

    def reload(self):
        """
        Load data from a CSV file, store each line into every object, and return a list of VegetableStorage object.
    
        """
        self.column_name, self.records = self.persistence.readCSV(filename=self.csvfilename, n=self.size)
        print('Successfully load {} records from {}.'.format(len(self.records), self.csvfilename))


    def get_needed_records(self, conds):
        """
        Get all records that meet the `conds` dict
        e.g. `conds`: {'REF_DATE': '1970-01', 'GEO': 'Canada'}
        :param conds: a dict requirments
        :return: a list of positions, that meet the requirments in `conds`
        """
        
        tmpidx = []
        for i in range(len(self.records)):
            tmpidx.append(i)
        nextidx = []
        for col, val in conds.items():
            if col not in self.column_name:
                return None
            for j in tmpidx:
                r = self.records[j]
                if r.get(col) == val:
                    nextidx.append(j)
            tmpidx = list(nextidx)
            nextidx = []
        return tmpidx

    def show_by_conds(self, conds):
        """
        Show all records that meet requirements
        :param conds:
        :return:
        """
        idxes = self.get_needed_records(conds)
        
        if idxes is not None:
            for i in idxes:
                print(self.records[i])
        else:
            print('No such record.')
            
    
    def show_n(self, n=None):
        """
        Print the first n records
        :param n: the number of record that user would like to display on the screen

        """
        count = 0
        for record in self.records:
            count += 1
            print(record)
            if n is not None and count >= n:
                break
   
    def update_a_record(self, conds, column, newval):
        """
        Update a existing record in CSV file
        :param conds:a dict requirments
        :param column: a column name 
        :param newval: a new value
        
        """
        if column not in self.column_name:
            print('In update_a_record(), no such column: ' + column)
            return None
        idxes = self.get_needed_records(conds)
        # if we found at least one needed record
        if idxes is not None and len(idxes) > 0:
            # update the first record that meets all conds
            record = self.records[idxes[0]]
            record.set(column, newval)
            print('Update one record successfully')
        else:
            print('No such record:' + str(conds))
    # 
    def delete_a_record(self, conds):
        """
        Delete the first record that meets all requirements provided by conds in CSV file
        :param conds: a dict requirments
        """
        idxes = self.get_needed_records(conds)
        # if we found at least one needed record
        if idxes is not None and len(idxes) > 0:
            self.records.pop(idxes[0])
            print('Delete one record successfully')
        else:
            print('No such record:' + str(conds))
    def add_a_record(self, record_dict):
        """
        Add a record into a CSV file
        :param record_dict: a dict record, that include all values
        """
        val = []
        for i in self.column_name: # keep order
            val.append(record_dict[i])
        a_record = VegetableStorage(
            val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9], val[10], val[11], val[12], val[13], val[14], val[15]
        )
        self.records.append(a_record)
        print('add a record  successful ')

if __name__ == '__main__':
    # Simple test For Business Layer
    filename = '../data/32100260.csv'
    bus = Business(filename, 5)
    bus.show_n()
    print('***********************')
    conds = {'Type of product':'Potatoes', 'GEO': 'Canada'}
    bus.update_a_record(conds, 'Type of product', 'Jesus')
    bus.show_n()
    print('***********************')
    conds = {'Type of product':'Potatoes', 'GEO':'Maritime provinces'}
    bus.delete_a_record(conds)
    bus.show_n()
    print('***********************')
    bus.persist('tmp.csv')
    # bus.show_n()

    
    
