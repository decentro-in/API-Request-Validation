from flask import Flask, request
from marshmallow import ValidationError
from UserProfileSchema import UserProfile

app = Flask(__name__)

@app.route("/", methods=['POST'])
def add_user_profile():
    try:
        request_body = request.get_json()
        schema = UserProfile()
        validated_request   = schema.load(request_body)
        transformed_request = schema.dump(validated_request)

        return {
            "message" : "User created successfully.",
            "transformed_data" : transformed_request
        }

    except ValidationError as err:
        request_errors = err.messages
        return {
            "error": request_errors
        }, 400
    except Exception as err:
        return {
            "error": "Something went wrong."
        }, 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port="5000"
    )