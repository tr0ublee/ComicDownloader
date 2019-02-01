import os
import sqlite3 
import getpass
#WRITTEN BY tr0uble



#------------------------------------------------------------------------------------------
									#MACROS
USER=getpass.getuser()
FIREFOX_COOKIES='/home/'+USER+'/.mozilla/firefox/pei4xq4c.default/cookies.sqlite'
COMMAND1='wget -O /home/'+USER+'/Desktop/RawFiles/' 
COMMAND2=' -U "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0" '
COMMAND3='--header="Accept: text/html" --header="Cookie: __cfduid='
COMMAND4='" -np  '
RAW_PATH="/home/"+USER+"/Desktop/RawFiles/"
COMPILED="/home/"+USER+"/Desktop/Comics/"
LINERS="-----------------------------------------------------------------------------------"
#------------------------------------------------------------------------------------------

def creator():
	os.system("killall firefox")
	if os.system("find ~/Desktop/RawFiles | grep -q ~/Desktop/RawFiles")!=0: 
		print "Creating Directory"
		os.system("mkdir RawFiles")
	os.system("mkdir Comics")

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
	line=line.strip()
	line2=line2.strip()	
	line+=line2
	for i in range(0,len(line)-1):
		result+=line[i]
		if line[i+1]==" "or line[i+1]=="(" or line[i+1]==")" or line[i+1]=="/":
			result+="\\"
	result+=line[len(line)-1]
	return result

def compileComic(title):
	
	os.system("rar -m0 a "+COMPILED+title+".cbr "+RAW_PATH+"*.jpg")
	os.system("rm "+RAW_PATH+"*")
	
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
			os.system("wget -O /home/"+USER+"/Desktop/RawFiles/"+str(count)+".jpg"+" "+line[:-3])
			count+=1 
def __main__():

	print "\nIMPORTANT NOTES : "
	print "1- Use firefox when obtaining the comic links."
	print "2- This script will automatically shut down the firefox. If you have any unsaved work, SAVE IT ! "
	count=0
	links=[]
	title=""
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
	if links==[]: 
		print "You didn't enter any link.Terminating..."
		return 0
	creator()
	for i in links:
		os.system(COMMAND1+'main.html'+COMMAND2+COMMAND3+getCookies()[0]+'; cf_clearance='+getCookies()[1]+COMMAND4+i)
		title=getTitle() 
		getComics()
		compileComic(title)

__main__()
