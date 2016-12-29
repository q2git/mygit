########################################################################################
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:19:20 2016

"""

import random
import xlwings as xw
from tkfactory import TkFactory

class Gui(TkFactory):
    def __init__(self,filename):
        super(Gui, self).__init__(filename)
        self.show_hide(int(self.widgets['subcnts'].get()))
        self.widgets['run'].config(command=self.cmd)
        self.widgets['subcnts'].bind('<FocusOut>', self.show_hide)
        
    def cmd(self):
        mainsheet = self.textvariables.get('mainsheet').get()
        subcnts = int(self.textvariables.get('subcnts').get())
        sheets = [( 
                    self.textvariables['l{}'.format(i)].get(),
                    self.textvariables.get('{}s'.format(i)).get(),
                    int(self.textvariables.get('{}n'.format(i)).get())
                   ) for i in range(1,subcnts+1)]
        choose_subject(mainsheet,*sheets) 
    
    def show_hide(self,event=None):
        num = int(self.widgets['subcnts'].get())
        num = num if num<10 else 10
        for i in range(1,10):
            if i>num:
                self.widgets['l{}'.format(i)].grid_remove()
                self.widgets['{}s'.format(i)].grid_remove()
                self.widgets['{}n'.format(i)].grid_remove()
            else:
                self.widgets['l{}'.format(i)].grid()
                self.widgets['{}s'.format(i)].grid()
                self.widgets['{}n'.format(i)].grid()               
            

def choose_subject(sht, *sheets):
    xw.sheets[sht].activate()
    row_main = 5
    xw.sheets[sht].range((row_main,1),(200,1)).clear_contents()    
    for label, sheet, num in sheets:
        count = xw.sheets[sheet].range((1,1)).end('down').row
        num = num if num<count else count
        sample = random.sample(range(1,count+1), num)
        xw.sheets[sht].range((row_main,1)).value = label+sheet
        xw.sheets[sht].range((row_main+1,1)).expand().value = \
            map(lambda (row,i): [str(i)+'.  '+xw.sheets[sheet].range((row,1)).value],
                         zip(sample,range(1,len(sample)+1))
                         )
        row_main = row_main + num + 2
   
def main():
    #wb = xw.Book('optest.xlsx')
    gui = Gui('gui.ini') 
    gui.run()
            
            
if __name__ == '__main__':

    main()
    
    
########################################Call From Excel#####################################################    
    
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 08:54:54 2015

"""
import os
import sys
from xlwings import Workbook, Range, Sheet, RgbColor

ShtNames = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',
            7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
def main():
    wb = Workbook.caller()
    count = Range(1,'A1').table.last_cell.row + 1
    for rid in range(3,count):
        if Range(1,(rid,1)).color == (192,192,192): continue
        rgv = get_rgv(1,rid)
        #if arg and arg != rgv[2].month:continue
        data = calc(rgv[2],rgv[3],rgv[6])
        #print i,data
        if data:
            Sheet(data["sht"]).activate()
            for i in range(1,data["rowcnt"]):
                if rgv[0] == Range(data["sht"],(i,1)).value:
                    Range(data["sht"],(i,rgv[2].day+3)).value = data["value"]
                    break
            else:
                Range(data["sht"],(data["rowcnt"],1)).value = [ rgv[0], rgv[1], rgv[4]]
                Range(data["sht"],(data["rowcnt"],rgv[2].day+3)).value = data["value"]
            Range(1,(rid,1)).color = (192,192,192)
        else:
            Range(1,(rid,1)).color = RgbColor.rgbYellow
    Sheet(1).activate()
    
def get_rgv(shtname,rowid):
    rgv = Range(shtname,(rowid,1),(rowid,4)).value
    rgv = rgv + Range(shtname,(rowid,18),(rowid,20)).value
    rgv[0] = int(rgv[0])
    return rgv
    
def calc(begin,end,hrs):
    data = {}
    data["sht"] = ShtNames[begin.month]
    data["rowcnt"] = Range(data["sht"],'A1').table.last_cell.row + 1
    if begin == end:
        data["value"] = hrs
        return data
    elif begin.month == end.month:
        days = end.day - begin.day + 1
        if days <= 0: return None
        data["value"] = []
        weekday = begin.weekday()
        for i in range(days):
            if weekday in [5,6]:
                data["value"].append(None)
                days = days - 1
            else:
                data["value"].append(hrs)
            weekday = weekday+1 if weekday<6 else 0
            #print weekday,
        for i,d in enumerate(data["value"]):
            if d != None:
                data["value"][i] = d/days
        return data
    return None
 
    
    
if __name__ == '__main__':
    if not hasattr(sys, 'frozen'):
        # The next two lines are here to run the example from Python
        # Ignore them when called in the frozen/standalone version
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'template.xls'))
        Workbook.set_mock_caller(path)
    #arg = input('Please input month:')
    main()
