import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pathtree.pathtree as pathtree

def TestAdd():

    path = pathtree.Path(["interfaces","interface1","BGP","state"])
    path2 = pathtree.Path(["newinterfaces","interface1","CGP","state"])
    path3 = pathtree.Path(["interfaces"])

    branch = pathtree.Branch({})
    branch.add(path, 2)
    print branch.dic
    branch.add(path, 3)
    print branch.dic
    branch.add(path, 5)
    print branch.dic
    branch.add(path2, 6) 
    print branch.dic
    print branch.get(path)
    print branch.get(path3)
    

if __name__ == '__main__':
    TestAdd()

