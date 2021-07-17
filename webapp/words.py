from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from webapp.db import get_db
from webapp.oxford_dict import Word
from webapp.auth import create_auth
AUTH = create_auth()

bp = Blueprint("words", __name__)

@bp.route("/")
@bp.route("/index.html")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        " SELECT id, name, definition, created"
        " FROM words"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("index.html", posts=posts, id="1")

@bp.route("/search", methods=['GET', 'POST'])
def search():
    """Search for the definitions of a word"""
    name = request.form['q']
    word = Word(name, AUTH)
    word.get_json()
    if word.status_code() != 200:
        flash(f"Word {name} doesn't exist.")

    return render_template("index.html",  id="1")

def get_post(id):
    """Get a post
    :param id: id of post to get
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
def create():
    """Create a new post."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            #return redirect(url_for("blog.index"))

    #return render_template("blog/create.html")
    return render_template("index.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    """Update a post."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    """Delete a post.
    Ensures that the post exists. """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM words WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))

