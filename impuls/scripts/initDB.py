import os
import sys
import transaction

from sqlalchemy import engine_from_config, func

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..Base import (
    Base,
    User,
    Group,
    Event,
    Task,
    History,
    Member,
    Song,
    Comment
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: %s development.ini)' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    #DBSession.configure(bind=engine)
    #Base.metadata.create_all(engine)
    #with transaction.manager:
    from sqlalchemy import create_engine
    #engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import Session
    session = Session(bind=engine)
    session.add_all([
        User(idUser = 1, UserName='Sol', UserPass = "123"),
        User(idUser = 2, UserName='Cat', UserPass = "123"),
        User(idUser = 3, UserName='Xaver', UserPass = "123"),
        Group(idGroup = 1, GroupName = "Boec"),
        Group(idGroup = 2, GroupName = "TG"),
        Group(idGroup = 3, GroupName = "KS"),
        Group(idGroup = 4, GroupName = "old"),
        Event(idEvent = 1, EventName = "Kefirnik", EventDate = func.now()),
        Task (idTask = 1, TaskText = "Order", TaskStatus = False, idExecutor = 1, idDirector = 1),
        History(idHistory = 1, HistoryText = "test1"),
        Member(idMember = 1, MemberName = "Malakhov Konstantin Denisovich", MemberYear = func.now()),
        Song(idSong = 1, SongTitle = "Test2", SongText = "Text test2")
    ])
    session.commit()
        