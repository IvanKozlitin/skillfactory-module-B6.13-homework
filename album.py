import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

class InvalidAlbum(Exception):
    """
    Используется для идентификации некорректных данных для добавления нового альбома в базу данных
    """
    pass

class AlbumAvailable(InvalidAlbum):
    """
    Используется для идентификации того что, передаваемый альбом для добавления уже имеется в базе данных
    """
    def __init__(self, text):
        self.txt = text
        self.name = "AlbumAvailable"

class WrongYear(InvalidAlbum):
    """
    Используется для идентификации того что, передаваемый год альбома для добавления некорректен
    """
    def __init__(self, text):
        self.txt = text
        self.name = "WrongYear"

class WrongArtist(InvalidAlbum):
    """
    Используется для идентификации того что, имя артиста передаваемого альбома для добавления некорректено
    """
    def __init__(self, text):
        self.txt = text
        self.name = "WrongArtist"

class WrongGenre(InvalidAlbum):
    """
    Используется для идентификации того что, название жанра передаваемого альбома для добавления некорректено
    """
    def __init__(self, text):
        self.txt = text
        self.name = "WrongGenre"

class WrongAlbum(InvalidAlbum):
    """
    Используется для идентификации того что, название альбома передаваемого альбома для добавления некорректено
    """
    def __init__(self, text):
        self.txt = text
        self.name = "WrongAlbum"

class WrongForm(InvalidAlbum):
    """
    Используется для идентификации того что, в передаваемых данные не соответствуют схеме таблицы album
    """
    def __init__(self, text):
        self.txt = text
        self.name = "WrongForm"

def validation_check(album_data):
    """
    Проверка правильности введённых данных, для добавления нового альбома,
    используется в функции add_album()
    """

    # Проверяем наличие всех данных в соответствии со схемой таблицы album
    try:
        if album_data["year"] == None or album_data["artist"] == None or album_data["genre"] == None or album_data["album"] == None:
            raise WrongForm("Передаваемых данные не соответствуют схеме таблицы album")
    except WrongForm as err:
        return [err]

    session = connect_db()
    # Проверяем, есть ли уже альбом с таким именем
    albums = session.query(Album).filter(Album.album == album_data["album"]).first()
    try:
        if albums:
            raise AlbumAvailable("Такой альбом уже есть в базе данных")
        elif album_data["year"].isdigit() == False:
            raise WrongYear("Год переданного альбома не является числом")
        elif int(album_data["year"]) < 0 or int(album_data["year"]) > 2200:
            raise WrongYear("Год переданного альбома некорректен")
        elif album_data["artist"].isdigit():
            raise WrongArtist("Имя исполнителя состоит из одних цифр, что недопустимо")
        elif album_data["genre"].isdigit():
            raise WrongGenre("Название жанра состоит из одних цифр, что недопустимо")
        elif album_data["album"].isdigit():
            raise WrongGenre("Название альбома состоит из одних цифр, что недопустимо")
    except (AlbumAvailable, WrongYear, WrongArtist, WrongGenre, WrongAlbum) as err:
        return [err]
    else:
        return True # Отправляем 1 если все проверки успешно пройдены


def add_album(album_data):
    """
    Добавляет новый альбом в базу данных
    """
    session = connect_db()
    val_check = validation_check(album_data) # Проверяем валидность данных
    if val_check == True: # Если данные валидны, то записываем их
        new_album = Album(
            year=album_data["year"],
            artist=album_data["artist"],
            genre=album_data["genre"],
            album=album_data["album"]
        )

        session.add(new_album)
        session.commit()

        return new_album.album
    else: # Иначе передаём название ошибки
        return val_check