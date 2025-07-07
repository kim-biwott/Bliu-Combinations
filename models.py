from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
import os

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///combinations.db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_session():
    return Session()

class SubjectCombination(Base):
    __tablename__ = 'subject_combinations'
    id = Column(Integer, primary_key=True)
    pathway = Column(String(100), nullable=False)
    track = Column(String(100), nullable=False)
    subjects = Column(Text, nullable=False)
    
    @classmethod
    def create(cls, session, **kwargs):
        try:
            combination = cls(**kwargs)
            session.add(combination)
            session.commit()
            return combination
        except IntegrityError as e:
            session.rollback()
            raise ValueError(str(e)) from e

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.get(cls, id)
    
    @classmethod
    def find_by_pathway(cls, session, pathway):
        return session.query(cls).filter(cls.pathway.ilike(f"%{pathway}%")).all()
    
    @classmethod
    def find_by_track(cls, session, track):
        return session.query(cls).filter(cls.track.ilike(f"%{track}%")).all()
    
    @classmethod
    def find_by_subject(cls, session, subject):
        return session.query(cls).filter(cls.subjects.ilike(f"%{subject}%")).all()
    
    @classmethod
    def find_combinations(cls, session, pathway=None, track=None, subjects=None):
        query = session.query(cls)
        if pathway:
            query = query.filter(cls.pathway.ilike(f"%{pathway}%"))
        if track:
            query = query.filter(cls.track.ilike(f"%{track}%"))
        if subjects:
            for subject in subjects:
                query = query.filter(cls.subjects.ilike(f"%{subject}%"))
        return query.all()
    
    def __repr__(self):
        return f"<Combination(id={self.id}, pathway='{self.pathway}', track='{self.track}')>"