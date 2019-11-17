class Pixels():
    def __init__(self,data):
       self.data = data
    def __getitem__(self, key):
        self.__check_key__(key)
        return (self.data[key*3],self.data[key*3+1],self.data[key*3+2])
    def __setitem__(self, key, value):
        self.__check_key__(key)
        self.data[key*3] = value[0]
        self.data[key*3+1] = value[1]
        self.data[key*3+2] = value[2]
    def __len__(self):
        return len(self.data)/3
    def __check_key__(self,key):
        if not isinstance(key,int):
            raise TypeError('A.a must be an int')
        if key >= len(self.data)/3 or key < 0:
            raise IndexError("out of bounds")
    def show():
        pass

arr = Pixels([0]*(3*10))
arr[1] = [128,64,32]
print(arr[9])
print(arr.data)
