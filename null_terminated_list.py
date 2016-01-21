
class null_terminated_list:
    def __init__(self,datatype,num_elements):
        self.datatype = datatype
        self.num_elements = num_elements
        self.data = [datatype()]*num_elements
        self.null_stop = 0
    
    def add(self,e):
#        if type(e) != type(self.datatype()):
#            raise TypeError("Expecting datatype "+str(self.datatype)+", received datatype "+str(type(e)))
#        if self.null_stop >= self.num_elements:
#            raise IndexError("This null terminated list is full, length="+str(self.num_elements))
#        if sys.getsizeof(self.data[self.null_stop]) != sys.getsizeof(e):
#            raise Error("This shit. the datatype size: "+str(sys.getsizeof(self.data[self.null_stop]))+", the element size: " + str(sys.getsizeof(e)))
        self.data[self.null_stop] = e
        self.null_stop += 1
    
    def extend(self,l):
#        if type(l) == type(list()):
#            for e in l:
#                self.add(e)
#        elif type(l) == type(null_terminated_list(self.datatype, self.num_elements)):
        for e in l.get():
            self.add(e)
#        else:
#            raise TypeError("did not understand input content type - should be list or null_terminated_list")
    
    def get(self):
        return self.data[:self.null_stop]
    
    def length(self):
        return self.null_stop
    
    def reset(self):
        self.__init__(self.datatype,self.num_elements)

    def remove(self,e):
        self.data.remove(e)
        self.null_stop -= 1