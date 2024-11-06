from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column, Integer, String, create_engine,select

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(100))
    age = Column(Integer)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}, age={self.age!r})"

engine = create_engine("sqlite:///sync.db", echo=True)
# User.metadata.create_all(engine)    # Create the table

# with Session(engine) as session:
#     user = select(User).where(User.id == 1)
#
select_session = Session(engine)
user = select_session.query(User).filter(User.id == 1).first
print(user)