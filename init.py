from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os
# from werkzeug.utils import safe_str_cmp

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)


class Userdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(60), nullable=False)


with app.app_context():
    db.create_all()

# Error handling for 404 Not Found


config = {
    "API_URL": os.getenv("API_URL"),
}


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

# Error handling for 500 Internal Server Error


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

# Error handling for other exceptions


@app.errorhandler(Exception)
def generic_error(error):
    return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/env')
def get_config():
    return jsonify(config)


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = Userdetails.query.all()

        user_list = []
        for user in users:
            user_data = {'id': user.id, 'firstName': user.firstName, 'lastName': user.lastName,
                         'email': user.email, 'age': user.age}
            user_list.append(user_data)
        return render_template('users.html', users=users)

        # return jsonify({'users': user_list}), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/create_user', methods=['GET'])
def create_user_page():
    return render_template('create_user.html')


@app.route('/update_user/<int:user_id>', methods=['GET'])
def update_user_page(user_id):
    return render_template('update_user.html', user_id=user_id)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    try:
        user = Userdetails.query.get_or_404(user_id)

        user_data = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'age': user.age
        }

        return jsonify({'user': user_data}), 200

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/users', methods=['POST'])
def create_ct_account():
    try:
        data = request.get_json()

        required_fields = ['firstName', 'lastName', 'email', 'age', 'password']
        if not all(field in data for field in required_fields):
            raise ValueError('Missing required fields')

        hashed_password = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')

        new_user = Userdetails(
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            age=data.get('age'),
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except ValueError as ve:
        app.logger.error(f"Validation error: {str(ve)}")
        return jsonify({'error': 'Bad Request'}), 400

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        user = Userdetails.query.get_or_404(user_id)

        # Update user fields
        user.firstName = data.get('firstName', user.firstName)
        user.lastName = data.get('lastName', user.lastName)
        user.email = data.get('email', user.email)
        user.age = data.get('age', user.age)

        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = Userdetails.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
