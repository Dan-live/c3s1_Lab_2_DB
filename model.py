import psycopg2


class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='1',
            host='localhost',
            port=5432
        )
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        # Check for tables
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'booking_ticket')")
        booking_ticket_table_exists = c.fetchone()[0]

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'client')")
        client_table_exists = c.fetchone()[0]

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'room')")
        room_table_exists = c.fetchone()[0]

        if not booking_ticket_table_exists:
            c.execute('''
                        CREATE TABLE booking_ticket (
                            booking_id SERIAL PRIMARY KEY,
                            client_id INTEGER NOT NULL,
                            room_number INTEGER NOT NULL,
                            booking_start_date DATE NOT NULL,
                            booking_end_date DATE NOT NULL,
                            price DECIMAL(10, 2) NOT NULL
                        )
                    ''')
        if not client_table_exists:
            c.execute('''
                        CREATE TABLE client (
                            client_id SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            email TEXT
                        )
                    ''')
        if not room_table_exists:
            c.execute('''
                        CREATE TABLE room (
                            room_number SERIAL PRIMARY KEY,
                            room_type TEXT NOT NULL
                        )
                    ''')

        self.conn.commit()


