"""
A module to easly manage JSON objects using python objects
"""
from io import TextIOWrapper
from types import NoneType
def _tabs(num):
    s = ""
    for i in range(num):
        s+= "\t"
    return s

def Help():
    print("A module to easly manage JSON objects using python objects")

class JsonArray:
    """
    A way to store JSON arrays using python objects.
    
    The elements are a list of JsonValue. If nothing is passed in the constructor, an empty array will be created.
    """
    def __init__(self, elements:list=None):
        if not elements:
            self.elements = list()
        else:
            self.elements = elements
        for el in self.elements:
            if hasattr(el,"_internal"):
                if not el._internal() == "AKsj478)//#=774gGhsggH5362L":
                    raise TypeError("Every value must be of type 'JsonValue'")
            else:
                raise TypeError("Every value must be of type 'JsonValue'") 
        
    def Add(self,element):
        """
        Add a JsonValue to the elements.
        """
        if hasattr(element,"_internal"):
            if not element._internal() == "AKsj478)//#=774gGhsggH5362L":
                raise TypeError("Every value must be of type 'JsonValue'")
        else:
            raise TypeError("Every value must be of type 'JsonValue'") 
        self.elements.append(element)
        
    def Remove(self,element):
        """
        Remove a JsonValue from the elements.
        """
        self.elements.remove(element)
      
    def Set(self,elements):
        """
        Set the elements. The list must contain JsonValue objects.
        """
        self.elements = elements
        for el in self.elements:
            if hasattr(el,"_internal"):
                if not el._internal() == "AKsj478)//#=774gGhsggH5362L":
                    raise TypeError("Every value must be of type 'JsonValue'")
            else:
                raise TypeError("Every value must be of type 'JsonValue'") 
      
    def Contains(self,element)->bool:
        """
        Check if a JsonValue element is in the elements.
        """
        return element in self.elements
    
    def ContainsType(self,type:str)->bool:
        """
        Check if one or more elements are of the specified type.
        """
        for e in self.elements:
            if e.type == type:
                return True
        return False
    
    def GetOfType(self,type:str)->list:
        """
        Return all the elements of the type specified.
        """
        values = list()
        for e in self.elements:
            if e.type == type:
                values.append(e)
        return values
    
    def _internal_str(self,tabs):
        if len(self.elements) <= 0:
            return "[]"
        string = "[\n"
        for i,el in enumerate(self.elements):
            string += _tabs(tabs+1)+el._internal_str(tabs+1)
            if (i<len(self.elements)-1):
                string += ","
            string += "\n"
        return string+_tabs(tabs)+"]"
        
    def __str__(self) -> str:
        if len(self.elements) <= 0:
            return "[]"
        string = "[\n"
        for i,el in enumerate(self.elements):
            string += "\t"+el._internal_str(1)
            if (i<len(self.elements)-1):
                string += ","
            string += "\n"
        return string+"]"
            
    def Copy(self):
        """
        Return a new JsonArray with the same elements.
        """
        return JsonArray([el.Copy() for el in self.elements])
            
    def Merge(self,jsonArray):
        """
        Merge itself with another JsonArray.
        """
        self.elements += jsonArray.elements        
   
    def Format(self)->str:
        """
        Return a string representation of the JsonArray correctly formatted and indented.
        
        Same as calling __str__.
        """
        return self.__str__()
    
