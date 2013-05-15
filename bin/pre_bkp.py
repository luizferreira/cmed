import random
from datetime import datetime
import time
import os
import string
import shutil
import tempfile
import transaction
from Products.CMFCore.utils import getToolByName
from subprocess import call


#============Defines=============
#Apache server folder backup path
bkp_folder = "/var/www/html/"



#===========Main==================
if __name__ == '__main__':
    
    #Create new folder based on today date POSIX_time + readible_time
    new_folder_name = str(time.time()) +"-"+ datetime.today().strftime("%d-%m-%Y")
    new_folder_path = bkp_folder+new_folder_name 
    call("mkdir %s" % (new_folder_path),shell=True)
    call("touch %s/index.html" % (new_folder_path), shell=True) #create index.html file to disable browser listing


    app_items = app.items()

    filetmp = open("tmp","w")

    for app_item in app_items:
        (name, item_obj) = app_item
        if str(item_obj).startswith('<PloneSite at '):
            plone_site = item_obj
            bkp_filename = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(20)]) + ".zip"
            bkp_file_path_sys = new_folder_path + "/" + bkp_filename
            
            bkp_file_path = new_folder_name + "/" + bkp_filename

            #Save file name in vocab
            vt = getToolByName(plone_site, 'vocabulary_tool')
            vt.add_vocab('cmed_backup',bkp_file_path)
            transaction.commit()

            print >> filetmp, "\t".join([name,bkp_filename,bkp_file_path_sys,new_folder_name])

    #Close File
    filetmp.close()

    
    

