from sqlalchemy import Column, Integer, String
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


class Room(Base):
    __tablename__ = 'room'
    room_number = Column(Integer, primary_key=True)
    room_type = Column(String, nullable=False)

# ModelRoom
##############################################################################
class ModelRoom:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = create_engine(DATABASE_URL)
        self.session = Session.configure(bind=self.engine)
        self.session = Session()


    def add_room(self, room_number, room_type):
        try:
            new_room = Room(
                room_number=room_number,
                room_type=room_type
            )
            self.session.add(new_room)
            self.session.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.session.rollback()
            print(f"Error when adding a room: {str(e)}")
            return False   # Returns False if insertion fails
    # def add_room(self, room_number, room_type):
    #     c = self.conn.cursor()
    #     try:
    #         c.execute('INSERT INTO room (room_number ,room_type) VALUES (%s, %s)', (room_number, room_type,))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"Error when adding a room: {str(e)}")
    #         return False   # Returns False if insertion fails



    def update_room(self, room_number, room_type):
        try:
            # Отримуємо бронювання з бази даних за його унікальним ідентифікатором
            room = self.session.query(Room).filter_by(room_number=room_number).first()

            if room:
                # Оновлюємо дані про бронювання
                room.name = room_number
                room.surname = room_type

                self.session.commit()
                return True  # Повертає True у випадку успішного оновлення
            else:
                return False  # Повертає False, якщо бронювання не знайдено
        except Exception as e:
            self.session.rollback()
            print(f"Error when updating a room: {str(e)}")
            return False   # Returns False if insertion fails

    # def update_room(self, room_number, room_type):
    #     c = self.conn.cursor()
    #     try:
    #         c.execute('UPDATE room SET room_type=%s WHERE room_number=%s', (room_type, room_number))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"Error when updating a room: {str(e)}")
    #         return False   # Returns False if insertion fails



    def delete_room(self, room_number):
        try:
            # Отримуємо бронювання з бази даних за його унікальним ідентифікатором
            room = self.session.query(Room).filter_by(room_number=room_number).first()

            # Перевіряємо, чи бронювання існує у базі даних
            if room:
                # Видаляємо бронювання з сесії SQLAlchemy
                self.session.delete(room)
                self.session.commit()
                return True  # Повертає True у випадку успішного видалення
            else:
                return False  # Повертає False, якщо бронювання не знайдено
        except Exception as e:
            self.session.rollback()
            print(f"Error when deleting a room: {str(e)}")
            return False  # Returns False if insertion fails


    # def delete_room(self, room_number):
    #     c = self.conn.cursor()
    #     try:
    #         c.execute('DELETE FROM room WHERE room_number=%s', (room_number,))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"Error when deleting a room: {str(e)}")
    #         return False  # Returns False if insertion fails



    def get_all_rooms(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM room')
        return c.fetchall()


    def check_room_existence(self, room_number):
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM room WHERE room_number = %s', (room_number,))
        return c.fetchone() is not None

    def create_room_sequence(self):
        # Check for the existence of a sequence
        c = self.conn.cursor()
        c.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = 'room_number_seq') THEN
                -- Якщо послідовності не існує, створюємо її
                CREATE SEQUENCE room_number_seq;
            ELSE
                -- Якщо послідовність існує, видаляємо і створюємо нову
                DROP SEQUENCE room_number_seq;
                CREATE SEQUENCE room_number_seq;
            END IF;
        END $$;
        """)
        self.conn.commit()
    def generate_rand_room_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""
            INSERT INTO room (room_number, room_type)
            SELECT
                nextval('room_number_seq'), 
                (array['Single', 'Double', 'Suite'])[floor(random() * 3) + 1]
            FROM generate_series(1, %s);
            """, (number_of_operations,))
            self.conn.commit()
            return True  # Returns True if the insertion was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error when adding a room: {str(e)}")
            return False   # Returns False if insertion fails

    def truncate_room_table(self):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""DELETE FROM room""")
            self.conn.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error when adding a client: {str(e)}")
            return False   # Returns False if insertion fails