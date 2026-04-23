import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db


bp = Blueprint("core", __name__)


@bp.route("/")
def home():
    db = get_db()
    stats = {
        "clients": db.execute("SELECT COUNT(*) AS total FROM clients").fetchone()["total"],
        "active_memberships": db.execute(
            "SELECT COUNT(*) AS total FROM clients WHERE membership_status = ?",
            ("Active",),
        ).fetchone()["total"],
        "workouts": db.execute("SELECT COUNT(*) AS total FROM workouts").fetchone()["total"],
    }
    clients = db.execute(
        """
        SELECT id, name, program, membership_status, calories
        FROM clients
        ORDER BY name
        """
    ).fetchall()
    recent_workouts = db.execute(
        """
        SELECT workouts.date, workouts.workout_type, workouts.duration_min, clients.name AS client_name
        FROM workouts
        JOIN clients ON clients.name = workouts.client_name
        ORDER BY workouts.date DESC, workouts.id DESC
        LIMIT 5
        """
    ).fetchall()
    return render_template(
        "home.html",
        stats=stats,
        clients=clients,
        recent_workouts=recent_workouts,
    )


@bp.route("/clients/new", methods=("GET", "POST"))
def create_client():
    if request.method == "POST":
        name = request.form["name"].strip()
        membership_status = request.form["membership_status"].strip() or "Active"
        age = request.form.get("age") or None
        calories = request.form.get("calories") or None
        program = request.form.get("program", "").strip() or "Starter Plan"

        if not name:
            flash("Client name is required.", "error")
        else:
            db = get_db()
            try:
                db.execute(
                    """
                    INSERT INTO clients (name, age, program, calories, membership_status)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (name, age, program, calories, membership_status),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("Client name already exists.", "error")
            else:
                flash(f"Client '{name}' created.", "success")
                return redirect(url_for("core.home"))

    return render_template("client_form.html")


@bp.route("/clients/<int:client_id>")
def client_detail(client_id):
    db = get_db()
    client = db.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
    if client is None:
        return render_template("not_found.html"), 404

    workouts = db.execute(
        """
        SELECT id, date, workout_type, duration_min, notes
        FROM workouts
        WHERE client_name = ?
        ORDER BY date DESC, id DESC
        """,
        (client["name"],),
    ).fetchall()
    return render_template("client_detail.html", client=client, workouts=workouts)


@bp.route("/clients/<int:client_id>/workouts/new", methods=("POST",))
def create_workout(client_id):
    db = get_db()
    client = db.execute("SELECT id, name FROM clients WHERE id = ?", (client_id,)).fetchone()
    if client is None:
        return render_template("not_found.html"), 404

    workout_type = request.form["workout_type"].strip()
    date = request.form["date"].strip()
    duration_min = request.form["duration_min"].strip()
    notes = request.form.get("notes", "").strip()

    if not workout_type or not date or not duration_min:
        flash("Date, workout type, and duration are required.", "error")
        return redirect(url_for("core.client_detail", client_id=client_id))

    db.execute(
        """
        INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (client["name"], date, workout_type, duration_min, notes),
    )
    db.commit()
    flash("Workout logged successfully.", "success")
    return redirect(url_for("core.client_detail", client_id=client_id))