class JsonPair:
    """
    The pair type of a JsonObject. Stores the key (string) and value (JsonValue).
    """
    def __init__(self, key:str, value):
        self.key = key
        self.value = value
        if not isinstance(self.key,str):
            raise TypeError("Key must be of type 'str'")
        if hasattr(self.value,"_internal"):
            if not self.value._internal() == "AKsj478)//#=774gGhsggH5362L":
               raise TypeError("Value must be of type 'JsonValue'")
        else:
            raise TypeError("Value must be of type 'JsonValue'")
        self.value.pairReference = self 
        
    def Copy(self):
        """
        Return a new JsonPair with the same key and value.
        """
        return JsonPair(self.key,self.value.Copy())
        
    def Compare(self, pair)->bool:
        """
        Check whether a specified pair has the same key and value.
        """
        return self.key == pair.key and self.value.Compare(pair.value)
    
    def CompareKey(self,pair)->bool:
        """
        Checks whether a specified pair has the same key.
        """
        return self.key == pair.key
    
    def SetKey(self,key:str):
        """
        Changes the key.
        """
        if not isinstance(key,str):
            raise TypeError("Key must be of type 'str'")
        self.key = key
        
    def SetValue(self,value):
        """
        Changes the value.
        """
        self.value.pairReference = None
        if hasattr(value,"_internal"):
            if not value._internal() == "AKsj478)//#=774gGhsggH5362L":
               raise TypeError("Value must be of type 'JsonValue'")
        else:
            raise TypeError("Value must be of type 'JsonValue'")
        self.value = value
        self.value.pairReference = self
    
    def _internal_str(self,tabs):
        return '"'+self.key+'"'+f':{self.value._internal_str(tabs)}'
    
    def __str__(self):
        return '"'+self.key+'"'+f':{str(self.value)}'

    def Format(self):
        """
        Return a string representation of the JsonPair correctly formatted and indented.
        
        Same as calling __str__.
        """
        return self.__str__()

