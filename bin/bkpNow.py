#!/usr/bin/python
from subprocess import call

call("./instance run pre_bkp.py",shell=True)
FP = open("tmp","r")
for line in FP.readlines():
    line = line.replace("\n","").split("\t")
    name = line[0]
    filename = line[1]
    file_system_path = line[2]
    filefolder = line[3]
    filefolder_sys = "/".join(file_system_path.split("/")[:-1]) + "/"

    call("./instance run cmed_export.py %s" % name,shell=True)
    folder_exported = "export-" + name

    #Zip folders
    call("zip -r %s %s" % (filename,folder_exported),shell=True)

    #mv zip to apache server folder
    call("mv %s %s" % (filename,filefolder_sys),shell=True)    

    #Delete folders
    call("rm -r %s" % folder_exported,shell=True)

#rm temporary file
call("rm tmp",shell=True)

#Set SELinux Correct settings: fix apache download problem
call("restorecon -v %s/*" % filefolder_sys,shell=True)


