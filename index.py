import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from database.index import connect_to_db

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("list_games"))


@app.route("/games", methods=["GET"])
def list_games():
    conn = connect_to_db()
    if not conn:
        return render_template("index.html", games=[])
    q = request.args.get("q", "")
    cursor = conn.cursor()
    if q:
        cursor.execute(
            """
            SELECT * FROM games
            WHERE title ILIKE %s OR genre ILIKE %s OR description ILIKE %s
            ORDER BY id DESC
            """,
            (f"%{q}%", f"%{q}%", f"%{q}%"),
        )
    else:
        cursor.execute("SELECT * FROM games ORDER BY id DESC")
    games = cursor.fetchall()
    conn.close()
    return render_template("index.html", games=games)


@app.route("/games/<int:id>", methods=["GET"])
def game_detail(id):
    conn = connect_to_db()
    if not conn:
        return render_template("details.html", game=None)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE id = %s", (id,))
    game = cursor.fetchone()
    conn.close()
    return render_template("details.html", game=game)


@app.route("/games/create", methods=["POST", "GET"])
def create_game():
    if request.method == "POST":
        payload = {
            "title": (request.form.get("title", "") or "").strip(),
            "description": (request.form.get("description", "") or "").strip(),
            "genre": (request.form.get("genre", "") or "").strip(),
            "release_year": request.form.get("release_year", ""),
            "rating": request.form.get("rating", ""),
        }

        errors = []
        if not payload["title"]:
            errors.append("Title is required")
        if not payload["description"]:
            errors.append("Description is required")
        if not payload["genre"]:
            errors.append("Genre is required")
        try:
            year_int = int(str(payload["release_year"]).strip())
            if year_int < 1950 or year_int > 2100:
                errors.append("Release year must be between 1950 and 2100")
        except Exception:
            errors.append("Release year must be a number")
            year_int = 0
        try:
            rating_float = float(str(payload["rating"]).strip())
            if rating_float < 0 or rating_float > 10:
                errors.append("Rating must be between 0 and 10")
        except Exception:
            errors.append("Rating must be a number")
            rating_float = 0.0

        if errors:
            for e in errors:
                flash(e, "red")
            return render_template("create.html", payload=payload)

        conn = connect_to_db()
        if not conn:
            flash("DB connection failed", "red")
            return render_template("create.html", payload=payload)

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO games (title, description, genre, release_year, rating)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (
                payload["title"],
                payload["description"],
                payload["genre"],
                year_int,
                rating_float,
            ),
        )
        conn.commit()
        conn.close()

        flash("Game created successfully", "blue")
        return redirect(url_for("list_games"))

    return render_template("create.html")


@app.route("/games/edit/<int:id>", methods=["POST", "GET"])
def edit_game(id):
    conn = connect_to_db()
    if not conn:
        return render_template("edit.html", game=None)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE id = %s", (id,))
    game = cursor.fetchone()

    if request.method == "POST":
        title = (request.form.get("title", "") or "").strip()
        description = (request.form.get("description", "") or "").strip()
        genre = (request.form.get("genre", "") or "").strip()
        release_year_raw = request.form.get("release_year", "")
        rating_raw = request.form.get("rating", "")

        errors = []
        if not title:
            errors.append("Title is required")
        if not description:
            errors.append("Description is required")
        if not genre:
            errors.append("Genre is required")
        try:
            year_int = int(str(release_year_raw).strip())
            if year_int < 1950 or year_int > 2100:
                errors.append("Release year must be between 1950 and 2100")
        except Exception:
            errors.append("Release year must be a number")
            year_int = game["release_year"] if game else 0
        try:
            rating_float = float(str(rating_raw).strip())
            if rating_float < 0 or rating_float > 10:
                errors.append("Rating must be between 0 and 10")
        except Exception:
            errors.append("Rating must be a number")
            rating_float = game["rating"] if game else 0.0

        if errors:
            for e in errors:
                flash(e, "red")
            conn.close()
            payload = {
                "id": id,
                "title": title,
                "description": description,
                "genre": genre,
                "release_year": release_year_raw,
                "rating": rating_raw,
            }
            return render_template("edit.html", game=payload)

        cursor.execute(
            """
            UPDATE games SET title = %s, description = %s, genre = %s, release_year = %s, rating = %s
            WHERE id = %s
        """,
            (title, description, genre, year_int, rating_float, id),
        )
        conn.commit()
        conn.close()

        flash("Game updated successfully", "blue")
        return redirect(url_for("game_detail", id=id))

    conn.close()
    return render_template("edit.html", game=game)


@app.route("/games/delete/<int:id>", methods=["POST"])
def delete_game(id):
    conn = connect_to_db()
    if not conn:
        return redirect(url_for("list_games"))

    cursor = conn.cursor()
    cursor.execute("DELETE FROM games WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    flash("Game deleted successfully", "blue")
    return redirect(url_for("list_games"))


# ---------------- STATS ----------------
@app.route("/stats", methods=["GET"])
def stats_page():
    conn = connect_to_db()
    if not conn:
        return render_template("stats.html", kpis={}, charts={})

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS n FROM games")
    total_games = cur.fetchone()["n"]

    cur.execute("SELECT ROUND(AVG(rating)::numeric,2) AS avg_rating FROM games")
    avg_rating = cur.fetchone()["avg_rating"]

    cur.execute(
        """
        SELECT genre, COUNT(*) AS n
        FROM games
        GROUP BY genre
        ORDER BY n DESC
        """
    )
    by_genre = cur.fetchall()

    cur.execute(
        """
        SELECT release_year AS year, COUNT(*) AS n
        FROM games
        GROUP BY release_year
        ORDER BY year ASC
        """
    )
    by_year = cur.fetchall()

    conn.close()

    kpis = {"total_games": total_games, "avg_rating": avg_rating}
    charts = {"by_genre": by_genre, "by_year": by_year}
    return render_template("stats.html", kpis=kpis, charts=charts)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
