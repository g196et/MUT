from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, DateTime, BOOLEAN
from sqlalchemy import Numeric, func, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
#Helper table
permission_table = Table('Permissions', Base.metadata,
    Column('idEvent', Integer, ForeignKey('Event.idEvent')),
    Column('idGroup', Integer, ForeignKey('Group.idGroup'))
)

userGroup_table = Table('UserGroup', Base.metadata,
    Column('idUser', Integer, ForeignKey('Event.idEvent')),
    Column('idGroup', Integer, ForeignKey('Group.idGroup'))
)
#Primary Class
class User(Base):
    __tablename__ = 'Users'

    idUser = Column(Integer, primary_key=True)
    UserName = Column(String, nullable = False)
    UserPass = Column(String, nullable = False)
    Email = Column(String)
    VKID = Column(String)

    group = relationship(
        "Group",
        secondary=userGroup_table,
        back_populates="users")
    
    taskExecute = relationship("Task", back_populates="executors")
    taskDirect = relationship("Task", back_populates="directors")

    comment = relationship("Comment", back_populates="writer")
    def __repr__(self):
        return "<User(%r)>" % (
                self.UserName
            )

class Group(Base):
    __tablename__ = 'Groups'

    idGroup = Column(Integer, primary_key=True)
    GroupName = Column(String, nullable = False)

    event = relationship(
        "Event",
        secondary=permission_table,
        back_populates="groups")

    user = relationship(
        "User",
        secondary=userGroup_table,
        back_populates="groups")

    def __repr__(self):
        return "<Group(%r)>" % (
                self.GroupName
            )

class Event(Base):
    __tablename__ = 'Events'

    idEvent = Column(Integer, primary_key=True)
    EventName = Column(String, nullable = False)
    EventDate = Column(DateTime, nullable = False)
    EventPrice = Column(Integer)
    EventTime = Column(String)
    EventPlace = Column(String)
    EventGirls = Column(String)

    group = relationship(
        "Group",
        secondary=permission_table,
        back_populates="events")

    def __repr__(self):
        return "<Event(%r, %r)>" % (
                self.EventName, self.EventDate
            )

class Task(Base):
    __tablename__ = 'Tasks'

    idTask = Column(Integer, primary_key=True)
    TaskText = Column(String, nullable = False)
    TaskStatus = Column(BOOLEAN, nullable = False)
    idExecutor = Column(Integer, ForeignKey(User.idUser), nullable = False)
    execute = relationship('User', back_populates = "executors")
    idDirector = Column(Integer, ForeignKey(User.idUser), nullable = False)   
    direct = relationship ('User', back_populates = "directors")

    def __repr__(self):
        return "<Task(%r)>" % (
                self.TaskText
            )

class History(Base):
    __tablename__ = 'History'

    idHistory = Column(Integer, primary_key=True)
    HistoryText = Column(String, nullable = False)
    HistoryYear = Column(DateTime)

    def __repr__(self):
        return "<History(%r)>" % (
                self.HistoryText
            )

class Member(Base):
    __tablename__ = 'Members'

    idMember = Column(Integer, primary_key=True)
    MemberName = Column(String, nullable = False)
    MemberYear = Column(DateTime, nullable = False)
    MemberPhotoLink = Column(String)

    def __repr__(self):
        return "<member(%r, %r)>" % (
                self.MemberName, self.MemberYear
            )

class Song(Base):
    __tablename__ = 'Songs'

    idSong = Column(Integer, primary_key=True)
    SongTitle = Column(String, nullable = False)
    SongText = Column(String, nullable = False)
    SongWriter = Column(String)

    def __repr__(self):
        return "<member(%r, %r)>" % (
            self.MemberName, self.MemberYear
        )

class Comment(Base):
    __tablename__ = 'Comments'

    idComment = Column(Integer, primary_key=True)
    CommentText = Column(String, nullable = False)
    idWriter = Column(String, ForeignKey('Users.idUser'), nullable = False)

    writer = relationship('User', back_populates = "comment")

    def __repr__(self):
        return "<member(%r, %r)>" % (
            self.MemberName, self.MemberYear
        )

from sqlalchemy import create_engine
engine = create_engine('sqlite://')
Base.metadata.create_all(engine)
from sqlalchemy.orm import Session
session = Session(bind=engine)
session.add_all([
    User(idUser = 1, UserName='Соль', UserPass = "123"),
    User(idUser = 2, UserName='Киса', UserPass = "123"),
    User(idUser = 3, UserName='Ксавьер', UserPass = "123")
    Group(idGroup = 1, GroupName = "Боец")
    Group(idGroup = 2, GroupName = "ТГ")
    Group(idGroup = 3, GroupName = "КомСостав")
    Group(idGroup = 4, GroupName = "Старик")
    Event(idEvent = 1, EventName = "Знакомка", EventDate = func.now())
    Task (idTask = 1, TaskText = "Служебка", TaskStatus = False, idExecutor = 1, idDirector = 1)
    History(idHistory = 1, HistoryText = "Давным давно...")
    Member(idMember = 1, MemberName = "Малахов Константин Денисович", MemberYear = func.now())
    Song(idSong = 1, SongTitle = "Вот моя целинка", SongText = "Вот моя целинка, а на ней значёк")
])
session.commit()