from sqlalchemy import (
    create_engine,
    insert,
    MetaData,
    Table,
    Column,
    Integer,
    Boolean,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    scoped_session,
    sessionmaker,
    Session as SessionType,
    relationship
)
from datetime import datetime
import re


DB_URL = 'sqlite:///my_blog.db'
DB_ECHO = True
engine = create_engine(url=DB_URL, echo=DB_ECHO)
Base = declarative_base(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    fullname = Column(String(100))
    is_admin = Column(Boolean, nullable=False, default=False)
    posts = relationship('Post', backref='users')

    def __str__(self):
        return (
            f'{self.__class__.__name__}('
            f'id={self.id}, '
            f'username={self.username!r}, '
            f'fullname={self.fullname}, '
            f'is admin={self.is_admin})'
        )

    def __repr__(self):
        return str(self)


post_tag = Table('post_tag', Base.metadata,
                 Column('post_id', Integer, ForeignKey('posts.id')),
                 Column('tag_id', Integer, ForeignKey('tags.id'))
                 )


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    slug = Column(String(150), unique=True)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __str__(self):
        return f'<Post id: {self.id}, title: {self.title}, slug: {self.slug}>'

    def __repr__(self):
        return str(self)

    def generate_slug(self):
        if self.title:
            pattern = r'[^\w+]'
            self.slug = re.sub(pattern, '-', self.title)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    post = relationship('Post', secondary=post_tag, backref='tags')

    def __str__(self):
        return f'tag id: {self.id} name: {self.name}'

    def __repr__(self):
        return str(self)


def create_user(session: SessionType, username: str, fullname: str) -> User:
    user = User(username=username, fullname=fullname)
    session.add(user)
    session.commit()
    return user


def create_post(session: SessionType, title: str, body: str, user_id: int) -> Post:
    post = Post(title=title, body=body, user_id=user_id)
    session.add(post)
    session.commit()
    return post


def create_tag(session: SessionType, name: str) -> Tag:
    tag = Tag(name=name)
    session.add(tag)
    session.commit()
    return tag


def query_all_users(session: SessionType) -> list[User]:
    return session.query(User).all()


def find_posts_by_userid(session: SessionType, user_id: int) -> list[User]:
    return session.query(Post).filter(Post.user_id == user_id).all()


def main():
    Base.metadata.create_all(bind=engine)
    session: SessionType = Session()
    user1 = create_user(session, username='vanya', fullname='Ivanov Ivan')
    user2 = create_user(session, username='qwerty', fullname='Samuel L. Jackson')
    user3 = create_user(session, username='zorro', fullname='Peter Jackson')

    create_post(session, title='Post 1', body='Body of post 1', user_id=user2.id)
    create_post(session, title='Post 2', body='Body of post 2', user_id=user2.id)
    create_post(session, title='Post 3', body='Body of post 3', user_id=user1.id)
    create_post(session, title='Post 4', body='Body of post 4', user_id=user3.id)
    create_post(session, title='Post 5', body='Body of post 5', user_id=user2.id)

    create_tag(session, name='tag1')
    create_tag(session, name='tag2')

    session.execute(post_tag.insert().values([
        {'post_id': 1, 'tag_id': 1},
        {'post_id': 2, 'tag_id': 1},
        {'post_id': 2, 'tag_id': 2},
        {'post_id': 3, 'tag_id': 2},
        {'post_id': 4, 'tag_id': 1},

    ]))
    session.commit()

    users = query_all_users(session)
    print('#' * 100)
    print('Users:', users)
    posts = find_posts_by_userid(session, user2.id)
    print('#' * 100)
    print(f'Posts of user {user2.fullname}', posts)

    session.close()


if __name__ == '__main__':
    main()
