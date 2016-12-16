from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, DateTime, BOOLEAN
from sqlalchemy import Numeric, func, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
#Helper table
userGroup_table = Table('User2Group', Base.metadata,
    Column('idGroup', Integer, ForeignKey('Groups.idGroup')),
    Column('idUser', Integer, ForeignKey('Users.idUser'))
)

permission_table = Table('Permissions', Base.metadata,
    Column('idEvent', Integer, ForeignKey('Events.idEvent')),
    Column('idGroup', Integer, ForeignKey('Groups.idGroup'))
)
#Primary Class
class User(Base):
    __tablename__ = 'Users'

    idUser = Column(Integer, primary_key=True)
    UserName = Column(String, nullable = False)
    UserPass = Column(String, nullable = False)
    Email = Column(String)
    VKID = Column(String)

    group2user = relationship(
        "Group",
        secondary=userGroup_table,
        back_populates="user2group")
    
#    taskExecute = relationship("Task", back_populates="executors")
#    taskDirect = relationship("Task", back_populates="directors")


    comment = relationship("Comment", back_populates="writer")
    def __repr__(self):
        return "<User(%r)>" % (
                self.UserName
            )

class Group(Base):
    __tablename__ = 'Groups'

    idGroup = Column(Integer, primary_key=True)
    GroupName = Column(String, nullable = False)

    events = relationship(
        "Event",
        secondary=permission_table,
        back_populates="groups")

    user2group = relationship(
        "User",
        secondary=userGroup_table,
        back_populates="group2user")

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

    groups = relationship(
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
    executors = relationship('User', foreign_keys = [idExecutor])
    idDirector = Column(Integer, ForeignKey(User.idUser), nullable = False)   
    directors = relationship ('User', foreign_keys = [idDirector])

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