
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
        
print "Welcome to The Library"
print
while True:
    print "1.System Update"
    print "2.Library Functions"
    print "3.Exit"
    print
    ch=input("Select your choice : ")
    print
    import Inventory
    if ch==1:
        p=raw_input("Please Enter The password : ")
        print
        if p == "17":
            while True:
                print
                print
                print "1.Register New Books"
                print "2.Remove Books"
                print "3.Member Registration"
                print "4.Display Library Members"
                print "5.Display Library Members in a Specific Class"
                print "6.Deleting a Member"
                print "7.Read And Remove Enquiries/Complaints"
                print "8.Restock books"
                print "9.Exit"
                print
                print
                ch=input("Select your choice : ")
                print
                print
                if ch==1:
                    Inventory.addbooks()
                elif ch==2:
                    Inventory.delbooks()
                elif ch==3:
                    Inventory.registerstudents()
                elif ch==4:
                    Inventory.displays()
                elif ch==5:
                    Inventory.displaysc()
                elif ch==6:
                    Inventory.deletestudents()
                elif ch==7:
                    Inventory.reade()
                elif ch==8:
                    Inventory.replenish()
                else:
                    break
        else:
            
            print "Wrong Password, Entry Denied."
            print
            pass    
    elif ch==2:
        while True:
            print
            print
            print "1.Display books"
            print "2.Issue A Book"
            print "3.Return A Book"
            print "4.View your book log"
            print "5.Equiries/Complaints"
            print "6.Lost books"
            print "7.Exit"
            print
            print
            ch=input("Select your choice : ")
            print
            print
            if ch==1:
                Inventory.displayb()
            elif ch==2:
                Inventory.issueb()
            elif ch==3:
                Inventory.returnb()
            elif ch==4:
                Inventory.viewlog1()
            elif ch==5:
                Inventory.enco()
            elif ch==6:
                Inventory.lostb()
            else:
                break
    else:
        break

