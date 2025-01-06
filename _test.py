import pytest
from flask import Flask, jsonify


# Тестируем Flask приложение
@pytest.fixture
def client():
    app = Flask(__name__)

    # Фейковая настройка для тестов
    @app.route("/plants", methods=["GET"])
    def get_plants():
        return jsonify(
            [
                {"id": 1, "species": "Фикус", "watering_frequency": "1 раз в неделю"},
                {
                    "id": 2,
                    "species": "Замиокулькас",
                    "watering_frequency": "2 раза в неделю",
                },
            ]
        )

    @app.route("/watering-info", methods=["GET"])
    def get_watering_info():
        return jsonify(
            {
                "species": "Фикус",
                "watering_frequency": "1 раз в неделю",
                "next_watering_date": "27.01.23",
            }
        )

    return app.test_client()


def test_get_plants(client):
    response = client.get("/plants")
    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "species": "Фикус", "watering_frequency": "1 раз в неделю"},
        {"id": 2, "species": "Замиокулькас", "watering_frequency": "2 раза в неделю"},
    ]


def test_get_watering_info_valid(client):
    response = client.get("/watering-info?username=cactuses&password=111cactus111")
    assert response.status_code == 200
    assert response.json == {
        "species": "Фикус",
        "watering_frequency": "1 раз в неделю",
        "next_watering_date": "27.01.23",
    }


def test_get_watering_info_invalid(client):
    response = client.get("/watering-info?username=invalid&password=invalid")
    assert response.status_code == 200


def test_post_plant(client):
    response = client.post(
        "/plants", json={"species": "Пальма", "watering_frequency": "2 раза в месяц"}
    )
    assert response.status_code == 405
    assert response.json is None
