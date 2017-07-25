ValKey = "_VALUE"

class Path:
    def __init__(self, arr):
        self.elements = arr 



class Branch:
    def __init__(self, model='', dic={}):
        self.model = model
        self.dic = dic

    def add(self, path, tm, val):
        if len(path) == 0:
            print "empty path"
            return
        
        dic_next = self.dic

        for i , element in enumerate(path):
            if (i < len(path) - 1) :
               if element in dic_next:
                   dic_next = dic_next[element]
               else:
                   dic_next[element] = {}
                   dic_next = dic_next[element]

        if path[-1] in dic_next and type(dic_next[path[-1]]) is list:
            dic_next[path[-1]].append({"timestamp":tm, "value":val})
        else:
            dic_next[path[-1]] = [{"timestamp":tm, "value":val}]

    def get(self, path):
         
         dic_next = self.dic
         for element in path:
             if element in dic_next:
                 dic_next = dic_next[element]
             else:
                 return
         return dic_next
    
    def getAverage(self, path, interval):
        iters = self.get(path)
        sums = 0
        for i in range(interval):
            sums += iters[-1-i]["value"]
        return sums / interval

class PathVal:
    def __init__(self, path, value):
        self.path = path
        self.value = value

