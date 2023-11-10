import pandas as pd
import json
from dataclasses import make_dataclass
import os
from typing import Union, List

class ReadCsvAndConvertToJSON():

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.file_name: str = os.path.basename(file_path)
        self.class_name: str = self.build_class_name() 

    def extract_name_without_extension(self) -> Union[str, None]:

        splited_file_name = self.file_name.split('.')
        if len(splited_file_name) > 0:
            return splited_file_name[0]
        else:
            return None
    
    def build_class_name(self) -> str:

        file_name = self.extract_name_without_extension()

        splited_file_name = file_name.split('_')
        build_class_name = ''
        if len(splited_file_name) == 1:
            build_class_name = splited_file_name[0].capitalize()
            return build_class_name
        for word in splited_file_name:
            build_class_name += word.capitalize()
        return build_class_name
    
    def read_file(self):
        
        read_data = pd.read_csv(self.file_path, sep = ';', index_col = False, encoding='unicode_escape')
        json_output = self.class_name+'.json'
        read_data.to_json(json_output, indent=1, orient='records')

        with open(json_output, 'r') as file:
            data = json.load(file)
        return data

    
    def create_dynamic_class(self, data):

        class_attrs = []
        class_list = []
        attrs_values = []

        for tuple in data[0].items():
            class_attr = tuple[0]
            print("#####################################")
            print(data[0].items())
            print("#####################################")
            class_attrs.append(class_attr)

        MyClass = make_dataclass(self.class_name, class_attrs)

        for entry in data:
            for key, value in entry.items():
                attrs_values.append(value)
            
            MyClassObject = MyClass(*attrs_values)
            attrs_values = []
            class_list.append(MyClassObject)
        return class_list
        
    