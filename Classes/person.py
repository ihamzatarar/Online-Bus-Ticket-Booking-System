import os

#---------------------------------------------------- Person Class -----------------------------------------------------------  

class person:
    def __init__(self,id,name,gender,age,DOB):
        self.id = id
        self.name = name 
        self.gender = gender
        self.age = age
        self.DOB = DOB
    def profile(self):
        print('\nName:    ',self.name,'\nId:    ',self.id,'\nGender:    ',self.gender,'\nAge:    ',self.age,'\nDOB:    ',self.DOB)

#---------------------------------------------------- Customer Class -----------------------------------------------------------  
class customer(person):                                                 #Inheritance
    def __init__(self, id, name, gender, age, DOB):
        super().__init__(id, name, gender, age, DOB)
    def profile(self):
        super().print()
    
    
    def verify(username, password):
        with open("./TextFiles/credential.txt", "r") as f:                      #Filling
            info = f.readlines()
            for e in info:
                u, p =e.split(",")
                if u.strip() == username and p.strip() == password:
                    return True
            return False
    
    def register(name,password,confirmpassword,id, gender, age, DOB,phoneNo):
        if name!="" or password!="" or confirmpassword!="" or id!="" or gender!="" or age!="" or DOB!="" or phoneNo!="":
            if password==confirmpassword:
                with open("./TextFiles/credential.txt", "a") as f:                  #Filling
                    f.write(name+","+password+"\n")
                with open("./TextFiles/userInfo.txt", "a") as f:
                    f.write(id+","+name+","+gender+","+age+","+DOB+","+phoneNo+"\n")
                    f.close()
                return True
    
    def contact(self,contact):                                          #Assosiation
        return 'Email: '+contact.email+'\nPhone No:'+contact.phoneNo
                       
#---------------------------------------------------- Admin Class -----------------------------------------------------------  

class admin(person):                                                        #Inheritance
    def __init__(self, id, name, gender, age, DOB, email,phoneNo):
        super().__init__(id, name, gender, age, DOB)
        self.phoneNo = phoneNo
        self.email = email
    def login(name,password):
        with open("./TextFiles/admin.txt", "r") as f:                   #Filling
            for line in f:
                a=line.rstrip('\n').split(',')
                if a[0] == name and a[1] == password:
                    return True
                else:
                    return False
    def addBus(busId,BusNo,maintenanceCost):
        with open("./TextFiles/buses.txt", "a") as f:                   #Filling
            f.write(busId+','+BusNo+','+maintenanceCost+'\n')
            f.close()
    
    def removeBus(busId):
        check = False
        with open("./TextFiles/buses.txt", "r") as input:               #Filling
            with open("temp.txt", "w") as output:
                for line in input:
                    e = line.split(',')
                    if str(e[0]) != busId:
                        output.write(line)
                    else:
                        check = True
        os.replace('temp.txt', './TextFiles/buses.txt')
        return check
    
    def addRoute(routeId,From,To,DepatureTime,ArrivalTime,TravelingTime,TotalDistance,Fare):
        with open("./TextFiles/routes.txt", 'a') as f:                                          #Filling
            f.write(routeId+','+From+','+To+','+DepatureTime+','+ArrivalTime+','+TravelingTime+','+TotalDistance+','+Fare+'\n')
            f.close()
    
    def removeRoute(routeId):
        check = False
        with open("./TextFiles/routes.txt", "r") as input:                  #Filling
            with open("temp.txt", "w") as output:
                for line in input:
                    e = line.split(',')
                    if str(e[0]) != routeId:
                        output.write(line)
                    else:
                        check = True
        os.replace('temp.txt', './TextFiles/routes.txt')
        return check
    
    def addToSchedule(routeId,busId,schedule):                              #Association
        schedule.addToSchedule(routeId,busId)


    def removeFromSchedule(routeId,busId,schedule):                         #Association
        return schedule.removeFromSchedule(routeId,busId)

    def profile(self):
        super().print()
        print('Phone No:    ',self.phoneNo,'\nEmail:    ',self.email)
