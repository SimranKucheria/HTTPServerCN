#Build-in Modules imported
import pickle
import os

#Creation of Student Directory
class studic:
    def __init__(self):
        self.rollno=input("Enter your Library Roll No : ")
        self.name=raw_input("Enter name : ")
        self.classe=raw_input("Enter class : ")
        self.books=[]
        print
    def modifys(self,a,b,c,d):
        self.rollno=a
        self.name=b
        self.classe=c
        self.books=d
        return self
    def __str__(self):
        return str(self.rollno) + " : " + self.name + " : " + self.classe + " : " + str(self.books)
    def __del__(self):
        print
#Creation of Book Directory
class bookdic:
    def __init__(self):
        self.bcode=input("Enter the Bookcode : ")
        self.bname=raw_input("Enter the Bookname : ")
        self.author=raw_input("Enter the name of the author : ")
        self.price=input("Enter the price : ")
        self.count=input("Enter the count : ")
        print
    def modifyb(self,a,b,c,d,e):
        self.bcode=a
        self.bname=b
        self.author=c
        self.price=d
        self.count=e
        return self
    def __str__(self):
        return str(self.bcode) + " : " + self.bname + " : " + self.author + " : " + str(self.price) + " : " + str(self.count)
    def __del__(self):
        print 
        
#Temperory Creator Code (Students)
'''sd1=open("Studic.dat","wb")
n=input("Enter number of students : ")
for i in range (n):
    sd=studic()
    pickle.dump(sd,sd1)
sd1.close()'''


#Temperory Creator Code (Books)
'''d1=open("Books.dat","wb")
n=input("Enter number of books : ")
print
for i in range (n):
    d=bookdic()
    pickle.dump(d,d1)
d1.close()'''

#Temperory Enquiry Complaint Box Creator
'''cd=open("Enquiry.txt","w")
cd.close()'''

#Print Check Statement
'''sd1=open("Studic.dat","rb")
d1=open("Books.dat","rb")
n=raw_input("Enter the Inventory Code : ")
print
try:
    while True:
        if n=="s":
            o=pickle.load(sd1)
            print o
        else:
            ob=pickle.load(d1)
            print ob
except EOFError:
    sd1.close()
    d1.close()
print'''

#Registration Students
def registerstudents():
    print "Note: ENSURE TO USE AN UNEXSISTING Library Roll No.."
    print
    sd1=open("Studic.dat","ab")
    n=input("Enter number of Members : ")
    ch="n"
    for i in range (n):
        sd=studic()
        pickle.dump(sd,sd1)
        ch="y"
        print "Please confirm that the Member details are correct. If not approach Technincal Assistance Staff."
        print
        print sd
    sd1.close()
    print
    print "You have succesfully registered into The Library"
    print "Verify The Registration of the Member."
    displays()
    print
    print "Thank You"
        
#Deleting Students
def deletestudents():
    sd1=open("Studic.dat","rb")
    sd2=open("Temp.dat","wb")
    rn=input("Enter your Library Roll No : ")
    ch='n'
    try:
        while True:
            e=pickle.load(sd1)
            if e.rollno==rn and e.books==[]:
                print "Please confirm that the Member details are correct. If not approach Technincal Assistance Staff."
                print "Member Details"
                print e
                t=e
                del t
                ch='y'
                pass
            else:
                pickle.dump(e,sd2)
    except EOFError:
        sd1.close()
        sd2.close()
    os.remove("Studic.dat")
    os.rename("Temp.dat","Studic.dat")
    if ch=="n":
        print
        print "Your Elimination was detected to be unsuccesfull.Please ensure that you have returned all the issued books."
        print
        while True:
            print "1. Return book"
            print "2.Lost Book"
            print "3.Delete member (After removing all books)"
            print "4.Exit"
            print
            ch=input("Enter your choice : ")
            if ch==1:
                returnb()                
            elif ch==2:
                lostb()
            elif ch==3:
                sd1=open("Studic.dat","rb")
                sd2=open("Temp.dat","wb")
                try:
                    while True:
                        e=pickle.load(sd1)
                        if e.rollno==rn and e.books==[]:
                            print "Please confirm that the Member details are correct. If not approach Technincal Assistance Staff."
                            print "Member Details"
                            print e
                            t=e
                            del t
                            ch='y'
                            pass
                        else:
                            pickle.dump(e,sd2)
                except EOFError:
                    sd1.close()
                    sd2.close()
                os.remove("Studic.dat")
                os.rename("Temp.dat","Studic.dat")
            else:
                break
    else:
        print
        print "You have succesfully Eliminated your Member from The Library"
        print "Thank You"

