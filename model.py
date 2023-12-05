from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BookingTicket(Base):
    __tablename__ = 'booking_ticket'

    booking_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    room_number = Column(Integer, nullable=False)
    booking_start_date = Column(Date, nullable=False)
    booking_end_date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String)

class Room(Base):
    __tablename__ = 'room'

    room_number = Column(Integer, primary_key=True)
    room_type = Column(String, nullable=False)

class Model:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:1@localhost/postgres')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_connection(self):
        self.session.close()
