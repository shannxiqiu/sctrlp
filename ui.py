from __future__ import print_function
import Tkinter as tk
import tkMessageBox
import tkFont
import wpdata
from wpexception import *

class sctrlp_ui(object):
    "layout the ui"
    count = 0;
    editable = False
    def __init__(self):
        super(sctrlp_ui, self).__init__()
        self.pwon= False   
        self.top = tk.Tk()
        self.strbtpw = tk.StringVar(value="off")
        self.itms_tree = wpdata.sctrlp_wpcfg()
        self.edit_pos_cur = 0
        self.itms_tree.loadwpcfg()
        
    def __top__(self):   
        self.top.title('sctrlp')
        self.top.geometry('320x300+600+200')
         
    def __btok_callback__(self):  
        if self.__power_check__():
            self.itms_tree.go2son()
            if not self.itms_tree.isleafnode():            
                self.__showitems__(True)
            else:
                if self.editable:
                    self.itms_tree.go2father()
                    self.__showitems__(True)
                    self.__set_item_uneditable__()   
                    self.edit_pos_cur = 0
                else:
                    self.__showitems__(False)
                    
    def __keyback_callback__(self):
        if self.__power_check__():
            if not self.editable:
                self.itms_tree.go2father()
                self.__showitems__(True)
            else:
                lcd_lst = (self.lcd0, self.lcd1,self.lcd2, self.lcd3)
                self.edit_pos_cur = (self.edit_pos_cur+1)%len(lcd_lst)    
                                           
    def __keynumx_callback__(self):
        if self.__power_check__():
            self.itms_tree.go2brother()
            if self.itms_tree.curnode().brother() != None: 
                self.__showitems__(True)
            elif self.editable:
                nlst = [int(self.canvaslcd.itemcget(self.lcd0, 'text')),\
                          int(self.canvaslcd.itemcget(self.lcd1, 'text')),\
                          int(self.canvaslcd.itemcget(self.lcd2, 'text')),\
                          int(self.canvaslcd.itemcget(self.lcd3, 'text'))]
                nlst[self.edit_pos_cur] = (nlst[self.edit_pos_cur]+1)%10
                self.itms_tree.curnode().set_value(nlst[3]*1000+nlst[2]*100+nlst[1]*10+nlst[0])
                print('value is %d'%(self.itms_tree.curnode().value()))
                self.__showitems__(False)
                                                
    def __keys__(self):
        self.lbkeys = tk.LabelFrame(self.top,text='keys')
        self.lbkeys.grid(row=1,column=1)

        self.btnumx = tk.Button(self.lbkeys,text='num+',cursor='hand1',width=5,height=2,\
                              command = self.__keynumx_callback__,repeatdelay = 100, repeatinterval = 100)
        self.btnumx.grid(column=2, row=2,padx=5)

        self.btback = tk.Button(self.lbkeys,text='back',cursor='hand1',width=5,height=2,\
                               command = self.__keyback_callback__)
        self.btback.grid(column=0, row=2,padx=5)

        self.btok = tk.Button(self.lbkeys,text='ok',cursor='hand1',width=5,height=2,\
                              command = self.__btok_callback__)
        self.btok.grid(column=1, row=2,pady=30)  

    def __btpw_callback__(self):
        if  self.pwon:
            self.strbtpw.set('off')
            self.pwon = False
            self.itms_tree.go2root()
            self.__showitems__(True)
        else:
            self.strbtpw.set('on')
            self.pwon = True
            self.itms_tree.go2son()
            self.__showitems__(True)
            
    def __power__(self):                 
        self.lbpw = tk.LabelFrame(self.top,text='power')
        self.lbpw.grid(row=0,column=0,sticky=tk.W,padx=10)
        
        self.btpw = tk.Button(self.lbpw,textvariable=self.strbtpw,command=self.__btpw_callback__, \
                             cursor='hand1',width=6,height=1,state=tk.DISABLED)
        self.btpw.grid(padx=5,pady=5)
        self.btpw['state'] = tk.NORMAL
                      
    def __btmod_callback__(self):  
        if self.__power_check__() and self.itms_tree.isleafnode(): 
            if self.count==3 and not self.editable:
                self.count=0            
                print("edit switch on")
                self.__set_item_editable__()
            else:
                self.count = (self.count+1)%4  
                 
    def __btdump_callback__(self):
        self.itms_tree.dumpwpcfg()
                
    def __mode__(self):
        self.lbmod = tk.LabelFrame(self.top,text='modify')
        self.lbmod.grid(row=1,column=0)
        
        self.btmod = tk.Button(self.lbmod,text='mod',cursor='hand1',width=6,height=1,\
                               command=self.__btmod_callback__, repeatdelay = 1000, repeatinterval = 500)
        self.btmod.grid(row=0,column=0,padx=5,pady=5)
        
        self.btdump = tk.Button(self.lbmod,text='dump',cursor='hand1',width=6,height=1,
                                command=self.__btdump_callback__)
        self.btdump.grid(row=1,column=0,padx=5,pady=5)
            
    def __lcd__(self):
        self.canvaslcd = tk.Canvas(self.top,width=200,height =50)
        self.canvaslcd.create_rectangle(0,0,50,50)
        self.canvaslcd.create_rectangle(50,0,100,50)
        self.canvaslcd.create_rectangle(50,0,150,50)
        self.canvaslcd.create_rectangle(50,0,200,50)

        tmp_font = tkFont.Font(family="time", size=30, underline=0) 
        self.lcd3 = self.canvaslcd.create_text(25,30,width=30,text='',font=tmp_font)
        self.lcd2 = self.canvaslcd.create_text(75,30,width=30,text='',font=tmp_font)
        self.lcd1 = self.canvaslcd.create_text(125,30,width=30,text='',font=tmp_font)
        self.lcd0 = self.canvaslcd.create_text(175,30,width=30,text='',font=tmp_font)
        self.canvaslcd.grid(row=0,column=1,pady=30)
        
    def draw(self): 
        self.__top__()
        self.__keys__()
        self.__mode__()
        self.__power__()  
        self.__lcd__() 
        self.top.mainloop()
     
    def __power_check__(self):
        try:
            if not self.pwon:
                raise wp_excption("power on first")
            else:
                return True    
        except wp_excption,err:
            tkMessageBox.showwarning('warning',err.errmsg)
            return False 
           
    def __set_item_editable__(self):  
        #tmpfont = self.canvaslcd.itemcget(self.lcd0, 'font') 
        #print(type(tmpfont)) 
        #print(tmpfont)
        lcd_lst = (self.lcd0, self.lcd1,self.lcd2, self.lcd3)
        tmp_font = tkFont.Font(family="time", size=30, underline=1)
        for i in range(len(lcd_lst)):
            self.canvaslcd.itemconfigure(lcd_lst[i], font=tmp_font)
        self.editable =True 
    
    def __set_item_uneditable__(self):     
        lcd_lst = (self.lcd0, self.lcd1,self.lcd2, self.lcd3)
        tmp_font = tkFont.Font(family="time", size=30, underline=0)
        for i in range(len(lcd_lst)):
            self.canvaslcd.itemconfigure(lcd_lst[i], font=tmp_font)
        self.editable =False 

    def __showitems__(self, bName): 
        lcd_lst = (self.lcd0, self.lcd1,self.lcd2, self.lcd3)  
        if bName:
            for i in range(len(lcd_lst)):
                self.canvaslcd.itemconfigure(lcd_lst[i],text = self.itms_tree.curnode().name()[(len(lcd_lst)-1)-i])
        else:       
            tmp = self.itms_tree.curnode().value()
            for j in range(len(lcd_lst)):
                self.canvaslcd.itemconfigure(lcd_lst[j],text = tmp%10)
                tmp //=10 
        

        