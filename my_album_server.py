from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    """
    GET запрос по адресу /albums/<artist> показывающий общее количество альбомов,
    запрошенного артиста и вывод всего списка его альбомов, и выведение ошибки если альбы не найдены.
    """
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Количесто альбомов {}: {}\n".format(artist, len(album_names))
        result += "Список альбомов {}: ".format(artist)
        result += ", ".join(album_names)
    return result

@route("/albums", method="POST")
def album_add():
    """
    POST запрос по адресу /albums, который при передаче валидных данных добавляет новый альбом в базу данных.
    """
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    name_new_album = album.add_album(album_data)
    if isinstance(name_new_album, str):
        print("Album add: ", name_new_album)
        result = "Данные успешно сохранены"
    elif name_new_album[0].name == "AlbumAvailable":
        message = "{} - {}".format(name_new_album[0].name ,str(name_new_album[0]))
        result = HTTPError(409, message)
    else:
        message = "{} - {}".format(name_new_album[0].name ,str(name_new_album[0]))
        result = HTTPError(400, message)
    return result
    

    
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)