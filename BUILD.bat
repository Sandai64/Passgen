@ECHO OFF

python cxfreeze -OO -c --include-modules=string,os,sys,random,time,io,secrets,base64,decimal,colorama,termcolor passgen.py

pause
