import os
class schedule:
    def __init__(self):
        self.schedule = {}
        
    def add(self,bus,route):                                                #Aggregation
        if route not in self.schedule:
                self.schedule[route]= [bus]
        else:
            self.schedule[route].append(bus)
                
    
    def remove(self,bus,route):                                              #Aggregation
        for i in self.schedule:
            if i == route:
                self.schedule[i].remove(bus)

    def addToSchedule(self,routeId,busId):                                      
        with open("./TextFiles/routes-buses.txt", "a") as f:                    #Filling
            f.write(routeId+','+busId+'\n')
            f.close()



    def removeFromSchedule(self,routeId,busId):                                   
        check = False
        with open("./TextFiles/routes-buses.txt", "r") as input:                    #Filling
            with open("temp.txt", "w") as output:
                for line in input:
                    e = line.split(',')
                    if str(e[0]) != routeId:
                        output.write(line)
                    else:
                        check = True
        os.replace('temp.txt', './TextFiles/routes-buses.txt')
        return check

class contactUs:
    def __init__(self,email,phoneNo):
        self.email = email
        self.phoneNo = phoneNo