class JsonObject:
    """
    A python object rapresenting a JSON object. Contains a lot of useful functions to get informations.
    
    Contains a list of JsonPair.
    
    If nothing is passed in the constructor, an empty object will be created.
    """
    def __init__(self,pairs=None):
        if not pairs:
            self.pairs = list()
        else:
            self.pairs = pairs
        for pair in self.pairs:
            if not isinstance(pair,JsonPair):
                raise TypeError("Every pair must be of type 'JsonPair'")
    
    def Add(self,pair:JsonPair):
        """
        Add a JsonPair to the pairs.
        """
        if not isinstance(pair,JsonPair):
            raise TypeError("Pair must me of type 'JsonPair'")
        self.pairs.append(pair)
        
    def Remove(self,pair:JsonPair):
        """
        Remove a JsonPair from the pairs.
        """
        self.pairs.remove(pair)
        
    def Contains(self,pair:JsonPair,inChildren:bool=True)->bool:
        """
        Checks if a pair is contained in the pairs.
        
        When isChildren is True the children object will be checked aswell.
        """
        hasMe =  pair in self.pairs
        if hasMe:
            return True
        else:
            if inChildren:
                for pair in self.pairs:
                    if pair.value.type == "Object":
                        hasPair = pair.value.value.Contains(pair,True)
                        if hasPair: 
                            return True
        return False
    
    def ContainsKey(self,key:str,inChildren:bool=True)->bool:
        """
        Checks if a key is contained in the pairs.
        
        When isChildren is True the children object will be checked aswell.
        """
        keys = self.GetKeys(inChildren)
        return key in keys
    
    def GetKeys(self,inChildren:bool=True)->bool:
        """
        Return all the keys in the pairs.
        
        When isChildren is True the children object will be checked aswell.
        """
        keys = []
        if not inChildren:
            for pair in self.pairs:
                keys.append(pair.key)
            return keys
        else:
            for pair in self.pairs:
                keys.append(pair.key)
                if pair.value.type == "Object":
                    for k in pair.value.value.GetKeys(True):
                        keys.append(k)
            return keys
    
    def GetValue(self,key:str,inChildren:bool=True,returnValueIfNotFound=None):
        """
        Tries to get the value of a specified key. If none is found it will return the value specified. If there are duplicates the first value will be returned.
        
        When isChildren is True the children object will be checked aswell.
        """
        if self.ContainsKey(key,inChildren):
            for pair in self.pairs:
                if pair.key == key:
                    return pair.value
                else:
                    if inChildren:
                        if pair.value.type == "Object":
                            return pair.value.value.GetValue(key,True,returnValueIfNotFound)  
        return returnValueIfNotFound
    
    def GetValues(self,key:str,inChildren:bool=True)->list:
        """
        Return all the values of a speicified key.
        
        When isChildren is True the children object will be checked aswell.
        """
        values = list()
        if self.ContainsKey(key,inChildren):
            for pair in self.pairs:
                if pair.key == key:
                    values.append(pair.value)
                else:
                    if inChildren:
                        if pair.value.type == "Object":
                            for v in pair.value.value.GetValues(key,True):
                                values.append(v) 
        return values
    
    def GetValuesOfType(self,type:str,inChildren:bool=True)->list:
        """
        Return all the values of a speicified type.
        
        When isChildren is True the children object will be checked aswell.
        """
        values = list()
        if inChildren:
            for p in self.pairs:
                if p.value.type == type:
                    values.append(p.value)
                if p.value.type == "Object":
                    for v in p.value.value.GetValuesOfType(type,True):
                        values.append(v)
            return values
        else:
            for p in self.pairs:
                if p.value.type == type:
                    values.append(p.value)
            return values
    
    def ContainsDuplicate(self,key:str,inChildren:bool=True)->bool|int:
        """
        Checks if there are more of the same key. If it is the case, the number of times it has been found will be returned.
        
        When isChildren is True the children object will be checked aswell.
        """
        if self.ContainsKey(key,inChildren):
            keys = self.GetKeys()
            c = keys.count(key)
            if c> 1:
                return c
        return False
    
    def RemoveDuplicate(self,key:str,inChildren:bool=True):
        """
        Remove all the pairs that has the same specified keys.
        
        When isChildren is True the children object will be checked aswell.
        """
        found = False
        toRemove = []
        for p in self.pairs:
            if p.key == key:
                if not found:
                    found = True
                else:
                    toRemove.append(p)
        for pp in toRemove:
            self.Remove(pp) 
        if inChildren:
            for ppp in self.pairs:
                if ppp.value.type == "Object":
                    ppp.value.value.RemoveDuplicate(key,True)
    
    def RemoveDuplicates(self,inChildren:bool=True):
        """
        Remove all the pairs that has the same keys.
        
        When isChildren is True the children object will be checked aswell.
        """
        found = []
        toRemove = []
        for p in self.pairs:
            if p.key not in found:
                found.append(p.key)
            else:
                toRemove.append(p)
        for pp in toRemove:
            self.Remove(pp)
        if inChildren:
            for ppp in self.pairs:
                if ppp.value.type == "Object":
                    ppp.value.value.RemoveDuplicates(True)
    
    def Copy(self):
        """
        Return a new JsonObject with the same pairs.
        """
        return JsonObject([p.Copy() for p in self.pairs])
    
    def Merge(self,jsonObject):
        """
        Adds the pairs of a specified JsonObject to itself.
        """
        self.pairs += jsonObject.pairs
    
    def _internal_str(self,tabs):
        if len(self.pairs) <= 0:
            return "{}"
        string = "{\n"
        for i,pair in enumerate(self.pairs):
            string += _tabs(tabs+1)+pair._internal_str(tabs+1)
            if (i < len(self.pairs)-1):
                string += ","
            string += "\n"
        return string+_tabs(tabs)+"}"
    
    def __str__(self):
        if len(self.pairs) <= 0:
            return "{}"
        string = "{\n"
        for i,pair in enumerate(self.pairs):
            string += "\t"+pair._internal_str(1)
            if (i < len(self.pairs)-1):
                string += ","
            string += "\n"
        return string+"}"

    def Format(self):
        """
        Return a string representation of the JsonObject correctly formatted and indented.
        
        Same as calling __str__.
        """
        return self.__str__()

