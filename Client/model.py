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

    # def add_client(self, client_id, name, surname, email):
    #     c = self.conn.cursor()
    #     try:
    #         c.execute('INSERT INTO client (client_id, name, surname, email) VALUES (%s, %s, %s, %s)',
    #                   (client_id, name, surname, email))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"Error when adding a client: {str(e)}")
    #         return False  # Returns False if insertion fails

    def update_client(self, client_id, name, surname, email):
        try:
            # Отримуємо бронювання з бази даних за його унікальним ідентифікатором
            client = self.session.query(Client).filter_by(client_id=client_id).first()

            if client:
                # Оновлюємо дані про бронювання
                client.name = name
                client.surname = surname
                client.email = email

                self.session.commit()
                return True  # Повертає True у випадку успішного оновлення
            else:
                return False  # Повертає False, якщо бронювання не знайдено
        except Exception as e:
            self.session.rollback()
            print(f"Error when updating the client: {str(e)}")
            return False   # Returns False if insertion fails

    # def update_client(self, client_id, name, surname, email):
    #     c = self.conn.cursor()
    #     try:
    #         c.execute('UPDATE client SET name=%s, surname=%s, email=%s WHERE client_id=%s',
    #                   (name, surname, email, client_id))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"Error when updating the client: {str(e)}")
    #         return False   # Returns False if insertion fails


    def delete_client(self, client_id):
        try:
            # Отримуємо бронювання з бази даних за його унікальним ідентифікатором
            client = self.session.query(Client).filter_by(client_id=client_id).first()

            # Перевіряємо, чи бронювання існує у базі даних
            if client:
                # Видаляємо бронювання з сесії SQLAlchemy
                self.session.delete(client)
                self.session.commit()
                return True  # Повертає True у випадку успішного видалення
            else:
                return False  # Повертає False, якщо бронювання не знайдено
        except Exception as e:
            self.session.rollback()
            print(f"An error when deleting a client breaks the foreign key restriction: {str(e)}")
            return False   # Returns False if insertion fails

    # def delete_client(self, client_id):
    #     c = self.conn.cursor()
    #     try:
    #         c.execute('DELETE FROM client WHERE client_id=%s', (client_id,))
    #         self.conn.commit()
    #         return True  # Returns True if the update was successful
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"An error when deleting a client breaks the foreign key restriction: {str(e)}")
    #         return False   # Returns False if insertion fails




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