#Adding Books
def addbooks():
    print "Note: ENSURE TO USE AN UNEXSISTING BOOKCODE."
    print
    d1=open("Books.dat","ab")
    n=input("Enter number of books : ")
    for i in range (n):
        d=bookdic()
        pickle.dump(d,d1)
        print
        print "Please confirm that the book details are correct. If not approach Technincal Assistance Staff."
        print "Book Details"
        print d
    d1.close()
    print
    print "You have succesfully added your book into the Inventory"
    print "Verify The Registration of the Book."
    displayb()
    print
    print "Thank You"
    
#Deleting Books
def delbooks():
    d1=open("Books.dat","rb")
    d2=open("Temp1.dat","wb")
    bc=input("Enter the Book Code : ")
    ch='n'
    try:
        while True:
            b = pickle.load(d1)
            if b.bcode==bc:
                print
                print "Please confirm that this the correct book that has been requested for elimination. Else approach Technincal Assistance Staff"
                print "Book Details"
                print b
                t=b
                ch='y'
            else:
                pickle.dump(b,d2)
        del t
    except EOFError:
        d1.close()
        d2.close()
    os.remove("Books.dat")
    os.rename("Temp1.dat","Books.dat")
    if ch=='n':
        print
        print "Your Elimination was detected to be unsuccesfull."
        print"Book Not Found. Contact Technical Assistance Staff"
    else:
        print
        print "You have succesfully removed your book from the Inventory"
        print "Verify The Removal of the Book."
        displayb()
        print
        print "Thank You"

#Issuing Books
def issueb():
    d1=open("Books.dat",'rb')
    d2=open("Temp2.dat","wb")
    sd1=open("Studic.dat",'rb')
    sd2=open("Temp3.dat","wb")
    rn=input("Enter your Library Roll No : ")
    bc=input("Enter book code : ")
    ch=0
    try:
        while True:
            e=pickle.load(d1)
            if bc==e.bcode and e.count!=0:
                print "Confirm the Details : "
                print "Book details"
                print e
                t=e.count-1
                y=e.modifyb(e.bcode,e.bname,e.author,e.price,t)
                pickle.dump(y,d2)
                try:
                    while True:
                        f=pickle.load(sd1)
                        if rn==f.rollno:
                            print "Student details"
                            print f
                            l=f.books
                            l.append(bc)
                            x=f.modifys(f.rollno,f.name,f.classe,l)
                            pickle.dump(x,sd2)
                            ch=1
                            print
                            print "Book Issued successfully"
                            print "Student details"
                            print x
                            print "Book details"
                            print y
                        else:
                            pickle.dump(f,sd2)
                except EOFError:
                    sd1.close()
                    sd2.close()
                    os.remove("Studic.dat")
                    os.rename("Temp3.dat","Studic.dat")
            else:
                pickle.dump(e,d2)
    except EOFError:
        d1.close()
        d2.close()
    os.remove("Books.dat")
    os.rename("Temp2.dat","Books.dat")
    if ch==0:
        print
        print "Sorry Book not available"                

#Returning Books
def returnb():
    d1=open("Books.dat",'rb')
    d2=open("Temp4.dat","wb")
    sd1=open("Studic.dat",'rb')
    sd2=open("Temp5.dat","wb")
    rn=input("Enter your Library Roll No : ")
    bc=input("Enter book code : ")
    ch=0
    try:
        while True:
            e=pickle.load(d1)
            if bc==e.bcode:
                print "Confirm the Deatils : "
                print "Book Details"
                print e
                t=e.count+1
                y=e.modifyb(e.bcode,e.bname,e.author,e.price,t)
                pickle.dump(y,d2)
                try:
                    while True:
                        f=pickle.load(sd1)
                        if rn==f.rollno:
                            print "Student Details"
                            print f
                            l=f.books
                            l.remove(bc)
                            x=f.modifys(f.rollno,f.name,f.classe,l)
                            print
                            print "Book returned successfully"
                            print "Student Details"
                            print x
                            print "Book Details"
                            print y
                            pickle.dump(x,sd2)
                            ch=1
                        else:
                            pickle.dump(f,sd2)
                except EOFError:
                    sd1.close()
                    sd2.close()
                    os.remove("Studic.dat")
                    os.rename("Temp5.dat","Studic.dat")
            else:
                pickle.dump(e,d2)
    except EOFError:
        d1.close()
        d2.close()
    os.remove("Books.dat")
    os.rename("Temp4.dat","Books.dat")         
    if ch==0:
        print
        print "Error"


