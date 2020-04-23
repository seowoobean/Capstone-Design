class Set:
    def __init__(self, value = []):    # Constructor
        self.data = []                 # Manages a list
        self.concat(value)

    def intersection(self, other):        # other is any sequence
        res = []                       # self is the subject
        for x in self.data:
            if x in other:             # Pick common items
                res.append(x)
        return Set(res)                # Return a new Set

    def union(self, other):            # other is any sequence
        res = self.data[:]             # Copy of my list
        for x in other:                # Add items in other
            if not x in res:
                res.append(x)
        return Set(res)

    def concat(self, value):
        for x in value:                
            if not x in self.data:     # Removes duplicates
                self.data.append(x)

    def __len__(self):          return len(self.data)        # len(self)
    def __getitem__(self, key): return self.data[key]        # self[i], self[i:j]
    def __and__(self, other):   return self.intersection(other) # self & other
    def __or__(self, other):    return self.union(other)     # self | other
    def __repr__(self):         return 'Set({})'.format(repr(self.data))  
    def __iter__(self):         return iter(self.data)       # for x in self:
    def __le__(self, other):    return self.union(other).data == other.data
    def __lt__(self, other):    
        return (self | other).data == other.data and (self&other).data != other.data
    def issubset(self, other):  return self<=other
    def __ge__(self, other):    return self.union(other).data == self.data
    def __gt__(self, other):    
        return (self | other).data == self.data and (self&other).data != self.data
    def issuperset(self, other):  return self>=other
    def __ior__(self,other):    return self|other
    def __iand__(self,other):    return self&other
    def __isub__(self,other):
        return Set([j for j in self.data if j not in other])
    def __ixor__(self,other):
        return Set([j for j in self|other.data if j not in self&other])
    def add(self,elem): 
        self.data.append(elem)
    def remove(self,elem):
        self.data.remove(elem)
    def intersection_update(self,other):
        self.data = (self&other).data
    def difference_update(self,other):
        self.data = Set([j for j in self.data if j not in other]).data
    def symmetric_difference_update(self,other):
        self.data = Set([j for j in self|other.data if j not in self&other]).data

x = Set([1,3,5,7, 1, 3])
y = Set([2,1,4,5,6])
print(x, y, len(x))
print(x.intersection(y), y.union(x))
print(x & y, x | y)
print(x[2], y[:2])
for element in x:
    print(element, end=' ')
print()
print(3 not in y)  # membership test
print(list(x))   # convert to list because x is iterable
#subset test
print(x.issubset(Set([1,3,5,7,9])))
print(x<=Set([1,3,5,7]))
print(x<Set([1,3,5,7]))
print(x<Set([1,3,5,7,9]))
#superset test
print(x.issuperset(Set([1,3])))
print(x>=Set([1,3,5,7]))
print(x>=Set([1,3,5]))
print(x>Set([1,3,5,7]))
print(x>Set([1,3,5]))
#ior test
x |= y
print(x)
#iand test
x &= y
print(x)
x.intersection_update(Set([1,2,4]))
print(x)
#isub test
x -= Set([1])
print(x)
x.difference_update(x)
print(x)
#ixor test
x = y
print(x)
x ^= Set([1,4,7,8])
print(x)
x.symmetric_difference_update(Set([1,2,5]))
print(x)
#add remove test
x.add(10)
x.remove(1)
print(x)