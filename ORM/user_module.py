from sqlalchemy import Column,Integer,String,DateTime,Boolean
from .connect import Base,session
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from sqlalchemy import ForeignKey



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True ,autoincrement=True )
    username = Column(String(20))
    password = Column(String (50))
    creatime = Column(DateTime,default=datetime.now)
    _locked = Column(Boolean,default=False ,nullable=False)

    @classmethod  # 类装饰器，cls相当于类名
    def by_id(cls, id):
        return session.query(cls).filter(cls.id == id).first()

    @classmethod #类装饰器，cls相当于类名
    def by_name(cls,name):
        return session.query(cls).filter(cls.username==name).first()



    def __repr__(self):
        return '''<User(id = %s,username=%s,password=%s,creatime=%s,_locked=%s)>
        '''%(
            self.id,
            self.username,
            self.password,
            self.creatime,
            self._locked
        )



class UserDetails(Base):
    __tablename__ = 'user_details'
    id = Column(Integer ,primary_key= True ,autoincrement= True )
    id_card = Column(Integer ,nullable= True , unique= True )
    lost_login = Column (DateTime )
    login_num = Column(Integer ,default=0 )
    user_id = Column(Integer ,ForeignKey('user.id'),unique= True)

    userdetail = relationship('User',backref='details',uselist = False ,cascade = 'all')

    def __repr__(self):
        return '<UserDetails(id=%s,id_card=%s,lost_login=%s,login_num=%s,user_id=%s)>'%(
            self.id,
            self.id_card ,
            self.lost_login ,
            self.login_num,
            self.user_id
        )


user_article = Table('user_article',Base.metadata,
                     Column('user_id',Integer,ForeignKey('user.id'),primary_key= True),
                     Column('article.id',Integer,ForeignKey('article.id'),primary_key=True)
                     )

class Article(Base):
    __tablename__='article'
    id = Column(Integer,primary_key= True ,autoincrement= True)
    content = Column(String(500),nullable=True)
    create_time = Column(DateTime,default= datetime.now)


    article_user = relationship('User',backref='article',secondary=user_article)

    def __repr__(self):
        return 'Article(id=%s,content=%s,create_time=%s)'%(
            self.id,
            self.content,
            self.create_time
        )



if __name__ == '__main__':
    Base.metadata.create_all()