#Book Display Table
def displayb():
    print
    print
    print "Book Log"
    print "-"*90;
    print "Book Code","  ",
    t=["Name","Author","Price","Count"]
    for i in t:
        if i==t[0] or i==t[1]:
            r=18-len(i)    
        else:
            r=5-len(i)
        print i," "*r,
    print
    print "_"*90
    d1=open("Books.dat","rb")
    try:
        while True:
            b=pickle.load(d1)
            print " ",b.bcode,"      ",
            t1=["Name","Author","Price","Count"]
            for y in t1:              
                if y==t1[0]:
                    v=18-len( b.bname)
                    print b.bname," "*v,
                elif y==t[1]:
                    v=18-len(b.author)
                    print b.author," "*v,
                elif y==t[2]:
                    v=5-len(str(b.price))
                    print b.price," "*v,
                else:
                    v=5-len(str(b.count))
                    print" ", b.count," "*v,
            print
            print "_"*90
    except EOFError:
        d1.close()
    
    print
    print
                     
#Student Display Table**********
def displays():
    sd1=open("Studic.dat","rb")
    print
    print "_"*90
    print"Student Details"
    print "_"*90
    print
    print "G.R.No","  ",
    t=["Name","Class","Books"]
    for i in t:
        if i==t[0] or i==t[2]:
            r=18-len(i)    
        else:
            r=8-len(i)
        print i," "*r,
    print
    print "_"*90
    try:
        while True:
            s=pickle.load(sd1)
            print " ",s.rollno,"     ",
            t=["Name","Class","Books"]
            for y in t:
                if y==t[0]:
                    print s.name,
                    v=(18-len(s.name))
                    print " "*(v),
                elif y==t[1]:
                    print s.classe,
                    v=(8-len(s.classe))
                    print " "*(v),
                elif y==t[2]:
                    print s.books,
                    v=(18-len(s.books))
                    print " "*(v)
            print 
            print "_"*90
    except EOFError:
        sd1.close()
    print
    print
    

#View your books
    
def viewlog1():
    k=input("Enter your Library Roll No: ")
    sd1=open("Studic.dat","rb")
    print
    print
    print "Book Log"
    print "-"*90;
    print "Book Code","  ",
    t=["Name","Author","Price","Count"]
    for i in t:
        if i==t[0] or i==t[1]:
            r=18-len(i)    
        else:
            r=5-len(i)
        print i," "*r,
    print
    print "_"*90
    d=open("Books.dat","rb")
    try:
        while True:
            s=pickle.load(sd1)
            if k==s.rollno:
                l=s.books
                z=s.name
                try:
                    while True:
                        b=pickle.load(d)
                        for i in l:
                            if i==b.bcode:
                                print " ",b.bcode,"      ",
                                t1=["Name","Author","Price","Count"]
                                for y in t1:
                                    if y==t1[0]:
                                        v=18-len( b.bname)
                                        print b.bname," "*v,
                                    elif y==t[1]:
                                        v=18-len(b.author)
                                        print b.author," "*v,
                                    elif y==t[2]:
                                        v=5-len(str(b.price))
                                        print b.price," "*v,
                                    else:
                                        v=5-len(str(b.count))
                                        print" ", b.count," "*v,
                                print
                                print "_"*90
                except EOFError:
                    d.close()                  
    except EOFError:
        sd1.close()
    print "Name : " , z
    print
        
