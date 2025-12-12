import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# HTTP GET - Read Record
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    cafe=random.choice(all_cafes)
    # data={
    #     "name": cafe.name,
    #     "map_url": cafe.map_url,
    #     "img_url": cafe.img_url,
    #     "location": cafe.location,
    #
    #     "amenities": {
    #       "seats": cafe.seats,
    #       "has_toilet": cafe.has_toilet,
    #       "has_wifi": cafe.has_wifi,
    #       "has_sockets": cafe.has_sockets,
    #       "can_take_calls": cafe.can_take_calls,
    #       "coffee_price": cafe.coffee_price,
    #     }
    # }
    # cafe_serialized=jsonify(cafe=data)
    # return cafe_serialized
    return jsonify(cafe=cafe.to_dict())

@app.route("/all")
def all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search")
def all_cafes_at():
    location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location==location).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    if len(all_cafes) == 0:
        return jsonify(error={
            "Not Found" : "Sorry, we don't have cafe at this location."
        }), 404
    return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    body=request.form
    new_cafe = Cafe(name=body.get("name"),
                    map_url=body.get("map_url"),
                    img_url=body.get("img_url"),
                    location=body.get("location"),
                    seats=body.get("seats"),
                    has_toilet=bool(body.get("has_toilet")),
                    has_wifi=bool(body.get("has_wifi")),
                    has_sockets=bool(body.get("has_sockets")),
                    can_take_calls=bool(body.get("can_take_calls")),
                    coffee_price=body.get("coffee_price"),
                    )
    try:
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={
            "success" : "Successfully added the new cafe."
        })
    except:
        return jsonify(error={
            "Not executed": "Sorry, we don't add the new cafe."
        }), 404

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_cafe_price(cafe_id):
    try:
        cafe = db.session.get(Cafe, cafe_id)
    except AttributeError:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200

# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    try:
        cafe = db.session.get(Cafe, cafe_id)
    except AttributeError:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        api_key=request.args.get("api_key")
        if api_key == "TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

if __name__ == '__main__':
    app.run(debug=True)

    #my docs in postman: https://documenter.getpostman.com/view/50726073/2sB3dSP8Yv
