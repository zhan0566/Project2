from model.vegetableModels import *

class VegetableFactory:
    
    classdict = {
        'onions': Onion, 
        'carrots': Carrot, 
        'cabbage': Cabbage, 
        'potatoes': Potato, 
        'rutabagas': Rutabaga
    }

    # @staticmethod
    # def buildWithDict(record_dict:dict):

    @staticmethod
    def buildWithList(vallist:list):
        # Assume the vals in given vallist follows the order of columns: 
        # REF_DATE,GEO,DGUID,Type_of_product,Type_of_storage,UOM,UOM_ID,SCALAR_FACTOR,SCALAR_ID,VECTOR,COORDINATE,VALUE,STATUS,SYMBOL,TERMINATED,DECIMALS
        type_of_product = vallist[3].lower()
        
        classtype = VegetableFactory.classdict.get(type_of_product, VegetableStorage)
        return classtype(*vallist)