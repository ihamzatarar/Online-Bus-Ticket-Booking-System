#---------------------------------------------------- Seat Class -----------------------------------------------------------  

class seat:
    def __init__(self,seatNo,availabilityFlag = 1, occupant = None):
        self.seatNo, self.availabilityFlag, self.occupant = seatNo, availabilityFlag, occupant
    def seatinfo(self):
        print('SeatNo:    ',self.seatNo,'Availability:    ',self.availabilityFlag,'Occupant:    ',self.occupant.name)

#---------------------------------------------------- Route Class -----------------------------------------------------------------------
class route:
    def __init__(self,routeId,source,destination,depatureTime,arrivalTime,travelingTime,distance,fare):                 #change
        self.routeId, self.source, self.destination, self.depatureTime, self.arrivalTime = routeId, source,destination,depatureTime,arrivalTime
        self.travelingTime, self.distance, self.fare = travelingTime, distance , fare 
    def routeInfo(self):
        print('route Id:    ',self.routeId,'\nFrom:    ',self.source,'\nTo:    ',self.destination,'\nDepature Time:    ',self.depatureTime,\
            '\nArrival Time:    ',self.arrivalTime,'\nTraveling Time:    ',\
                self.travelingTime,'\nTotal Distance:    ',self.distance,'\nFare:    ',self.fare)

#---------------------------------------------------- Bus Class -----------------------------------------------------------  

class bus:
    def __init__(self,busId,busNo,maintenanceCost):
        self.busId, self.busNo ,self.maintaincost = busId, busNo, maintenanceCost,
        self.seats = {}
        #self.staff = [staff]
        self.route = None
        self.Type = None                                                #Polymorphism
        for i in range(1,31):                                           
            self.seats[str(i)] = seat(i)                                #Composition
    def setRoute(self,route):
        self.route = route
    def delRoute(self):
        self.route = None
    def busInfo(self):
        print('Bus Id:    ',self.busId,'\nBus No:    ',self.busNo)

#---------------------------------------------------- EconomyClass -----------------------------------------------------------  
class economyClass(bus):                                                #Inheritance
    features = 'Ac-bus'
    def __init__(self, busId, busNo, maintenanceCost):                  
        super().__init__(busId, busNo, maintenanceCost)
        self.Type = 'Economy Class'
        
#---------------------------------------------------- BussinessClass -----------------------------------------------------------  

class businessClass(bus):                                               #Inheritance
    features = 'Ac-bus wifi free lunch'
    additionalFare = 500                                       
    def __init__(self, busId, busNo, maintenanceCost):                  
        super().__init__(busId, busNo, maintenanceCost)
        self.Type = 'Business Class'