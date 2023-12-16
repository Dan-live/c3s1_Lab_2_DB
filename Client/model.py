from sqlalchemy import Column, Integer, String
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

class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)



# ModelClient
############################################################################
class ModelClient:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = create_engine(DATABASE_URL)
        self.session = Session.configure(bind=self.engine)
        self.session = Session()

    def add_client(self, client_id, name, surname, email):
        try:
            new_client = Client(
                client_id=client_id,
                name=name,
                surname=surname,
                email=email
            )
            self.session.add(new_client)
            self.session.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.session.rollback()
            print(f"Error when adding a client: {str(e)}")
            return False  # Returns False if insertion fails


    def update_client(self, client_id, name, surname, email):
        try:
            # Receive a booking from the database by its unique identifier
            client = self.session.query(Client).filter_by(client_id=client_id).first()

            if client:
                # Update booking information
                client.name = name
                client.surname = surname
                client.email = email

                self.session.commit()
                return True  # Returns True if the update is successful
            else:
                return False  # Returns False if no reservation is found
        except Exception as e:
            self.session.rollback()
            print(f"Error when updating the client: {str(e)}")
            return False   # Returns False if insertion fails

    def delete_client(self, client_id):
        try:
            # Receive a booking from the database by its unique identifier
            client = self.session.query(Client).filter_by(client_id=client_id).first()

            # Check if the reservation exists in the database
            if client:
                self.session.delete(client)
                self.session.commit()
                return True  # Returns True if the deletion is successful
            else:
                return False  # Returns False if no reservation is found
        except Exception as e:
            self.session.rollback()
            print(f"An error when deleting a client breaks the foreign key restriction: {str(e)}")
            return False   # Returns False if insertion fails


    def get_all_clients(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM client')
        return c.fetchall()

    def check_client_existence(self, client_id):
        c = self.conn.cursor()
        c.execute("SELECT 1 FROM client WHERE client_id = %s", (client_id,))
        return bool(c.fetchone())

    def create_client_sequence(self):
        # Check for the existence of a sequence
        c = self.conn.cursor()
        c.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = 'client_id_seq') THEN
                -- Якщо послідовності не існує, створюємо її
                CREATE SEQUENCE client_id_seq;
            ELSE
                -- Якщо послідовність існує, видаляємо і створюємо нову
                DROP SEQUENCE client_id_seq;
                CREATE SEQUENCE client_id_seq;
            END IF;
        END $$;
        """)
        self.conn.commit()

    def generate_rand_client_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""
            INSERT INTO client (client_id, name, surname, email)
            SELECT
                nextval('client_id_seq'), 
                (array['John', 'Alice', 'Bob', 'Emma', 'Michael'])[floor(random() * 5) + 1], 
                (array['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson'])[floor(random() * 5) + 1],  
                (substr(md5(random()::text), 1, 10) || '@gmail.com') 
            FROM generate_series(1, %s);
            """, (number_of_operations,))
            self.conn.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error when adding a client: {str(e)}")
            return False   # Returns False if insertion fails


    def truncate_client_table(self):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""DELETE FROM client""")
            self.conn.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error when adding a client: {str(e)}")
            return False   # Returns False if insertion fails