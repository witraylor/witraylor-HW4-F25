# SI 201 HW4
# Your name: Willow Traylor
# Your student id: 67975434
# Your email: wtraylor@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.  
# e.g.: 
# Asked Chatgpt hints for debugging and suggesting the general sturcture of the code

# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

import unittest


class Traveler:
    def __init__(self, name, provider_id=None, credits=15):
        '''
        ARGUMENTS: 
            self: the current object

            name: a string representing a traveler's name

            provider_id: integer representing ID of the travel provider the traveler works for (default = None)

            credits: integer showing how many credits the traveler currently has

            trip_history: a list of dictionaries which stores a traveler’s history of trip requests successfully booked 

        
        RETURNS: None
        '''
        self.name = name
        self.provider_id = provider_id
        self.credits = credits
        self.trip_history = []


    def __str__(self):
        '''
        ARGUMENTS: 
            self: the current object

        RETURNS: a string
        '''
        return f'My name is {self.name}, and I have {self.credits} credits in my account'


    def add_credits(self, credits):
        '''
        ARGUMENTS: 
            self: the current object

            credits: an integer showing how many credits to add to the traveler's account
            
        RETURNS: a float
        '''
        self.credits += credits


    def book_trip(self, travel_provider_obj, trip_request):
        for trip, info in trip_request.items():
            num_seats = info["num_seats"]
            first_class = info["first_class"]
        
        cost = travel_provider_obj.calculate_trip_cost(trip, num_seats, first_class, self)

        if self.credits < cost:
            return False
        
        if travel_provider_obj.process_trip_request(trip_request) == False:
            return False
        
        self.credits -= cost
        travel_provider_obj.accept_payment(cost)
        self.trip_history.append({
            "provider": travel_provider_obj.name,
            "trip": trip,
            "num_seats": num_seats,
            "first_class": first_class,
            "cost": cost
        })
        return True
        '''
        ARGUMENTS: 
            self: the current Traveler object

            travel_provider_obj: the TravelProvider object through which we are booking the trip 

            trip_request: a nested dictionary -> KEYS - Trip objects; VALUES - another dictionary with keys of num_seats (Integer) and first_class (Boolean)

        RETURNS: a Boolean value (True or False)
        '''
    
    def view_trip_history(self):
        if self.trip_history == []:
            print(f"{self.name} has no trips booked yet.")
        
        output = [f"Trip history for {self.name}:"]
        i = 1    
        for trip in self.trip_history:
            provider = trip["provider"]
            trip_type = trip["trip"].type
            num_seats = trip["num_seats"]
            first_class = "Yes" if trip["first_class"] else "No"
            cost = trip["cost"]

            output.append(
            f"Trip {i}\n"
            f"Provider: {provider}\n"
            f"Total Cost: {cost}\n"
            f"{trip_type}: (Number of Seats: {num_seats}, First Class: {first_class})"
            )
            i += 1
        return "\n\n".join(output)
        '''
        ARGUMENTS:
            self: the current Traveler object

        RETURNS: None

        '''



class Trip:
    def __init__(self, type, price):
        ''' 
        ARGUMENTS: 
            self: the current object

            name: a string representing the type of the trip that can be booked

            price: a float representing the price per seat of a trip type

        RETURNS: None
        '''
        self.type = type
        self.price = price

    def __str__(self):
        ''' 
        ARGUMENTS: 
            self: the current object

        RETURNS: a string
        '''
        return f"{self.type} costs ${self.price} per seat"


class TravelProvider:
    def __init__(self, name, provider_id, income=0):
        ''' 
        ARGUMENTS: 
            self: the current object

            name: a string representing the name of the trip

            provider_id: an integer representing the ID of the travel provider (used for travelers who are also employees to track who they work for)

            income: a float representing the income the travel provider has collected

            capacity: a dictionary which holds the Trip objects as the keys 
            and the available number of seats for that trip type from this travel provider as the value

        RETURNS: None
        '''
        self.name = name
        self.provider_id = provider_id
        self.income = income
        self.capacity = {}

    
    def __str__(self):
        '''
        ARGUMENTS: 
            self: the current object

        RETURNS: a string
        '''
        return f"Hello we are {self.name}. This is our current income: {self.income}"

    
    def accept_payment(self, amount):
        '''
        ARGUMENTS: 
            self: the current object

            amount: total cost of a trip request (as a float) added to the travel provider's income

        RETURNS: a float
        '''
        self.income += amount

    
    def calculate_trip_cost(self, trip_obj, num_seats, first_class, traveler_obj):
        cost = trip_obj.price * num_seats

        if first_class:
            cost *= 1.5
        
        if traveler_obj.provider_id == self.provider_id:
            cost *= .8
        
        return cost
        '''
        ARGUMENTS: 
            self: the current object

            trip_obj: Trip object

            num_seats: number of seats (requested from trip)

            first_class: Boolean variable specifying if a first class trip request was made

            traveler_obj: Traveler object (the traveler who made a request)

        RETURNS: a float

        ***If a first class request is made, a 50% surcharge is added.***

        EXTRA CREDIT: If the traveler works for the travel provider, then they receive a 20% discount on the trip. They also still pay the 50% surcharge for first class requests before the discount is applied.
        '''

    def add_seats(self, trip_obj, num_seats):
        if trip_obj not in self.capacity:
            self.capacity[trip_obj] = num_seats
        else:
            self.capacity[trip_obj] += num_seats
        
        return None
        ''' 
        ARGUMENTS: 
            self: the current object

            trip_obj: Trip object

            num_seats: number of seats (requested from trip)
        
        RETURNS: None
        '''


    def process_trip_request(self, trip_request):
        for trip, info in trip_request.items():
            if trip not in self.capacity or info["num_seats"] > self.capacity[trip]:
                return False
        
        for trip, info in trip_request.items():
            self.capacity[trip] -= info["num_seats"]
            
        return True     
        
        '''
        ARGUMENTS: 
            self: the current object

            trip_request: a nested dictionary -> KEYS: Trip objects; VALUES: another dictionary with keys of num_seats and first_class

        RETURNS: a Boolean value (True or False)
        '''

