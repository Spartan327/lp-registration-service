from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://mnqwfzlh:Dvthtq9BU6RjsvfO-R7m9PVSnxxQWvSk@hattie.db.elephantsql.com:5432/mnqwfzlh')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()