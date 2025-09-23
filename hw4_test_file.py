import unittest
from hw4_submission import Traveler, Trip, TravelProvider

class TestAllMethods(unittest.TestCase):

    def setUp(self):
        self.taxi = Trip('Taxi', 25.00)
        self.rideshare = Trip('Rideshare', 40.00)
        self.bus = Trip('Bus', 50.00)
        self.airplane = Trip('Airplane', 100.00)

        self.global_getaways = TravelProvider(name="Global Getaways", provider_id=1)
        self.grand_travels = TravelProvider(name="Grand Travels", provider_id=2)

        self.bob = Traveler(name='Bob', provider_id=None)
        self.alice = Traveler(name='Alice', provider_id=17, credits=125)
        self.charlie = Traveler(name='Charlie', provider_id=1, credits=200)

    # Check the constructors
    def test_traveler_constructor(self):
        self.assertEqual(self.bob.name, 'Bob')
        self.assertEqual(self.bob.credits, 15)
        self.assertEqual(self.bob.provider_id, None)
        self.assertEqual(self.charlie.provider_id, 1)

    def test_trip_constructor(self):
        self.assertEqual(self.taxi.type, 'Taxi')
        self.assertAlmostEqual(self.bus.price, 50.00, 2)
        self.assertEqual(self.airplane.type, 'Airplane')
        self.assertAlmostEqual(self.rideshare.price, 40.00, 2)

    def test_trip_provider_constructor(self):
        self.assertEqual(self.global_getaways.name, "Global Getaways")
        self.assertEqual(self.global_getaways.income, 0)
        self.assertEqual(self.grand_travels.name, "Grand Travels")
        self.assertEqual(self.grand_travels.capacity, {})

    # Check the add_credits method for traveler
    def test_traveler_add_credits(self):
        self.alice.add_credits(100)
        self.assertAlmostEqual(self.alice.credits, 225, 1)

    ### TESTS INVOLVING TRIP PROVIDER CLASS ###
    # Check the calculate_trip_cost for trip provider
    def test_trip_provider_calculate_trip_cost_1(self):
        self.assertAlmostEqual(self.global_getaways.calculate_trip_cost(
            self.bus, 2, False, self.alice), 100.00, 2)
    
    def test_trip_provider_calculate_trip_cost_2(self):
        # Check if discount is applied
        self.assertAlmostEqual(self.grand_travels.calculate_trip_cost(
            self.taxi, 3, False, self.alice), 75, 2)
    
    def test_trip_provider_calculate_trip_cost_3(self):
        # Check if first class requests are billed correctly
        self.assertAlmostEqual(self.grand_travels.calculate_trip_cost(
            self.airplane, 4, True, self.alice), 600.00, 2)
    
    # Check the accept_payment method for trip provider
    def test_trip_provider_accept_payment(self):
        self.grand_travels.accept_payment(500)
        self.assertAlmostEqual(self.grand_travels.income, 500.00, 2)

    # Check the add_duration method for trip provider
    def test_trip_provider_add_seats_1(self):
        self.grand_travels.add_seats(self.taxi, 40)
        self.grand_travels.add_seats(self.rideshare, 20)
        self.assertEqual(self.grand_travels.capacity, {
                         self.taxi: 40, self.rideshare: 20})
    
    def test_trip_provider_add_seats_2(self):
        self.global_getaways.add_seats(self.bus, 30)
        self.global_getaways.add_seats(self.airplane, 50)
        self.assertEqual(self.global_getaways.capacity, {
                         self.bus: 30, self.airplane: 50})
    
    def test_trip_provider_process_trip_request_1(self):
        self.global_getaways.add_seats(self.bus, 30)
        self.global_getaways.add_seats(self.airplane, 50)

        # Scenario 1: trip provider doesn't offer that trip type
        self.assertFalse(self.global_getaways.process_trip_request({
            self.taxi: {
                "num_seats": 1,
                "first_class": False
            }}
        ))
    
    def test_trip_provider_process_trip_request_2(self):
        self.global_getaways.add_seats(self.bus, 30)
        self.global_getaways.add_seats(self.airplane, 50)

        # Scenario 2: The trip actually got processed
        self.global_getaways.process_trip_request({self.bus:{'num_seats': 20, 'first_class': False}})
        self.global_getaways.process_trip_request({self.airplane:{'num_seats': 20, 'first_class': False}})
        
        self.assertEqual(self.global_getaways.capacity, {self.bus: 10, self.airplane: 30})
        
        # Scenario 3: There are not enough seats
        self.assertFalse(
            self.global_getaways.process_trip_request(
            {self.airplane: {'num_seats': 31, 'first_class': False}}
            )
        )
        
    ### END OF TRIP PROVIDER TESTS ###
    
    ### START OF TRAVELER TESTS ###
    def test_traveler_book_trip_1(self):
        pam = Traveler(name='Pam', provider_id=19)
        jetsetter_journeys = TravelProvider(name="Jetsetter Journeys", provider_id=14)

        jetsetter_journeys.add_seats(self.airplane, 10)
        jetsetter_journeys.add_seats(self.taxi, 15)

        # Scenario 1: traveler doesn't have enough credits in their account
        # TODO
    
    # Check the book_trip method for traveler scenario 2
    def test_traveler_book_trip_2(self):
        pam = Traveler(name='Pam', provider_id=19)
        jetsetter_journeys = TravelProvider(name="Jetsetter Journeys", provider_id=14)

        jetsetter_journeys.add_seats(self.airplane, 10)
        jetsetter_journeys.add_seats(self.taxi, 15)

        # Scenario 2: travel provicer doesn't have enough seats left
        # TODO
    
    # Check the book_trip method for traveler
    def test_traveler_book_trip_3(self):
        pam = Traveler(name='Pam', provider_id=19)
        jetsetter_journeys = TravelProvider(name="Jetsetter Journeys", provider_id=14)

        jetsetter_journeys.add_seats(self.airplane, 10)
        jetsetter_journeys.add_seats(self.taxi, 15)

        # Scenario 3: travel provider doesn't offer that trip type
        # TODO
    
    def test_traveler_view_trip_history(self):
        pam = Traveler(name='Pam', provider_id=19)
        jetsetter_journeys = TravelProvider(name="Jetsetter Journeys", provider_id=14)

        jetsetter_journeys.add_seats(self.airplane, 10)
        jetsetter_journeys.add_seats(self.taxi, 17)
        
        #checking multiple trips that pam is making
        pam.add_credits(1000)
        pam.book_trip(jetsetter_journeys, {
            self.taxi: {
                "num_seats": 5,
                "first_class": False
            }}
        )
        pam.book_trip(jetsetter_journeys, {
            self.taxi: {
                "num_seats": 7,
                "first_class": True
            }}
        )
        pam.book_trip(jetsetter_journeys, {
            self.taxi: {
                "num_seats": 5,
                "first_class": False
            }}
        )
        pam.book_trip(jetsetter_journeys, {
            self.taxi: {
                "num_seats": 5,
                "first_class": False
            }}
        )
        pam.book_trip(jetsetter_journeys, {
            self.airplane: {
                "num_seats": 5,
                "first_class": False
            }}
        )
        pam.book_trip(jetsetter_journeys, {
            self.airplane: {
                "num_seats": 5,
                "first_class": True
            }}
        )
        
        self.assertEqual(
            pam.view_trip_history(),
            "Trip history for Pam:\n\n"
            "Trip 1\n"
            "Provider: Jetsetter Journeys\n"
            "Total Cost: 125.0\n"
            "Taxi: (Number of Seats: 5, First Class: No)\n\n"
            "Trip 2\n"
            "Provider: Jetsetter Journeys\n"
            "Total Cost: 262.5\n"
            "Taxi: (Number of Seats: 7, First Class: Yes)\n\n"
            "Trip 3\n"
            "Provider: Jetsetter Journeys\n"
            "Total Cost: 125.0\n"
            "Taxi: (Number of Seats: 5, First Class: No)\n\n"
            "Trip 4\n"
            "Provider: Jetsetter Journeys\n"
            "Total Cost: 500.0\n"
            "Airplane: (Number of Seats: 5, First Class: No)"
        )

    ### END OF TRAVELER TESTS ###


def main():
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
    main()
