import os
import sqlite3 
import getpass
from time import sleep
# @author : tr0uble



#------------------------------------------------------------------------------------------
									#MACROS

USER=getpass.getuser()
FIREFOX_COOKIES='/home/'+USER+'/.mozilla/firefox/'
DEFAULT_FOLD=os.listdir(FIREFOX_COOKIES)
for i in DEFAULT_FOLD:
	if type(i)==str and "def" in i:
		FIREFOX_COOKIES+=i+"/cookies.sqlite"
		break
print "COOKIES ",FIREFOX_COOKIES
COMMAND1='wget -q -O /home/'+USER+'/Desktop/RawFiles/' 
# Change COMMAND2 with your own user agent.
# You can use https://www.whatismybrowser.com/detect/what-is-my-user-agent
COMMAND2=' -U "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0" ' 
COMMAND3='--header="Accept: text/html" --header="Cookie: __cfduid='
COMMAND4='" -np  '
RAW_PATH="/home/"+USER+"/Desktop/RawFiles/"
COMPILED="/home/"+USER+"/Desktop/Comics/"
LINERS="-----------------------------------------------------------------------------------"
#------------------------------------------------------------------------------------------

def readInput():
	links=[]
	while True:
		count=0
		print "\n"
		print "Keep pasting the links of the comics you want to download"
		print "Type q to start downloading"
		print "Type 1 to print the list"
		print "Type 2 to delete from the list"
		print "\n"
		url=raw_input()
		if url=="Q" or url=='q':
			return links
			break
		elif url=="1" :
			print LINERS
			print "Your List:"
			for i in links : print i
			print LINERS
		elif url=="2" : 
			print "\n"
			for i in links  : 
				print " "+str(count)+" - "+i
				count+=1
			print "Enter the index of the link you want to remove (Starts FROM 0 ! )"
			print "press q to exit"
			i=raw_input()
			
			if i=="q" or i=="Q":
				continue
			else:
				links.pop(int(i))
		else:
			if url not in links: 
				links.append(url)
			else : print "Already in the list. Skipping...\n"
def makeChoice():
	print "\nIMPORTANT NOTES : "
	print "****Use firefox when obtaining the comic links."
	print "****This script will automatically shut down the firefox. If you have any unsaved work, SAVE IT ! "
	count=0
	title=""
	decision=0
	while True:
		print "Would you like to download all comics of an URL or specific ones ? "
		print "1-All Comics"
		print "2-Specific Ones"
		decision=raw_input()
		if decision=="1" or decision=="2":
			return decision
		else :
			print "Wrong input.Try Again.\n"
def creator():
	os.system("killall firefox")
	if os.system("find ~/Desktop/RawFiles | grep -q ~/Desktop/RawFiles")!=0: 
		print "Creating Directory"
		os.system("mkdir ~/Desktop/RawFiles")
	os.system("mkdir ~/Desktop/Comics")

def getCookies():
	cookies=[] #[__cfduid,cf_clearance]
	cookieTable=sqlite3.connect(FIREFOX_COOKIES)
	rows=cookieTable.cursor()
	rows.execute("SELECT baseDomain, name, value FROM moz_cookies WHERE name='__cfduid' and baseDomain='readcomiconline.to';")	
	for row in rows:
		cookies.append(row[2])
	rows.execute("SELECT baseDomain, name, value FROM moz_cookies WHERE name='cf_clearance' and baseDomain='readcomiconline.to';")
	for row in rows : 
		cookies.append(row[2])
		break
	return cookies
	
def getTitle():
	file=open("/home/"+USER+"/Desktop/RawFiles/main.html", "rw+")
	result=""
	line=""
	line2=""
	for line in file : 
		if line.find('<head><title>')==0:
			line=file.next()
			line=file.next()
			line2=file.next()
			break
	print "line ",line
	line=line.strip()
	line2=line2.strip()	
	line+=line2
	for i in range(0,len(line)-1):
		result+=line[i]
		if line[i+1]==" "or line[i+1]=="(" or line[i+1]==")" or line[i+1]=="/":
			result+="\\"
	print "RESULT ",result
	result+=line[len(line)-1]
	return result

def compileComic(title):
	
	os.system("rar -m0 a "+COMPILED+title+".cbr "+RAW_PATH+"*.jpg")
	
def getComics():
	file=open("/home/"+USER+"/Desktop/RawFiles/main.html", "rw+")
	href=""
	previous=""
	count=1
	for line in file : 
		
		if ("lstImages.push") in line : 
			index=line.index("push")
			line=line[index+6:]
			line=line.strip()
			line=line.replace("s1600","s0")
			os.system("wget -q -O /home/"+USER+"/Desktop/RawFiles/"+str(count)+".jpg"+" "+line[:-3])
			count+=1 

def getLinks(string): #For whole issues
	lock=0
	link=""
	for i in string:
		if lock==1 and i==" ":
			break
		elif lock==0 and i=="=" :
			lock=1
		elif lock==1:
			link+=i

	return link
def readFile(): # For whole issues
	result=[]
	file=open("/home/"+USER+"/Desktop/RawFiles/main1.html", "rw+")
	lock=0
	for i in file :
		if lock==1 and "</table>" in i :

			return result

		elif lock==1:
			if "href=" in i :
				result.append("https://readcomiconline.to"+getLinks(i))

		elif lock==0 and '<table class="listing">' in i :
			lock=1 


def __main__():
	decision=makeChoice()
	links=readInput()
	if links==[]: 
		print "You didn't enter any link.Terminating..."
		return 0
	creator()
	cf_clearance,cfduid=getCookies()[1],getCookies()[0]
	for i in links:
		if decision=="2": #Specific issues
			print "Downloading index"
			#DEBUG
			print COMMAND1+'main.html'+COMMAND2+COMMAND3+cfduid+'; cf_clearance='+cf_clearance+COMMAND4+i
			#--
			os.system(COMMAND1+'main.html'+COMMAND2+COMMAND3+cfduid+'; cf_clearance='+cf_clearance+COMMAND4+i)
			title=getTitle()
			print "Downloading "+title
			getComics()
			compileComic(title)
		else: #whole issues
			print "Downloading index"
			os.system(COMMAND1+'main1.html'+COMMAND2+COMMAND3+cfduid+'; cf_clearance='+cf_clearance+COMMAND4+i)
			readFile()
			wholeLinks=readFile()

			if wholeLinks==[] : 
				break
			wholeLinks.reverse()
			for j in wholeLinks:
				print "Downloading index"
				os.system(COMMAND1+'main.html'+COMMAND2+COMMAND3+cfduid+'; cf_clearance='+cf_clearance+COMMAND4+j)
				title=getTitle()
				print "Downloading "+title
				getComics()
				compileComic(title)
				os.system("find "+RAW_PATH+" ! -name 'main1.html' -type f -exec rm -f {} +")
			os.system("rm "+RAW_PATH+"*")
	os.system("rm "+RAW_PATH+"*")



__main__()

