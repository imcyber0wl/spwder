# spwder
A simple HTML form password bruteforcing tool written in python.
 
------------------------------------------------------------ 
Arguments:
 
url (required)   -   URL to Login page (do not include http://) 
 
-pl (optional)   -   Path to file containing custom passwords (minimum of 20 passwords)
 
-cf (optional)   -   Use custom cookie from file
 
-cc (optional)   -   Use custom cookie  
 
-https (optional) -  Use HTTPs (uses HTTP by defualt)
 
-p (optional)    -   Provide parameters (you should provide username/email with it) Use %26 instead of "&"
 
-hd (optional)   -   Use custom headers from file 
 
-dump (optional) -   Show dumped data 
 
 
------------------------------------------------------------ 
Examples:

Basic: spwder.py url=facebook.com/login 

-pl=C:\Users\you\Desktop\mypasswords.txt 

-cf=C:\Users\you\Desktop\mycookie.txt

-cc=Mycookie124

-https=1    (this enables https)

-p=username=myusername%26other=1234   (notice using %26 instead of &)

-hd=C:\Users\you\Desktop\myheaders.txt 

myheaders.txt should look like this:

header

value 

example: 

User-Agent

Mozilla/5.0 
 
 
 
 
-dump=1    (it takes either 1 or 2, 1 for first response from target, 2 for response from target that indicated a possible correct password) 
 
Important: When trying to bruteforce do not use -dump , only use it after a bruteforce is done. Also use url=x with it to avoid errors. (spwder.py url=whatever -dump=2) 