#Entering Enquiry
def enco():
    cd=open("Enquiry.txt","a")
    q=input("Enter your Library Roll No : ")
    c=raw_input("Enter your Enquiry/Complaint : ")
    cd.write(str(q)+" "+c+"\n")
    cd.close()
    print "Thank You"
    
#Reading and Removing Enquiry/Complaint
def reade():
    cd=open("Enquiry.txt","r")
    t=open("Temp6.txt","w")
    c=cd.readline()
    while c:
        print c
        print
        print "a.Consider Enquiry "
        print "b.Exit"
        print
        r=raw_input("Enter Choice : ")
        if r=="a":
            pass
        else:
            t.write(c)
        c=cd.readline()
    cd.close()
    t.close()
    os.remove("Enquiry.txt")
    os.rename("Temp6.txt","Enquiry.txt")

#Lost Books
def lostb():
        d1=open("Books.dat",'rb')
        d2=open("Temp4.dat","wb")
        sd1=open("Studic.dat",'rb')
        sd2=open("Temp5.dat","wb")
        rn=input("Enter your Library Roll No : ")
        bc=input("Enter book code : ")
        ch=0
        try:
            while True:
                e=pickle.load(d1)
                if bc==e.bcode:
                    t=e.count-1
                    m=e.price
                    y=e.modifyb(e.bcode,e.bname,e.author,e.price,t)
                    print "Confirm the Details : "
                    print "Book Details"
                    print y
                    pickle.dump(y,d2)
                    try:
                        while True:
                            f=pickle.load(sd1)
                            if rn==f.rollno:
                                print "Student Details"
                                print f
                                l=f.books
                                l.remove(bc)
                                x=f.modifys(f.rollno,f.name,f.classe,l)
                                print
                                print"Change Reflected"
                                print"Student Details"
                                print x
                                print "Book Details"
                                print y
                                pickle.dump(x,sd2)
                                ch=1
                            else:
                                pickle.dump(f,sd2)
                    except EOFError:
                        sd1.close()
                        sd2.close()
                        os.remove("Studic.dat")
                        os.rename("Temp5.dat","Studic.dat")
                else:
                    pickle.dump(e,d2)
        except EOFError:
            d1.close()
            d2.close()
        os.remove("Books.dat")
        os.rename("Temp4.dat","Books.dat")         
        if ch==1:
            print
            print "Your library due is",m
        else:
            print
            print "An Unexplained error occured. Contact Technical Assistance"

#Replenish book stock
def replenish():
    d1=open("Books.dat",'rb')
    d2=open("Temp4.dat","wb")
    bc=input("Enter book code : ")
    n=input("Enter number of books to add : ")
    try:
        while True:
            e=pickle.load(d1)
            if bc==e.bcode:
                print "Confirm the Details : "
                print "Book Details"
                print e
                t=e.count+n
                y=e.modifyb(e.bcode,e.bname,e.author,e.price,t)
                pickle.dump(y,d2)
                print
                print "Book restocked successfully"
                print y
            else:
                pickle.dump(e,d2)
    except EOFError:
        d1.close()
        d2.close()
    os.remove("Books.dat")
    os.rename("Temp4.dat","Books.dat")

#Student Display Table Classwise**********
def displaysc():
    c=raw_input("Enter  The Class : ")
    sd1=open("Studic.dat","rb")
    print
    print "_"*90
    print"Student Details"
    print "_"*90
    print
    print "G.R.No","  ",
    t=["Name","Class","Books"]
    for i in t:
        if i==t[0] or i==t[2]:
            r=18-len(i)    
        else:
            r=8-len(i)
        print i," "*r,
    print
    print "_"*90
    try:
        while True:
            s=pickle.load(sd1)
            t=["Name","Class","Books"]
            if s.classe==c:
                print " ",s.rollno,"     ",
                for y in t:
                    if y==t[0]:
                        print s.name,
                        v=(18-len(s.name))
                        print " "*(v),
                    elif y==t[1]:
                        print s.classe,
                        v=(8-len(s.classe))
                        print " "*(v),
                    elif y==t[2]:
                        print s.books,
                        v=(18-len(s.books))
                        print " "*(v)
                print
                print "_"*90
    except EOFError:
        sd1.close()
    print
    print
    

                


    

    
   
        


    
    
    
    


    