class JsonType:
    """
    A static class containing the JSON supported types as string and some useful static methods.
    """
    
    String = "String"
    Number = "Number"
    Object = "Object"
    Array = "Array"
    Boolean = "Boolean"
    Null = "Null"
    
    @staticmethod
    def Compare(type1:str,type2:str)->bool:
        """
        (static) Check if two types are the same.
        """
        return type1 == type2
    
    @staticmethod
    def Get(value)->str:
        """
        (static) Finds the JsonType of a python object if supported.
        """
        if isinstance(value,str):
            return JsonType.String
        elif isinstance(value,bool):
            return JsonType.Boolean
        elif isinstance(value,(int,float)):
            return JsonType.Number
        elif isinstance(value,JsonObject):
            return JsonType.Object
        elif isinstance(value,JsonArray):
            return JsonType.Array
        
        elif value == None:
            return JsonType.Null
        else:
            raise TypeError(f"Unsupported type '{type(value)}'")
    
    @staticmethod
    def Validate(type:str,value)->bool:
        """
        (static) Checks whether a python value is of the correct JsonType.
        """
        if type == JsonType.String:
            return isinstance(value,str)
        elif type == JsonType.Boolean:
            return isinstance(value,bool)
        elif type == JsonType.Number:
            return isinstance(value,(int,float))
        elif type == JsonType.Object:
            return isinstance(value,JsonObject)
        elif type == JsonType.Array:
            return isinstance(value,JsonArray)
        
        elif type == JsonType.Null:
            return value == None
        else:
            raise TypeError("Type must be one of the following: String, Number, Object, Array, Boolean, Null, not '"+str(type)+"'")
    
    @staticmethod
    def StringToString(string:str)->str:
        """
        (static) Return the correct string representation of a python string (adds quotes).
        """
        return f'"{string}"'
    
    @staticmethod
    def BooleanToString(boolean:bool)->str:
        """
        (static) Convert a python boolean to a JSON boolean.
        """
        return str(boolean).lower()
    
    @staticmethod
    def NullToString()->str:
        """
        (static) Just returns 'null'.
        
        Why not.
        """
        return "null"

class JsonValue:
    """
    A python object storing a JSON supported type and its corrisponding value.
    
    The value can be any of the supported types.
    """
    def __init__(self,type:str,value:int|float|bool|NoneType|JsonObject|JsonArray):
        self.type = type
        self.value = value
        if not JsonType.Validate(self.type,self.value):
            raise ValueError(f"Type '{self.type}' doesn't match with the type of '{self.value.__class__.__name__}'")
        self.pairReference = None
        
    def Compare(self,value)->bool:
        """
        Checks whether a value has the same type and value.
        """
        return self.value == value.value and self.type == value.type
    
    def CompareType(self,value)->bool:
        """
        Checks wheter a value is of the same type.
        """
        return self.type == value.type
    
    def Copy(self):
        """
        Return a new JsonValue with the same type and value.
        """
        return JsonValue(self.type,self.value)
    
    def Set(self,value:int|float|bool|NoneType|JsonObject|JsonArray,type:str="Auto"):
        """
        Changes the value and the type. When the type is set to Auto it will be set automatically.
        """
        if type == "Auto":
            type = JsonType.Get(value)
        self.type = type
        self.value = value
        if not JsonType.Validate(self.type,self.value):
            raise ValueError(f"Type '{self.type}' doesn't match with the type of '{self.value.__class__.__name__}'")
    
    def _internal_str(self,tabs):
        if self.type == JsonType.String:
            return JsonType.StringToString(self.value)
        elif self.type == JsonType.Boolean:
            return JsonType.BooleanToString(self.value)
        elif self.type == JsonType.Null:
            return JsonType.NullToString()
        elif self.type == JsonType.Object or self.type == JsonType.Array:
            return self.value._internal_str(tabs)
        else:
            return str(self.value)
        
    def __str__(self):
        if self.type == JsonType.String:
            return JsonType.StringToString(self.value)
        elif self.type == JsonType.Boolean:
            return JsonType.BooleanToString(self.value)
        elif self.type == JsonType.Null:
            return JsonType.NullToString()
        else:
            return str(self.value)
        
    def _internal(self):
        return "AKsj478)//#=774gGhsggH5362L"

    def Format(self):
        """
        Return a string representation of the JsonValue correctly formatted and indented.
        
        Same as calling __str__.
        """
        return self.__str__()

