import os                                                                       
from multiprocessing import Pool                                                
import sys
import time
from itertools import repeat 

processes=(tuple(repeat('telnetinputget.py', 14)))                                   
                          
def run_process(process):
	rc='python {}'
	os.system(rc.format(process))                                       

os.system('gnome-terminal -- ./startserver.sh')
print ("server")
time.sleep(10)
pool = Pool(processes=14)
pool.map(run_process, processes)    
os.system('./stopserver.sh')
