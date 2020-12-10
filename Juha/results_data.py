#-*- coding: UTF8 -*-
# 
# """https://pypi.org/project/list-dict-DB/"""
#
# LIST-DICT-DB
#
import json
from createanyclass import create_class_instance as cci
from dictionaries import dictionaries as dic
from list_dict_DB import list_dict_DB
DBI = list_dict_DB()

#
# Singleton class creates dict_db class if no instancies are running 
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    #
#    
class dict_db(metaclass=Singleton):
    def __init__(self,balance=0,DB=DBI,db_json=''):
        self.balance = balance
        self.DB = DBI
        self.db_json = db_json
        #self.initialize(DB)
    
    
    def set_list_dict_db(self,value:object):
        """[Set the dictionary instance from dictionary class]

        Args:
            value (Dictionary object): [Dictionary data object]
        """
        self.list_dict_db=value
        
    def get_list_dict_db(self):
        return self.list_dict_db         
    
    def set_db_jason(self,file_path):
        """[set json data file path and name]

        Args:
            file_path ([str]): [file name and path]
        """
        self.db_json = file_path
        
    def get_db_json(self)->str():
        """[summary]

        Returns:
            [json]: [Returns json object path and name]
        """
        return self.db_json     
            
    # def initialize(self,DBI):
    #    print(type(DBI))
    #    set_list_dict_db(self,DBI)
    #
    #
    # Nice to know one way to build dictionary filter with simple sql like (not sql) syntax 
    # like "select * from items where first = 'Matti'"  
    def get_words(self):
        #
        # Should be build dynamically to get tbl/item and column/item[]
        words = []
        words = [{'select' : 'item for item '},
                {'from' : 'in '},
                {'items' : 'items '},
                {'where' : 'if '}]
        
        return words
    
    #
    def get_dictionary_data(self,query_string:str,dict_name:str):
        """[Search with dynamic queries of different dictionaries]

        Args:
            query_string (str): [search_string]
            dict_name (str): [dictionary_name]

        Returns:
            [list]: [result_list of dictionaries]
        """
        # print('dic.get_dict_' + dict_name + '(dic)')
        items = eval('dic.get_dict_' + dict_name + '(dic)')
        # print(query_string)
        return eval(query_string)
    
        #
    def get_dictionary(self,dict_name:str):
        """[Search with dynamic queries of different dictionaries]

        Args:
            query_string (str): [search_string]
            dict_name (str): [dictionary_name]

        Returns:
            [list]: [result_list of dictionaries]
        """
        # print('dic.get_dict_' + dict_name + '(dic)')
        items = eval('dic.get_dict_' + dict_name + '(dic)')
        # print(query_string)
        return items
        # ToDo: maybe wise to do with pickle not json
    
    # text = 'Hello'
    # data=json.dumps(text) # to json
    # text=json.loads(data) # to text
    #       
    def json_dump(self,db_json_path):
        """[dump to file from DB ]

        Args:
            db_json ([type]): [description]
        """
        with open(db_json_path,'w') as F:
            value_DB = get_list_dict_db()
            json.dump(value_DB.items(),F)
    
    def json_load(self,db_json_path):
        """[load from file to DB]

        Args:
            db_json ([type]): [description]
        """
        with open(db_json_path,'r') as F:
            loaded_DB = list_dict_DB(json.load(F))
            set_list_dict_db(loaded_DB)
    
    def __main__(self):
        """[class main function]
        """
        #-----------------1st-way------------------------
        # 1st way is sql like fecth of data 
        dict_name = 'items' # dictionary name
        sql_string = "select * from items where role = 'guitar'"
        sql_clause = sql_string.split() # to list
        words = self.get_words()
        # print("Search with sql like string")
        search1 = self.sql_to_db_frame(sql_clause, words,dict_name)
        print(search1)
        
        #-----------------2nd-way------------------------
        # 2nd way is search string fetch of data
        # print("Search with [] string")
        # dict_name = 'items' # dictionary name
        query_string = "[item for item in items if item['role']=='guitar']" # Query to get data
        search2 = self.get_dictionary_data(query_string,dict_name)
        print(search2)
    #
    # help function to create DataFrame search Strings
    def sql_to_db_frame(self,sql_clause:str,words:list,dict_name:str):
        """[sql to db_frame string builder for dynamic queries of different dictionaries]

        Args:
            sql_clause (str): [description]
        """
        #
        items = eval('dic.get_dict_' + dict_name + '(dic)')
        list_wheres = [] # list of where clause items like (column_pc = 'computer')
        rplc1="item['"
        rplc2="']"
        for index, elem in enumerate(sql_clause):
            if elem == '=': # check for equal(=) sign and left is key and right is value
                if (index+1 < len(sql_clause) and index - 1 >= 0):
                    prev_el = str(sql_clause[index-1]) # previous in list
                    prev_el = rplc1 + prev_el +rplc2 # concatenate to right form with brackets
                    curr_el = str(elem)+str(elem) # center or current in list (here is =)
                    next_el = str(sql_clause[index+1]) # next in list

                    wheres = prev_el + curr_el + next_el # current where clause 
                    list_wheres.append(wheres) # current where clause added to list
        #
        tmp_str = ""
        i=0
        for each_word in sql_clause:
            for word in words:
                if each_word.lower() == list(word.keys())[0].lower():
                    tmp_str = tmp_str + list(word.values())[0].lower()
                else:
                    pass
                
        list_wheres = "".join(list_wheres) # join list to string
        left="["
        right="]"
        search1 = eval(left + tmp_str + list_wheres + right)
        return search1
    
    #
    #
    # from list_dict_DB import list_dict_DB
    # DB = list_dict_DB(items) # Will index them all
    # DB.query(first='George',last='Harrison')
    #
    items = dic.get_dict_items(dic) 
    DB = list_dict_DB(items)
    DB.query( (DB.Q().role == 'guitar') )
    #
    # ToDo: DB is istance of list_dict_DB
    # Q is instance of list_dict_DB --> Qobj()
    # Dictionary X instance is  get_dictionary(X)
    #
    # Q = DB.Qobj(DB) # Instantiate it with the DB. DB.Q() will also work
    result_0 = DB.query( (DB.Q().role =='guitar') )
    print(result_0)
    ##DB.query( (Q.last != 'Meikäläinen') )
    ##DB. DB.Q()
    ##Q = DB.Qobj(DB) 
    result_1 = DB.query( (DB.Q().last == 'Meikäläinen') )
    print(result_1)
    result_2 = DB.query( (DB.Q().first != 'Minna') & (DB.Q().last == 'Meikäläinen'))
    print(result_2)
    result_3 = DB( ~( (DB.Q().role == 'guitar') | (DB.Q().role == 'drums'))) # negate with ~
    print(result_3)

    # Filter lookup if role quitar is true
    Q = DB.Qobj()
    #filt = lambda item: True if item['first'] == 'George' else False
    #DB.query(Q.filter(filt))
    #
    # 
    filt = lambda item: True if item['role'] == 'guitar' else False
    result_4 = DB.query(Q.filter(filt))
    print(result_4)
    
    #Templates
    # search_1 = [item for item in items_x if item['First']=='Mikko' and item['Last']=='Meikäläinen']
    #           select * from    tbl  where first == George  and last == Harrison
    # print(search_1)

    # search_2 = [item for item in items_x if item['Last']=='Meikäläinen']
    #           select * from    tbl  where first == George  and last == Harrison
    # print(search_2)
    #dict_race = {"0": {'Mikko Meikäläinen':{'Kisa' : 'Meikäläisten juoksukisa'}}
    #litems = list()   
    #search_1 = [item for item in items2 if item['first']=='George' and item['last']=='Harrison']
    #           select * from    tbl  where first == George  and last == Harrison
    #print(search_1)
    
            
if __name__ == "__main__":
    #print("*******Start********")
    ddb = dict_db(list([])) # create dict_db runtime object
    # For safety reasons may be better to leave main out !!!
    # For testing it is helpfull
    ddb.__main__() # call dict_db main method
    #ddb.main()

 
 
 
    
    

