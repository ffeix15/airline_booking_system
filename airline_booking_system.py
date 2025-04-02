#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:00:40 2025

@author: caoxufei
"""

import random
import string

class SeatBookingSystem:
    def __init__(self, rows=80, cols="ABCXDEF"):
        self.rows = rows  # Total number of rows in the seating plan
        self.cols = cols  # Column labels (A, B, C, X, D, E, F)
        self.seats = self._create_seats_table()  # Initialize the seats dictionary
        # Create a dictionary to store booking details instead of a database
        self.bookings = {}  # Key is the booking reference, value is a dictionary with customer info

    def _create_seats_table(self):
        seats = {}
        for row in range(1, self.rows + 1):  # Iterate through rows 1 to 80
            for col in self.cols:  # Iterate through columns A, B, C, X, D, E, F
                seat_id = f"{row}{col}"  # Create seat ID like "1A"
                if col == "X":
                    seats[seat_id] = "X"  # Mark as aisle (unbookable)
                elif self.rows - 4 <= row <= self.rows - 2 and col in ["D", "E", "F"]:
                    seats[seat_id] = "S"  # Mark as storage in rows 77-79, cols D-F
                else:
                    seats[seat_id] = "F"  # Mark as free (available for booking)
        return seats

    # New function to generate a random 8-character booking reference
    def generate_booking_ref(self):
        # Use uppercase letters (A-Z) and numbers (0-9) to make the reference
        characters = string.ascii_uppercase + string.digits
        while True:  # Keep trying until we get a unique reference
            # Pick 8 random characters and join them into a string
            booking_ref = ''.join(random.choice(characters) for _ in range(8))
            # Check if this reference is already used in our bookings dictionary
            if booking_ref not in self.bookings:
                return booking_ref  # If it’s not used, return it as the new reference

    def check_availability(self, row, col):
        seat_id = f"{row}{col}"  # Construct seat ID
        # Verify that row and column are within the valid range of the seat layout
        if (1 <= row <= self.rows and col in self.cols):
            seat = self.seats[seat_id]  # Get the current status of the specified seat
            # If the seat is marked F, it’s available for booking
            if seat == "F":
                print(f"Seat {seat_id} is available")
            # If the seat is marked X or S, it can’t be booked
            elif seat in ["X", "S"]:
                print(f"Seat {seat_id} cannot be booked (aisle or storage)")
            # If it’s not F, X, or S, it must be a booking reference, so it’s reserved
            else:
                print(f"Seat {seat_id} is reserved")
        # Handle invalid row or column inputs
        else:
            print("Invalid row or column number")

    def book_seat(self, row, col):
        seat_id = f"{row}{col}"  # Construct seat ID
        # Confirm the row and column are within the layout boundaries
        if (1 <= row <= self.rows and col in self.cols):
            # Check if the seat is free (F) and can be booked
            if self.seats[seat_id] == "F":
                # Ask the user for customer details to store with the booking
                passport = input("Enter passport number: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                # Generate a unique 8-character booking reference
                booking_ref = self.generate_booking_ref()
                # Store the booking reference in the seats dictionary instead of "R"
                self.seats[seat_id] = booking_ref
                # Save the customer details in the bookings dictionary using the reference as the key
                self.bookings[booking_ref] = {
                    "passport": passport,    
                    "first_name": first_name,  
                    "last_name": last_name,    
                    "seat_row": row,          
                    "seat_col": col          
                }
                print(f"Seat {seat_id} booked with reference {booking_ref}")
            # If the seat is an aisle (X) or storage (S), booking is not allowed
            elif self.seats[seat_id] in ["X", "S"]:
                print("Cannot book an aisle or storage area")
            # If the seat is already reserved, inform the user
            else:
                print("Seat is already reserved")
        # Notify the user if the row or column is invalid
        else:
            print("Row or column number is invalid")

    def free_seat(self, row, col):
        seat_id = f"{row}{col}"  # Construct seat ID
        # Ensure the row and column are within the valid range
        if (1 <= row <= self.rows and col in self.cols):
            # If the seat is reserved (not F, X, or S), it has a booking reference
            if self.seats[seat_id] not in ["F", "X", "S"]:
                # Get the booking reference from the seat
                booking_ref = self.seats[seat_id]
                # Remove the customer details from the bookings dictionary
                del self.bookings[booking_ref]
                # Change the seat status back to free (F)
                self.seats[seat_id] = "F"
                print(f"Seat {seat_id} has been released")
            # If the seat is an aisle (X) or storage (S), no action is needed
            elif self.seats[seat_id] in ["X", "S"]:
                print("Aisle or storage area cannot be released")
            # If the seat is already free (F), no change is required
            else:
                print("Seat is not reserved")
        # Alert the user if the row or column is out of range
        else:
            print("Invalid row or column number")

    def show_status(self):
        # Print a title to indicate the seat layout is being shown
        print("Current Seat Status:")
        for row in range(1, self.rows + 1):  # Loop through each row in the layout
            # Create a list of statuses for the current row and display it
            row_status = [self.seats[f"{row}{col}"] for col in self.cols]
            print(f"Row {row}: {' '.join(row_status)}")  # Use spaces for clarity

    def count_available_seats(self):
        # Calculate the total number of free seats (F) across all seats
        count = sum(1 for status in self.seats.values() if status == "F")
        # Display the result to the user
        print(f"Total number of available seats: {count}")

def main():
    # Create an instance of the SeatBookingSystem
    booking_system = SeatBookingSystem()
    
    while True:  # Main loop to keep menu active until exit
        # Display the available menu options to the user
        print("\nSeat Booking System Menu:")
        print("1. Check seat availability")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit program")
        print("6. Show total available seats")
        
        # Get the user’s choice from the menu
        choice = input("Select an option (1-6): ")
        
        if choice == "1":  # Option 1: Check availability of a seat
            # Prompt for row and column (no adjustment needed for 1-based indexing)
            row = int(input("Enter row number (1-80): "))
            col = input("Enter column letter (A-F, X): ").upper()
            booking_system.check_availability(row, col)  # Execute the availability check
        
        elif choice == "2":  # Option 2: Book a seat
            row = int(input("Enter row number (1-80): "))
            col = input("Enter column letter (A-F, X): ").upper()
            booking_system.book_seat(row, col)  # Attempt to book the specified seat
        
        elif choice == "3":  # Option 3: Release a seat
            row = int(input("Enter row number (1-80): "))
            col = input("Enter column letter (A-F, X): ").upper()
            booking_system.free_seat(row, col)  # Release the specified seat if possible
        
        elif choice == "4":  # Option 4: Display the seat layout
            booking_system.show_status()  # Show the current state of all seats
        
        elif choice == "5":  # Option 5: Exit the program
            print("Program terminated")
            break  # End the loop and stop the program
            
        elif choice == "6":  # Option 6: Show total available seats
            booking_system.count_available_seats()  # Call function to count and display free seats
        
        # Handle cases where the input isn’t a valid option
        else:
            print("Option not recognized, please select 1-6")

if __name__ == "__main__":
    main()