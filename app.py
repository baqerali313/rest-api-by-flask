from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

    app.app_context().push()
    db.create_all()


@app.route('/users', methods=['GET'])
def get_user():
    users = Users.query.all()
    data = []
    for user in users:
        user_data = {'id': user.id, 'name': user.name}
        data.append(user_data)
    return {'users': data}


@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = Users.query.get_or_404(id)
    return {'id': user.id, 'name': user.name}


@app.route('/users', methods=['POST'])
def add_user():
    new_user = Users(name=request.json['name'])
    db.session.add(new_user)
    db.session.commit()
    return {'id': new_user.id, 'name': new_user.name}


@app.route('/users/<int:id>', methods=['PATCH'])
def update(id):
    user = Users.query.get_or_404(id)
    if 'name' in request.json:
        user.name = request.json['name']

    db.session.commit()
    return {'id': user.id, 'name': user.name}


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return {'message': 'delete done'}


if __name__ == "__main__":
    app.run(debug=True)
