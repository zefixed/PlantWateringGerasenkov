from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash
from models import db, Plant, User

# Initialize Flask app
app = Flask(__name__)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:root@localhost/plant_watering"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Routes
@app.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    return jsonify(
        [
            {
                "id": plant.id,
                "species": plant.species,
                "watering_frequency": plant.watering_frequency,
            }
            for plant in plants
        ]
    )


@app.route("/watering-info", methods=["GET"])
def get_watering_info():
    username = request.args.get("username")
    password = request.args.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    plant = Plant.query.get(user.plant_id)
    return jsonify(
        {
            "species": plant.species,
            "watering_frequency": plant.watering_frequency,
            "next_watering_date": user.next_watering_date,
        }
    )


# Utility function to seed database (for demonstration purposes)
# Utility function to seed database (for demonstration purposes)
@app.cli.command("seed_db")
def seed_db():
    with app.app_context():
        db.create_all()

        if not Plant.query.first():
            # Add plants
            plant1 = Plant(species="Фикус", watering_frequency="1 раз в неделю")
            plant2 = Plant(species="Замиокулькас", watering_frequency="2 раза в неделю")
            plant3 = Plant(species="Кактус", watering_frequency="1 раз в неделю")
            db.session.add_all([plant1, plant2, plant3])

        if not User.query.first():
            # Add users
            user1 = User(
                username="cactuses",
                password="111cactus111",
                plant_id=3,
                next_watering_date="27.01.23",
            )
            user2 = User(
                username="planter",
                password="wfiosdjnv",
                plant_id=1,
                next_watering_date="30.01.23",
            )
            user3 = User(
                username="maria",
                password="wfhowuhgvwou",
                plant_id=1,
                next_watering_date="01.02.23",
            )
            db.session.add_all([user1, user2, user3])

        db.session.commit()
        print("Database seeded!")


if __name__ == "__main__":
    app.run(debug=True)
