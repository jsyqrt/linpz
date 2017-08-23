# coding: utf-8

from sqlalchemy import create_engine, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

class Sim_Track(Base):
    __tablename__ = 'sim_tracks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sim_from_id = Column(Integer, ForeignKey('tracks.id'))
    sim_to_id = Column(Integer, ForeignKey('tracks.id'))
    sim_index = Column(Integer)

class Track(Base):
    __tablename__ = 'tracks'

    id = Column('id', Integer, primary_key=True, autoincrement=False)
    name = Column(String(1000))
    album = Column(String(1000))
    artist = Column(String(1000))

    publishers = Column(String(1000))
    description = Column(String(1000))
    length = Column(String(1000))
    cue_type = Column(String(1000))
    label = Column(String(1000))
    release_date = Column(String(1000))
    catalog = Column(String(1000))
    composer = Column(String(1000))
    genre = Column(String(1000))

    sims = relationship('Track', secondary=Sim_Track, backref=backref('tracks', lazy='dynamic'))
    
    def __repr__(self):
        return "<Track(id='%s', name='%s', album='%s', artist='%s')>" % (
                self.id, self.name, self.album, self.artist)


def get_sim_tracks(track_id=None, track_name=None, session=None):
    if not session:
        return None
    if track_name:
        track_id = session.query(Track.id).filter(Track.name == track_name).first()[0]
    if track_id:
        return session.query(Track).join(Sim_Track, Track.id==Sim_Track.sim_to_id).filter(Sim_Track.sim_from_id == track_id).order_by(Sim_Track.sim_index).all()

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://localhost/songs_to_your_eyes')#, echo=True)
    # engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # query some.
    # for i in get_sim_tracks(track_id=10792495, session=session):
    #    print i
