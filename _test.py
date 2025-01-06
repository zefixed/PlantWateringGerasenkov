import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash
from app import app
from models import Plant, User


# Фикстура для тестового клиента
@pytest.fixture
def test_client():
    # Используем SQLite в памяти для тестов
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with app.app_context():  # Добавить контекст приложения
        # Создаем все таблицы для тестирования
        # Например, если у вас есть db.create_all(), можно использовать это
        # db.create_all()
        with app.test_client() as client:
            yield client


@pytest.fixture
def mock_plants_and_users():
    # Моки для растений и пользователей
    mock_plant1 = MagicMock(spec=Plant)
    mock_plant1.id = 1
    mock_plant1.species = "Фикус"
    mock_plant1.watering_frequency = "1 раз в неделю"

    mock_plant2 = MagicMock(spec=Plant)
    mock_plant2.id = 2
    mock_plant2.species = "Замиокулькас"
    mock_plant2.watering_frequency = "2 раза в неделю"

    mock_plant3 = MagicMock(spec=Plant)
    mock_plant3.id = 3
    mock_plant3.species = "Кактус"
    mock_plant3.watering_frequency = "1 раз в неделю"

    mock_user1 = MagicMock(spec=User)
    mock_user1.username = "cactuses"
    mock_user1.password = generate_password_hash("111cactus111")
    mock_user1.plant_id = 3
    mock_user1.next_watering_date = "27.01.23"

    mock_user2 = MagicMock(spec=User)
    mock_user2.username = "planter"
    mock_user2.password = generate_password_hash("wfiosdjnv")
    mock_user2.plant_id = 1
    mock_user2.next_watering_date = "30.01.23"

    mock_user3 = MagicMock(spec=User)
    mock_user3.username = "maria"
    mock_user3.password = generate_password_hash("wfhowuhgvwou")
    mock_user3.plant_id = 1
    mock_user3.next_watering_date = "01.02.23"

    return {
        "plants": [mock_plant1, mock_plant2, mock_plant3],
        "users": [mock_user1, mock_user2, mock_user3],
    }


def test_get_plants(test_client, mock_plants_and_users):
    # Мокируем запрос к базе данных
    with patch("models.Plant.query.all", return_value=mock_plants_and_users["plants"]):
        response = test_client.get("/plants")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        assert data[0]["species"] == "Фикус"
        assert data[1]["watering_frequency"] == "2 раза в неделю"


def test_get_watering_info_valid_user(test_client, mock_plants_and_users):
    # Мокируем запросы для пользователей и растений
    with (
        patch(
            "models.User.query.filter_by",
            return_value=[mock_plants_and_users["users"][0]],
        ),
        patch(
            "models.Plant.query.get", return_value=mock_plants_and_users["plants"][2]
        ),
    ):
        response = test_client.get(
            "/watering-info?username=cactuses&password=111cactus111"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["species"] == "Кактус"
        assert data["watering_frequency"] == "1 раз в неделю"
        assert data["next_watering_date"] == "27.01.23"


def test_get_watering_info_invalid_credentials(test_client, mock_plants_and_users):
    # Мокируем запрос для отсутствующих пользователей
    with patch(
        "models.User.query.filter_by", return_value=[]
    ):  # Нет таких пользователей
        response = test_client.get(
            "/watering-info?username=cactuses&password=wrongpassword"
        )
        assert response.status_code == 401
        data = response.get_json()
        assert data["error"] == "Invalid credentials"


def test_get_watering_info_missing_params(test_client, mock_plants_and_users):
    response = test_client.get("/watering-info?username=cactuses")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Username and password are required"
