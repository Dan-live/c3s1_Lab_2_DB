from sqlalchemy import Column, Integer, Date, Numeric
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connecting to the database
DATABASE_URL = 'postgresql://postgres:1@localhost:5432/postgres'
engine = create_engine(DATABASE_URL)

# Creating a base class from which all models will inherit
Base = declarative_base()

# Create a session to interact with the database
Session = sessionmaker()


class BookingTicket(Base):
    __tablename__ = 'booking_ticket'
    booking_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    room_number = Column(Integer, nullable=False)
    booking_start_date = Column(Date, nullable=False)
    booking_end_date = Column(Date, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

# ModelBookingTicket
#################################################################################
class ModelBookingTicket:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = create_engine(DATABASE_URL)
        self.session = Session.configure(bind=self.engine)
        self.session = Session()

    def add_booking_ticket(self, booking_id, client_id, room_number, booking_start_date, booking_end_date, price):
        try:
            new_booking = BookingTicket(
                booking_id=booking_id,
                client_id=client_id,
                room_number=room_number,
                booking_start_date=booking_start_date,
                booking_end_date=booking_end_date,
                price=price
            )
            self.session.add(new_booking)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error when adding a booking: {str(e)}")
            return False



    def update_booking_ticket(self, booking_id, client_id, room_number, booking_start_date, booking_end_date, price):
        try:
            # Receive a booking from the database by its unique identifier
            booking = self.session.query(BookingTicket).filter_by(booking_id=booking_id).first()

            # Check if the reservation exists in the database
            if booking:
                # Update booking information
                booking.client_id = client_id
                booking.room_number = room_number
                booking.booking_start_date = booking_start_date
                booking.booking_end_date = booking_end_date
                booking.price = price

                self.session.commit()
                return True  # Returns True if the update is successful
            else:
                return False  # Returns False if no reservation is found
        except Exception as e:
            self.session.rollback()
            print(f"Error when updating a reservation: {str(e)}")
            return False  # Returns False if an error occurs during the update


    def delete_booking_ticket(self, booking_id):
        try:
            # Receive a booking from the database by its unique identifier
            booking = self.session.query(BookingTicket).filter_by(booking_id=booking_id).first()

            # Check if the reservation exists in the database
            if booking:
                self.session.delete(booking)
                self.session.commit()
                return True  # Returns True if the deletion is successful
            else:
                return False  # Returns False if no reservation is found
        except Exception as e:
            self.session.rollback()
            print(f"Error when deleting a reservation: {str(e)}")
            return False  # Returns False in case of an error during deletion


    def get_all_booking_tickets(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM booking_ticket')
        return c.fetchall()

    def check_booking_existence(self, booking_id):
        c = self.conn.cursor()
        c.execute("SELECT 1 FROM booking_ticket WHERE booking_id = %s", (booking_id,))
        return bool(c.fetchone())

    def create_booking_sequence(self):
        c = self.conn.cursor()
        c.execute("""
           DO $$
           BEGIN
               IF NOT EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = 'booking_id_seq') THEN
                   CREATE SEQUENCE booking_id_seq;
               ELSE
                   DROP SEQUENCE booking_id_seq;
                   CREATE SEQUENCE booking_id_seq;
               END IF;
           END $$;
           """)
        self.conn.commit()

    def generate_rand_booking_ticket_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            c.execute("""
            INSERT INTO booking_ticket (booking_id, client_id, room_number, booking_start_date, booking_end_date, price)
            select * from (
            SELECT
                    nextval('booking_id_seq'),
                    floor(random() * (SELECT max(client_id) FROM client) + 1),
                    floor(random() * (SELECT max(room_number) FROM room) + 1),
                    ('2023-01-01'::date + floor(random() * 3) * interval '1 day' + floor(random() * 12) * interval '1 month' + floor(random() * 31) * interval '1 day') as start1,
                    ('2023-01-01'::date + floor(random() * 3) * interval '1 day' + floor(random() * 12) * interval '1 month' + floor(random() * 31) * interval '1 day') as finish1,
                	random() * 1000 
                FROM generate_series(1, %s)) as t
            WHERE start1 < finish1
                  """, (number_of_operations,))

            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error while generating booking tickets: {str(e)}")
            return False


    def truncate_booking_table(self):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""DELETE FROM booking_ticket""")
            self.conn.commit()
            return True  # Returns True if the insertion was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error when adding a client: {str(e)}")
            return False  # Returns False if insertion fails
