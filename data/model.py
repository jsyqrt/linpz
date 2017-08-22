# coding: utf-8

from sqlalchemy import create_engine, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

class Sim_Track(Base):
    __tablename__ = 'sim_tracks'

    id = Column('id', Integer, primary_key=True)
    sim_to_id = Column('sim_to_id', Integer, ForeignKey('tracks.id'), primary_key=True)
    sim_index = Column('sim_index', Integer)

class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    album = Column(String)
    artist = Column(String)

    publishers = Column(String)
    description = Column(String)
    length = Column(String)
    cue_type = Column(String)
    label = Column(String)
    release_date = Column(String)
    catalog = Column(String)
    composer = Column(String)
    genre = Column(String)

    sim_ids = relationship('Sim_Track', backref='tracks', lazy='dynamic')
    
    def __repr__(self):
        return "<Track(name='%s', album='%s', artist='%s')>" % (
                self.name, self.album, self.artist)


def get_sim_tracks(track_id=None, track_name=None, session=None):
    if not session:
        return None
    if track_name:
        track_id = session.query(Track.id).filter(Track.name == track_name).first()[0]
    if track_id:
        return session.query(Track).join(Sim_Track, Track.id==Sim_Track.sim_to_id).filter(Sim_Track.id == track_id).order_by(Sim_Track.sim_index).all()

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # query some.


