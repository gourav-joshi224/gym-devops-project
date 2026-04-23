from pathlib import Path
import sqlite3

import pytest

from aceest_app import create_app


@pytest.fixture()
def app(tmp_path: Path):
    database_path = tmp_path / "test.db"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(database_path),
            "SECRET_KEY": "test",
        }
    )
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Gym operations dashboard built for CI/CD delivery." in response.data


def test_create_client_persists_record(client, app):
    response = client.post(
        "/clients/new",
        data={
            "name": "Raghav Sharma",
            "age": "28",
            "program": "Muscle Gain",
            "calories": "2600",
            "membership_status": "Active",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Client &#39;Raghav Sharma&#39; created." in response.data

    with sqlite3.connect(app.config["DATABASE"]) as connection:
        row = connection.execute(
            "SELECT name, program, calories FROM clients WHERE name = ?",
            ("Raghav Sharma",),
        ).fetchone()

    assert row == ("Raghav Sharma", "Muscle Gain", 2600)


def test_create_client_requires_name(client):
    response = client.post(
        "/clients/new",
        data={
            "name": "",
            "age": "28",
            "program": "Fat Loss",
            "calories": "2200",
            "membership_status": "Active",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Client name is required." in response.data


def test_client_detail_shows_logged_workout(client):
    client.post(
        "/clients/new",
        data={
            "name": "Anaya Gupta",
            "age": "25",
            "program": "Performance",
            "calories": "2400",
            "membership_status": "Active",
        },
    )

    response = client.post(
        "/clients/1/workouts/new",
        data={
            "date": "2026-04-23",
            "workout_type": "Strength",
            "duration_min": "70",
            "notes": "Heavy lower body session",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Workout logged successfully." in response.data
    assert b"Heavy lower body session" in response.data