class JsonLexer:
    """
    A static class that can convert a string JSON into a list of tokens.
    """
    JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
    JSON_SYNTAX = [",",":","[","]","{","}"]
    JSON_QUOTE = '"'
    NUMBER_CHARACTERS = [str(d) for d in range(0, 10)] + ['-', 'e', '.']
    TRUE_LEN = 4
    FALSE_LEN = 5
    NULL_LEN = 4
    
    @staticmethod
    def LexString(string):
        """
        (static) Tokenize a string.
        """
        json_string = ''

        if string[0] == JsonLexer.JSON_QUOTE:
            string = string[1:]
        else:
            return None, string

        for c in string:
            if c == JsonLexer.JSON_QUOTE:
                return json_string, string[len(json_string)+1:]
            else:
                json_string += c

        raise Exception('Expected end-of-string quote')

    @staticmethod
    def LexNumber(string):
        """
        (static) Tokenize a number.
        """
        json_number = ''

        for c in string:
            if c in JsonLexer.NUMBER_CHARACTERS:
                json_number += c
            else:
                break

        rest = string[len(json_number):]

        if not len(json_number):
            return None, string

        if '.' in json_number:
            return float(json_number), rest

        return int(json_number), rest

    @staticmethod
    def LexBool(string):
        """
        (static) Tokenize a boolean.
        """
        string_len = len(string)

        if string_len >= JsonLexer.TRUE_LEN and string[:JsonLexer.TRUE_LEN] == 'true':
            return True, string[JsonLexer.TRUE_LEN:]
        elif string_len >= JsonLexer.FALSE_LEN and string[:JsonLexer.FALSE_LEN] == 'false':
            return False, string[JsonLexer.FALSE_LEN:]

        return None, string

    @staticmethod
    def LexNull(string):
        """
        (static) Tokenize a null value.
        """
        string_len = len(string)

        if string_len >= JsonLexer.NULL_LEN and string[:JsonLexer.NULL_LEN] == 'null':
            return True, string[JsonLexer.NULL_LEN:]

        return None, string

    @staticmethod
    def Lex(string):
        """
        (static) Convert a string JSON into a list of tokens.
        """
        tokens = []

        while len(string):
            json_string, string = JsonLexer.LexString(string)
            if json_string is not None:
                tokens.append(json_string)
                continue

            json_number, string = JsonLexer.LexNumber(string)
            if json_number is not None:
                tokens.append(json_number)
                continue

            json_bool, string =JsonLexer.LexBool(string)
            if json_bool is not None:
                tokens.append(json_bool)
                continue

            json_null, string = JsonLexer.LexNull(string)
            if json_null is not None:
                tokens.append(None)
                continue

            if string[0] in JsonLexer.JSON_WHITESPACE:
                string = string[1:]
            elif string[0] in JsonLexer.JSON_SYNTAX:
                tokens.append(string[0])
                string = string[1:]
            else:
                raise Exception('Unexpected character: {}'.format(string[0]))

        return tokens

class JsonParser:
    """
    A static class that can convert a list of JSON tokens into a python dictionary and a python dictionary to a JsonObject.
    """
    JSON_COMMA = ','
    JSON_COLON = ':'
    JSON_LEFTBRACKET = '['
    JSON_RIGHTBRACKET = ']'
    JSON_LEFTBRACE = '{'
    JSON_RIGHTBRACE = '}'
    
    @staticmethod
    def ParseArray(tokens):
        """
        (static) Parse a tokenized list.
        """
        json_array = []

        t = tokens[0]
        if t == JsonParser.JSON_RIGHTBRACKET:
            return json_array, tokens[1:]

        while True:
            json, tokens = JsonParser.Parse(tokens)
            json_array.append(json)

            t = tokens[0]
            if t == JsonParser.JSON_RIGHTBRACKET:
                return json_array, tokens[1:]
            elif t != JsonParser.JSON_COMMA:
                raise Exception('Expected comma after object in array')
            else:
                tokens = tokens[1:]

        raise Exception('Expected end-of-array bracket')

    @staticmethod
    def ParseObject(tokens):
        """
        (static) Parse a tokenized object.
        """
        json_object = {}

        t = tokens[0]
        if t == JsonParser.JSON_RIGHTBRACE:
            return json_object, tokens[1:]

        while True:
            json_key = tokens[0]
            if type(json_key) is str:
                tokens = tokens[1:]
            else:
                raise Exception('Expected string key, got: {}'.format(json_key))

            if tokens[0] != JsonParser.JSON_COLON:
                raise Exception('Expected colon after key in object, got: {}'.format(t))

            json_value, tokens = JsonParser.Parse(tokens[1:])

            json_object[json_key] = json_value

            t = tokens[0]
            if t == JsonParser.JSON_RIGHTBRACE:
                return json_object, tokens[1:]
            elif t != JsonParser.JSON_COMMA:
                raise Exception('Expected comma after pair in object, got: {}'.format(t))

            tokens = tokens[1:]

        raise Exception('Expected end-of-object bracket')

    @staticmethod
    def Parse(tokens, is_root=False):
        """
        (static) Parse a tokenized JSON string.
        
        If it has been called manually, remember to pass is_root as true.
        """
        t = tokens[0]

        if is_root and t != JsonParser.JSON_LEFTBRACE:
            raise Exception('Root must be an object')

        if t == JsonParser.JSON_LEFTBRACKET:
            return JsonParser.ParseArray(tokens[1:])
        elif t == JsonParser.JSON_LEFTBRACE:
            return JsonParser.ParseObject(tokens[1:])
        else:
            return t, tokens[1:]
        
    @staticmethod
    def ParseList(jsonList):
        """
        (static) converts a JSON supported python list into a JsonArray.
        """
        lst = JsonArray()
        for e in jsonList:
            if isinstance(e,dict):
                lst.Add(JsonParser.ParseDict(e))
            elif isinstance(e,list):
                lst.Add(JsonParser.ParseList(e))
            else:
                typ = JsonType.Get(e)
                lst.Add(JsonValue(typ,e))
        return JsonValue(JsonType.Array,lst)
        
    @staticmethod
    def ParseDict(jsonDict:dict,is_root=False):
        """
        (static) Converts a JSON supported python dictionary into a JsonObject.
        """
        obj = JsonObject()
        for k in jsonDict.keys():
            v = jsonDict[k]
            if isinstance(v,dict):
                obj.Add(JsonPair(k,JsonParser.ParseDict(v)))
            elif isinstance(v,list):
                obj.Add(JsonPair(k,JsonParser.ParseList(v)))
            else:
                typ = JsonType.Get(v)
                obj.Add(JsonPair(k,JsonValue(typ,v)))
        if is_root:
            return obj
        else:
            return JsonValue(JsonType.Object,obj)

