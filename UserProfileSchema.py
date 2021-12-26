import datetime
from marshmallow import Schema, fields, validate, validates_schema, pre_load, ValidationError

def resolve_pincode(pincode: str, resolve_to:str):
    """Dummy method to resolve pincode"""
    if resolve_to == 'area':
        return "Indira Nagar"

    if resolve_to == "city":
        return "Bengaluru"

    if resolve_to == "state":
        return "Karnataka"

    raise RuntimeError("Not able to resolve pincode")

def check_pincode(pincode: str):
    """Dummy method to validate pincode"""
    return True

class Name(Schema):
    first  = fields.String(required=True)
    middle = fields.String()
    last   = fields.String(required=True)

class NameWithSalutation(Name):
    salutation = fields.String(required=True)

class Address(Schema):

    flat_number = fields.String(required=True)
    locality    = fields.String(required=True)
    landmark    = fields.String()
    pincode     = fields.String(
        required=True,
        # Explicitly writing the REGEX validation rules.
        validate=validate.Regexp(
            regex="^[1-9][0-9]{5}$"
        )
    )

    # This fields will be resolved from the pincode.
    area        = fields.Method('pincode_to_area')
    city        = fields.Method('pincode_to_city')
    state       = fields.Method('pincode_to_state')

    # We will be writing these functions inside the same schema class
    # with the name mentioned in the respective parameters

    def pincode_to_area(self, obj):

        # In case pincode is not provided.
        # whole validation block is run irrespective of single
        # mismatch. That's why this check should be there.
        pincode = obj.get('pincode')
        if not pincode:
            return

        # calling external lookups to fetch the area and returning it
        # resolve pincode is external lookup method
        area = resolve_pincode(pincode, 'area')

        return area or ''

    # Building other methods in a similar way
    def pincode_to_city(self, obj):
        pincode = obj.get('pincode')
        if not pincode:
            return

        city = resolve_pincode(pincode, 'city')
        return city or ''

    def pincode_to_state(self, obj):
        pincode = obj.get('pincode')
        if not pincode:
            return

        state = resolve_pincode(pincode, 'state')
        return state or ''

    """
    We can even add custom validations, which can validate one
    or multiple parameters on custom logics

    Let's validates the pincode against our lookup
    If there pincode not found in our lookup, we will
    be raising a validation error.
    """
    @validates_schema
    def validate_pincode(self, obj, **kwargs):

        pincode = obj.get('pincode')

        # No proceeding further if get
        if not isinstance(pincode, str):
            return

        # Calling cutom method to check pincode against lookup
        if not check_pincode(pincode):
            err = {
                "pincode": [
                    "Please provide a valid pincode."
                ]
            }
            raise ValidationError(err)



class EachSocialPresence(Schema):
    site_name = fields.String(requried=True)
    site_url  = fields.String(required=True)


class UserProfile(Schema):

    # This is how we link the sub-schemas
    name            = fields.Nested(Name, required=True)
    date_of_birth   = fields.Date(
        format="%Y-%m-%d",
        # We can also give custom error messages
        # As in this case we want to specify the format
        error_messages = {
            "invalid": "Invalid date provided. Valid format: yyyy-mm-dd."
        },
        required=True
    )

    # This is how we handle categorical fields
    gender          = fields.Str(
        validate=validate.OneOf(
            ["M", "F", "O"],
            ["Male", "Female", "Others"]
        )
    )

    address         = fields.Nested(Address, required=True)
    social_presence = fields.List(fields.Nested(EachSocialPresence))

    # In this method we only validate the date_of_birth for the
    # future date
    @validates_schema
    def check_future_date(self, obj, **kwargs):
        date_of_birth = obj.get('date_of_birth')

        if not date_of_birth:
            return

        if date_of_birth > datetime.date.today():

            # We need to build the error body in this way
            err = {
                "date_of_birth" : [
                    "Future dates are not acceptable."
                ]
            }

            # And then need to pass the err dict in the validation
            # exception class provided by marshmallow
            raise ValidationError(err)

    @pre_load
    def uppercase_params(self, data, **kwargs):
        """
        Before the schema is loaded we can uppercase the categorical variable
        So as not to reject the request because they are just case-sensitive.
        """

        # This is raw input we need to deal with it carefully.
        gender = data.get('gender')
        if isinstance(gender, str):
            data['gender'] = gender.capitalize()

        return data