from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
import mysql.connector
import os

app = Flask(__name__,template_folder='templates')
app.secret_key = os.urandom(24)
# Database connection setup
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="12qwaszxQ@#",
    database="app"
)
db_cursor = db_connection.cursor(dictionary=True)

# Helper function for executing SQL queries
def execute_query(query, data=None, fetchone=False):
    try:
        with db_connection.cursor(dictionary=True) as cursor:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)

            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()

    except Exception as e:
        print(f"Error in execute_query: {str(e)}")
        raise  # Propagate the exception for better debugging

@app.route('/')
def home():
    return render_template('home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials against the database
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        data = (username, password)
        result = execute_query(query, data, fetchone=True)

        if result:
            session['username'] = username
            return redirect(url_for('admin_dashboard.html'))

    return render_template('login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home.html'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session:
        return render_template('admin_dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/worker_information')
def worker_information():
    # Fetch worker information from the database
    query = "SELECT * FROM worker_information"
    worker_data = execute_query(query)
    return render_template('worker_details.html', worker_data=worker_data)

@app.route('/customer_information', methods=['GET', 'POST'])
def customer_information():
    if request.method == 'POST':
        # Process the form submission
        name = request.form['name']
        contact = request.form['contact']
        block = request.form['selected_block']
        vehicle_type = request.form['vehicle_type']
        license_plate = request.form['license_plate']
        parking_space = request.form['selected_parking_space']

        # Check if the parking space is vacant
        query_vacant = "SELECT * FROM parking_slot WHERE SlotID = %s AND Status = 'Vacant'"
        data_vacant = (parking_space,)
        result_vacant = execute_query(query_vacant, data_vacant, fetchone=True)

        if result_vacant:
            # Generate a ticket
            ticket_details = generate_ticket(name, parking_space)

            # Update the parking slot status to 'Occupied'
            query_update = "UPDATE parking_slot SET Status = 'Occupied' WHERE SlotID = %s"
            data_update = (parking_space,)
            execute_query(query_update, data_update)

            # Display the ticket immediately
            return render_template('ticket_display.html', parking_space=parking_space, is_occupied=result_vacant, ticket_details=ticket_details)

        else:
            print("Parking space is already occupied.")
            return render_template('booking_failure.html', message='Parking space is already occupied.')

    # Fetch customer information from the database
    query_customer_info = "SELECT * FROM customer_information"
    customer_data = execute_query(query_customer_info)

    # Render the 'customer_form.html' template with customer data
    return render_template('customer_form.html', customer_data=customer_data)

@app.route('/parking_slots', methods=['GET', 'POST'])
def parking_slots():
    if request.method == 'POST':
        parking_space = request.form['parking_space']

        # Update: Extract the floor and block from the parking_space
        floor, block = parking_space[0], parking_space[1]

        # Update: Set the selected_block and vehicle_type based on the block
        selected_block = block
        vehicle_type = 'Bike' if block in ['A', 'C'] else 'Car'

        return render_template('customer_form.html', parking_space=parking_space, selected_block=selected_block, vehicle_type=vehicle_type)

    # Fetch parking slot information from the database
    query = "SELECT * FROM parking_slot"
    parking_slot_data = execute_query(query)
    return render_template('parking_slots.html', parking_slot_data=parking_slot_data)


@app.route('/ticket_display', methods=['GET'])
def ticket_display():
    # Extract parameters from the URL or session, adjust as needed
    parking_space = request.args.get('parking_space')
    is_occupied = request.args.get('is_occupied')
    ticket_id = request.args.get('ticket_id')  # Assuming the ticket ID is passed

    # Fetch additional ticket details for display
    query_ticket_details = "SELECT * FROM ticketgen WHERE TicketID = %s"
    data_ticket_details = (ticket_id,)
    ticket_details = execute_query(query_ticket_details, data_ticket_details, fetchone=True)

    # Render the ticket display template
    return render_template('ticket_display.html', parking_space=parking_space, is_occupied=is_occupied, ticket_details=ticket_details)

def generate_ticket_id():
    max_int_value = 2147483647  # Adjust based on your current maximum value
    timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
    numeric_value = 1234567890  # Replace with a unique numeric value or algorithm
    ticket_id = int(f"{timestamp_str}{numeric_value}") % max_int_value
    return ticket_id

def generate_ticket(username, parking_space):
    # Generate a ticket ID as an integer
    ticket_id = generate_ticket_id()

    # Get customer ID
    cust_id = get_customer_id(username)

    # Additional logic to store the ticket information in the 'ticketgen' table
    query_insert_ticket = "INSERT INTO ticketgen (TicketID, Cust_ID, VehicleType, PlateInformation, EntryTime) VALUES (%s, %s, %s, %s, %s)"
    data_insert_ticket = (ticket_id, cust_id, 'Car', 'ABC123', datetime.now())
    execute_query(query_insert_ticket, data_insert_ticket)

    # Fetch the generated ticket details from the database
    query_get_ticket = "SELECT * FROM ticketgen WHERE TicketID = %s"
    data_get_ticket = (ticket_id,)
    ticket_details = execute_query(query_get_ticket, data_get_ticket, fetchone=True)

    # Return the generated ticket details
    return ticket_details

def get_customer_id(username):
    # Fetch the 'CustomerID' from the 'customer_information' table based on the username
    query_get_customer_id = "SELECT CustomerID FROM customer_information WHERE name = %s"
    data_get_customer_id = (username,)
    result = execute_query(query_get_customer_id, data_get_customer_id, fetchone=True)

    print(result)  # Add this line for debugging

    if result:
        return result['CustomerID']
    else:
        # Handle the case where the customer does not exist
        raise ValueError(f"Customer with username '{username}' not found.")

if __name__ == '__main__':
    app.run(debug=True)