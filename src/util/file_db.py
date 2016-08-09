import leveldb

class FileDB(object):
    def __init__(self, db_path):
        self.__db = leveldb.DB(db_path, create_if_missing=True)

    def set(self, key, value):
        if self.__db and len(key) > 0:
            self.__db.put(key, value)

    def get(self, key):
        if self.__db and len(key) > 0:
            return self.__db.get(key)
        return None

    def delete(self, key):
        if self.__db and len(key) > 0:
            self.__db.delete(key)

    def contain(self, key):
        if self.__db and len(key) > 0:
            return key in self.__db
        return False

if __name__ == '__main__':
    db = FileDB('/data/test')
    db.set('hello', 'kitty')
    print db.get('hello')
    db.delete('hello')
