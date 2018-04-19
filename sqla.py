from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint
Base = declarative_base()


class HouseHold(Base):
    __tablename__ = 'households'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    utilities = relationship("Utility")

    __table_args__ = (
        UniqueConstraint('name', name='household_name'),
      ) 
    def __init__(self, name):
        self.name = name

class Utility(Base):
    __tablename__ = "utilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(Integer)
    name = Column(String)
    value = Column(String)
    __table_args__ = (
        ForeignKeyConstraint(['house_id'], ['households.id']),
      ) 
    def __init__(self, name, value, household):
        self.name = name
        self.value = value
        self.house_id = household.id

def query_sammy(sess,table_name='HouseHold'):
    hh = sess.query(HouseHold)
    for house in hh:
        print house.name
    
if __name__ == "__main__":
    engine = create_engine('postgresql://tanigai:tanigai@localhost:5432/sammy')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    print "Engine detail {}".format(engine)
    tanigai_house = HouseHold("Tanigai-1")

    session.add(tanigai_house)
    session.flush()
    session.refresh(tanigai_house)
    tanigai_utility = Utility("birthdate","25/08/1975", tanigai_house)
    print "Taigani house hold id...{}".format(tanigai_house.id)
    session.add(tanigai_utility)
    query_sammy(session) 
    hh = session.query(HouseHold)
    for house in hh:
        print "House hold name : {}".format(house.name)
    
    session.commit()
    session.close() 