class Json:
    """
    A static class that contains all the main general functions.
    """
    @staticmethod
    def Root()->JsonObject:
        """
        (static) Return a root object. (same as creating an empty JsonObject)
        """
        return JsonObject()
    
    @staticmethod
    def ToObject(stringJSON:str)->JsonObject:
        """
        (static) converts a string representation of JSON to a JsonObject.
        
        Can be done manually using the JsonLexer and JsonParser but is not recommended. 
        """
        lexed = JsonLexer.Lex(stringJSON)
        dicted = JsonParser.Parse(lexed,True)[0]
        return JsonParser.ParseDict(dicted,True)
    
    @staticmethod
    def ToDict(stringJSON:str)->dict:
        """
        (static) coonvert a string representation of JSON to a python dictionary.
        
        Can be also done with the builtin json module.
        """
        lexed = JsonLexer.Lex(stringJSON)
        return JsonParser.Parse(lexed,True)[0]
    
    @staticmethod
    def ToString(jsonObject:JsonObject)->str:
        """
        (static) Format a JsonObject to a python string. Same as calling Format.
        """
        return str(jsonObject)
    
    @staticmethod
    def SaveString(stringJSON:str,fileName:str)->TextIOWrapper:
        """
        (static) Saves a string representation of JSON to a file and returns it.
        """
        with open(fileName,"w") as file:
            file.write(stringJSON)
        return file
    
    @staticmethod 
    def SaveObject(jsonObject:JsonObject,fileName:str)->TextIOWrapper:
        """
        (static) Saves a JsonObject to a file and returns it.
        """
        stringJSON = str(jsonObject)
        with open(fileName,"w") as file:
            file.write(stringJSON)
        return file
    
    @staticmethod 
    def LoadString(fileName:str)->str:
        """
        (static) Loads a JSON from a file and returns it as a string. 
        """
        with open(fileName,"r") as file:
            return file.read()
    
    @staticmethod
    def LoadObject(fileName:str)->JsonObject:
        """
        (static) Loads a JSON from a file and returns it as a JsonObject.
        """
        with open(fileName,"r") as file:
            return Json.ToObject(file.read())
        
    @staticmethod
    def Format(jsonObject:JsonObject|JsonArray|JsonPair|JsonValue)->str:
        """
        (static) Format a Json Object/Array/Pair/Value to a string. Can be called inside the object aswell. 
        """
        return str(jsonObject)
