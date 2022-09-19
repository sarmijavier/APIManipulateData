

class CustomSerializer():
    '''
    Class that serialize and unserialize
    - to_dict => serializes
    - from_dict => unserializes
    '''
    def to_dict(self):
        data = {}
        for field in self.fields:
            data[field] = self.__getattribute__(field)

        return data


    def from_dict(self, data):
        for field in self.fields:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def to_simple_collection_dict(query):
        r = []
        for i in query:
            r.append(i.to_dict())

        return r