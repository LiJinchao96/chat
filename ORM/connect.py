from sqlalchemy import create_engine

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

Db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE
)

engine = create_engine(Db_url)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()

if __name__ == '__main__':
    conetion = engine.connect()
    result = conetion.execute('select 1')#能查到1说明能够连接
    print(result.fetchone())

