from __future__ import print_function
from wpexception import *
import json


CFG_WP = {"ROOT":{"WP1 ":{"1Distance":1234,"1Altitude":1234,"1Angle":1234},\
                  "WP2 ":{"2Distance":1234,"2Altitude":1234,"2Angle":1234},\
                  "WP3 ":{"3Distance":1234,"3Altitude":1234,"3Angle":1234}}}

LEAF_NODE = 'leafnode'

class sctrlp_wpcfg(object):
    def __init__(self):
        super(sctrlp_wpcfg, self).__init__()
        self.root = sctrlp_wp_node("ROOT")
        self.root.set_father(None)
        self.root.set_brother(None)
        self.cur_node = self.root
        self.__loadwpdict()
        self.__create_tree__(self.root, self.__wpcfg['ROOT'])
        
    def __create_tree__(self,node,sonvalue):
        sonlst = [] 
        if isinstance(sonvalue, dict):
            sortedlst = sorted(sonvalue.keys(),key=lambda item:item[2],reverse = False) 
            print(sortedlst)         
            for i in range(len(sonvalue)):
                sonlst.append(sctrlp_wp_node(sortedlst[i]))
            for j in range(len(sonlst)):
                print(len(sonlst))              
                if j==0:
                    node.set_son(sonlst[j])
                    print("%s's son is %s"%(node.name(),sonlst[j].name()))
                sonlst[j].set_father(node)
                print("%s's father is %s"%(sonlst[j].name(),node.name()))
                sonlst[j].set_brother(sonlst[(j+1)%len(sonlst)])
                print("%s's brother is %s"%(sonlst[j].name(),sonlst[(j+1)%len(sonlst)].name()))
                self.__create_tree__(sonlst[j],sonvalue[sortedlst[j]])
        else:
            node.set_son(sctrlp_wp_node(LEAF_NODE))
            node.son().set_value(sonvalue)
            node.son().set_father(node)
            node.son().set_son(None)
            node.son().set_brother(None)
            print("%s's value is %s"%(node.name(),node.son().value()))
    def go2father(self):
        if self.cur_node.father().name() != 'ROOT':
            self.cur_node = self.cur_node.father()
    def go2son(self):
        if self.cur_node.son() != None:
            self.cur_node = self.cur_node.son()
    def go2brother(self):
        if self.cur_node.brother() != None:
            self.cur_node = self.cur_node.brother()
    def go2root(self):
        self.cur_node = self.root
    def curnode(self):
        return self.cur_node 
    def isleafnode(self):
        return self.cur_node.name() == LEAF_NODE
    def __tree2dict__(self):
        pass
    def dumpwpcfg(self):
        print(json.dumps(CFG_WP))
        #json.dumps(self.root, default = self.__tree2dict__)
    def loadwpcfg(self):
        pass
    def __loadwpdict(self):
        f = open('d:\\json.txt','r')
        self.__wpcfg = json.load(f)
        print(self.__wpcfg)
     
class sctrlp_wp_node(object):
    def __init__(self,name):
        super(sctrlp_wp_node, self).__init__()
        self.__name = name
    def set_father(self,father):
        self.__father = father
    def set_brother(self,brother):
        self.__brother = brother
    def set_son(self,son):
        self.__son = son
    def set_value(self,value):
        self.__value = value
    def father(self):
        return self.__father
    def brother(self):
        return self.__brother
    def son(self):
        return self.__son
    def value(self):
        return self.__value
    def name(self):
        return self.__name
    