from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .sermons import query, get_sermon

bp = Blueprint('post', __name__)

@bp.route("/", methods=["GET", "POST"])
def search():
    results = []

    if request.method == "POST":
        results = query(request.args.get("query"))

    return render_template('post/search.html', results=results)
    
@bp.route("/view/<title>")
def view(title):
    post = get_sermon(title)
    return render_template("post/view.html", post=post)