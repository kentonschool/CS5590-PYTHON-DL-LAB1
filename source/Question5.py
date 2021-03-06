'''
DOCUMENTATION:

To use the manager fully, run the program and enter commands in the shell.

Please note that many methods in the classes should ONLY be called by BookingManager

Neither Person nor ThingOnPlane should ever be instantiated. They do not function with the BookingManger.

===
To use the manager:

First, instantiate BookingManager. ( b = BookingManager() )
This will automatically create some flights when it is instantiated

First, check b.printAllFlights() to see what flights are available
You can then assign a flight to an instance of Passenger (p) by calling:
b.bookFlight(p,b.flights[<flightnum>]
You can cancel a flight for a passenger in the same way.

You can create a flight for the BookingManager by first instantiating a flight.
Ideally the data types for flight are:

flightnum = int
start = str
destination = str
takeoffdatetime = str
plane = Plane
(A plane simply takes a name for whatever model you want. This can be a string or anything else.)
baseprice = int

but these are not checked and are not required.

Then call: b.createFlights(<flight>) (you can pass a list of flights if you want to)

Other functions should be fairly self explanatory

===
To instantiate a Passenger:
A name and age are required, but a list of luggage and a location are optional.
Location is only present to show inheritance from ThingOnPlane

the luggage list should be a list consisting ONLY of class Luggage.
A Luggage is only used for calculating prices for flights and
is just instantiated with a name for the luggage to keep track of it.
Location is optional and is only present to show inheritance from ThingOnPlane
'''



class Plane:
    def __init__(self,model):
        self.model = model
    def __str__(self):
        return self.model

class Flight:
    def __init__(self,flightnum,start,destination,takeoffdatetime,plane,baseprice):
        self.flightnum=flightnum
        self.start=start
        self.destination=destination
        self.time = takeoffdatetime
        self.plane=plane
        self.__passengers=[] #private data member (we don't want everyone knowing who is on what flight)
        self.baseprice = baseprice

    def __str__(self):
        return "flight {0} on a {1} from {2} to {3} at {4}.\n {5} passengers booked so far. Base price: ${6}".format(self.flightnum,self.plane,self.start,self.destination,self.time,self.getNumPassengers(),self.baseprice)

    def assignPassenger(self,passenger):
        self.__passengers.append(passenger)

    def removePassenger(self,passenger):
        '''
        Removes a passenger from a flight if they are on the flight
        '''
        try:
            self.__passengers.remove(passenger)
        except:
            print("This passenger isn't on this flight.")

    def getNumPassengers(self):
        return len(self.__passengers)

    
class BookingManager:
    
    def __init__(self):
        self.flights = dict()
        plane1 = Plane("Boeing 747")
        plane2 = Plane("Cessna")
        plane3 = Plane("Boeing 787")

        flight1 = Flight(123,"MCI","LAX","2/13/19 3:00PM",plane1,400)
        flight2 = Flight(233,"MCI","JFK","2/14/19 7:00AM",plane2,120)
        flight3 = Flight(314,"LAX","MCI","2/14/19 9:30PM",plane3,1000)
        self.createFlights(flight1,flight2,flight3)
        

    def bookFlight(self,passenger,flight):
        flight.assignPassenger(passenger)
        passenger.assignFlight(flight)

    def cancelFlight(self,passenger,flight):
        flight.removePassenger(passenger)
        passenger.cancelFlight()

    def deleteFlight(self,flight):
        if flight in self.flights.values():
            del self.flights[flight.flightnum]

    def createFlights(self, *flights):
        for flight in flights:
            self.flights[flight.flightnum] = flight

    def printAllFlights(self):
        for flight in self.flights.values():
            print(flight)
        

class Person: #base class never instantiated
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __str__(self):
        return "{0} is {1} years old".format(self.name,self.age)
        

class ThingOnPlane: #base class never instantiated
    def __init__(self,location):
        self.location = location

    def getLocation(self):
        return self.location

class Luggage(ThingOnPlane):
    def __init__(self,name,location="at home"):
        super().__init__(location)
        self.thing = name
    
class Passenger(Person,ThingOnPlane):
    def __init__(self,name,age,luggageList=[],location="at home"):
        #if location is in the arguments, assign it, else, default to "at home"
        self.location = location
        super().__init__(name,age)
        self.flight = 0
        self.flighthistory = []
        self.luggageList = luggageList
        self.needToPay = 0

    def printFlightHistory(self):
        for flight in self.flighthistory:
            print(flight)
   
    def assignFlight(self,flight):
        self.flight = flight
        self.needToPay = flight.baseprice + (30*len(self.luggageList))
        self.flighthistory.append(flight)
        print(self.name,"needs to pay $",self.needToPay)

    def cancelFlight(self):
        self.flight = 0
        self.needToPay = 0
        
def testClasses():   
    #test booking manager
    b = BookingManager()
    print("===Instantiate passenger with luggage===")
    laptop = Luggage("laptop")
    kenton = Passenger("kenton",22,[laptop])
    print(kenton)
    print("===print all flights available===")
    b.printAllFlights()
    print("===book flight 123 for kenton===")
    b.bookFlight(kenton,b.flights[123])
    print("==see that the flights have been updated (123 has one passenger now)===")
    b.printAllFlights()
    print("===kenton's flights have also been updated===")
    print(kenton.flight)
    print("===make a new plane and create a new flight===")
    newPlane = Plane("new model")
    newFlight = Flight(555,"HND","MCI","2/16/2019 10:00PM",newPlane,750)
    b.createFlights(newFlight)
    b.printAllFlights()
    print("===book that new flight for kenton and show all the flights again===")
    b.bookFlight(kenton,b.flights[555])
    b.printAllFlights()
    print("===cancel the 123 flight for kenton and show how the flights update===")
    b.cancelFlight(kenton,b.flights[123])
    b.printAllFlights()
    print("===delete the flight 123 and print the flights again===")
    b.deleteFlight(b.flights[123])
    b.printAllFlights()

    #instantiate all classes even if they aren't supposed to be and can't be used
    print("===now we instantiate a Person and a ThingOnPlane===")
    print("===the following classes should not be instantiated since the booking manager needs===\n===a passenger to book flights and a thing doesn't do anything===")
    newPerson = Person("Test",101)
    print(newPerson)
    newThing = ThingOnPlane("somewhere")
    print(newThing.getLocation())



inp = input("Enter y to test all of the classes or you can also read the start of Question5.py to run the manager in full yourself").lower()
if inp == 'y':
    testClasses()
