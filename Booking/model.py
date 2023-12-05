

from sqlalchemy import Column, Integer, Date, Numeric
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# З'єднання з базою даних
DATABASE_URL = 'postgresql://postgres:1@localhost:5432/postgres'  # Приклад URL для PostgreSQL
engine = create_engine(DATABASE_URL)

# Створення базового класу, від якого будуть наслідуватися всі моделі
Base = declarative_base()

# Створення сесії для взаємодії з базою даних
Session = sessionmaker()
session = Session()

class BookingTicket(Base):
    __tablename__ = 'booking_ticket'
    #__table_args__ = {'bind': engine}
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
        #self.session = db_model.session
        self.engine = create_engine(DATABASE_URL)
        self.session = Session()
    # def add_booking_ticket(self, booking_id, client_id, room_number, booking_start_date, booking_end_date, price):
    #     c = self.conn.cursor()
    #     try:
    #         # Check if client_id and room_number match parent tables
    #         c.execute('SELECT 1 FROM client WHERE client_id = %s', (client_id,))
    #         client_exists = c.fetchone()
    #
    #         c.execute('SELECT 1 FROM room WHERE room_number = %s', (room_number,))
    #         room_exists = c.fetchone()
    #
    #         if not client_exists or not room_exists:
    #             # Return an exception notification and throw an error
    #             return False  # Or throw an exception to process it further
    #         else:
    #             # All checks have passed, insert into booking_ticket
    #             c.execute(
    #                 'INSERT INTO booking_ticket (booking_id, client_id, room_number, '
    #                 'booking_start_date, booking_end_date, price) VALUES (%s, %s, %s, %s, %s, %s)',
    #                 (booking_id, client_id, room_number, booking_start_date, booking_end_date, price))
    #             self.conn.commit()
    #             return True
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"Error when adding a booking: {str(e)}")
    #         return False

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


    def get_all_booking_tickets(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM booking_ticket')
        return c.fetchall()

    def update_booking_ticket(self, booking_id, client_id, room_number, booking_start_date, booking_end_date, price):
        try:
            # Отримуємо бронювання з бази даних за його унікальним ідентифікатором
            booking = self.session.query(BookingTicket).filter_by(booking_id=booking_id).first()

            # Перевіряємо, чи бронювання існує у базі даних
            if booking:
                # Оновлюємо дані про бронювання
                booking.client_id = client_id
                booking.room_number = room_number
                booking.booking_start_date = booking_start_date
                booking.booking_end_date = booking_end_date
                booking.price = price

                self.session.commit()
                return True  # Повертає True у випадку успішного оновлення
            else:
                return False  # Повертає False, якщо бронювання не знайдено
        except Exception as e:
            self.session.rollback()
            print(f"Error when updating a reservation: {str(e)}")
            return False  # Повертає False у випадку помилки під час оновлення


    # def update_booking_ticket(self, booking_id, client_id, room_number, booking_start_date, booking_end_date, price):
    #     c = self.conn.cursor()
    #     try:
    #         # Attempting to update a record
    #         c.execute('UPDATE booking_ticket SET client_id=%s, room_number=%s, booking_start_date=%s, '
    #                   'booking_end_date=%s, price=%s WHERE booking_id=%s',
    #                   (client_id, room_number, booking_start_date, booking_end_date, price, booking_id))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         # Handling an error if the update failed
    #         self.conn.rollback()
    #         print(f"Error when updating a reservation: {str(e)}")
    #         return False   # Returns False if insertion fails

    def delete_booking_ticket(self, booking_id):
        try:
            # Отримуємо бронювання з бази даних за його унікальним ідентифікатором
            booking = self.session.query(BookingTicket).filter_by(booking_id=booking_id).first()

            # Перевіряємо, чи бронювання існує у базі даних
            if booking:
                # Видаляємо бронювання з сесії SQLAlchemy
                self.session.delete(booking)
                self.session.commit()
                return True  # Повертає True у випадку успішного видалення
            else:
                return False  # Повертає False, якщо бронювання не знайдено
        except Exception as e:
            self.session.rollback()
            print(f"Error when deleting a reservation: {str(e)}")
            return False  # Повертає False у випадку помилки під час видалення

    # def delete_booking_ticket(self, booking_id):
    #     c = self.conn.cursor()
    #     try:
    #         # Attempting to update a record
    #         c.execute('DELETE FROM booking_ticket WHERE booking_id=%s', (booking_id,))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         # Handling an error in case the deletion failed
    #         self.conn.rollback()
    #         print(f"Error when deleting a reservation: {str(e)}")
    #         return False   # Returns False if insertion fails

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
