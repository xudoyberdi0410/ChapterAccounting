from flask import Flask, request, render_template, redirect, make_response, jsonify
from app.discord import Discord
from app.mangalib import MangaLib
from app.db import Chapters, session
import os

app = Flask(__name__)

# Определяется путь к папке со списком тайтлов.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['manga_list'] = os.path.join(BASE_DIR, 'static', 'manga_list.json')

discord = Discord()
with app.app_context():
    mangalib = MangaLib()

@app.route("/")
def home_page():
    """
    Вовзращает главную страницу приложения, если пользователь авторизован.
    """
    
    if not 'access_token' in request.cookies:
        return redirect("/login")
    return render_template("index.html")

@app.route("/oauth/")
def oauth():
    """
    Выполняет процедуру аунтентификации пользователя через Discord. Устанавливает нужные куки файлы.
    """
    
    code = request.args.get("code")
    if not code:
        return {"Error": "Problems with logging. Please, try again."}
    res = discord.login(code=code)
    if res.get("status") == "success":
        access_token, refresh_token = discord.get_tokens()
        response = make_response(redirect("/", Response={"status": "success"}))
        response.set_cookie('access_token', access_token)
        response.set_cookie('refresh_token', refresh_token)
        response.set_cookie('username', res.get("username"))
        return response
    else:
        return redirect("/", Response={"status": "error"})

@app.route("/api/manga_list")
def get_manga_list():
    """
    Возвращает список тайтлов из файла manga_list.json.
    """
    
    return {"manga_list": mangalib.get_manga_list()}

@app.route("/login")
def login():
    """
    Страница логина пользователя.
    """
    
    return render_template("login.html")

@app.route("/login/discord")
def login_discord():
    """
    Генерирует ссылку и перенаправляет на страницу авторизации сервиса Discord.
    """
    
    return redirect(discord.generate_login_link())

@app.route("/logout")
def logout():
    """
    Удаляет все куки файлы и перенаправляет на страницу логина.
    """    
    resp = make_response(redirect("/login"))
    resp.delete_cookie("access_token")
    resp.delete_cookie("refresh_token")
    resp.delete_cookie("username")
    return resp

@app.route("/api/add", methods=['POST'])
def add_record():
    """
    Добавляет новую запись в базу данных.
    """
    
    if not 'access_token' in request.cookies:
        return redirect("/login")
    data = request.json

    chapter = Chapters(data.get("title"), data.get("number"), data.get("position"))
    session.add(chapter)
    session.commit()
    
    return redirect("/")

@app.route("/api/chapters", methods=['GET'])
def get_records():
    """
    Возвращает записи из базы данных в формате json. Поддерживает пагинацию. По умолчании последние 20 записей.
    """
    
    if not 'access_token' in request.cookies:
        return redirect("/login")
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    offset = (page - 1) * per_page

    chapters_query = session.query(Chapters).order_by(Chapters.ch_id.desc()).offset(offset).limit(per_page)
    chapters = [chapter.to_dict() for chapter in chapters_query.all()]

    total_count = session.query(Chapters).count()

    response = {
        "page": page,
        "per_page": per_page,
        "total_count": total_count,
        "total_pages": (total_count + per_page - 1) // per_page,
        "data": chapters
    }
    return jsonify(response)
