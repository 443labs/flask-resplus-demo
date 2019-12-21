import uuid

from flask_restplus_patched import Parameters, ModelSchema, Schema
from marshmallow import fields, post_load

from egl.db.models.user import User


###############################################################################
# Pagination
###############################################################################


class Page:
    def __init__(self, **kwargs):
        self.page = kwargs.get('page', 1)
        self.per_page = kwargs.get('per_page', 25)
        self.total = kwargs.get('total', 0)


class PageItems(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = kwargs.get('items', {})


class PageSchema(Parameters):
    page = fields.Int(required=False, default=1, missing=1, example=1)
    per_page = fields.Int(required=False, default=25, missing=25, example=25)
    total = fields.Int(required=False, default=0, missing=0, example=0)

    @post_load
    def deserialize(self, data):
        return Page(**data)


class PagingParameters:
    def __init__(self, page=1, per_page=25):
        self.page = page
        self.per_page = per_page


class PagingParametersSchema(Parameters):
    page = fields.Int(required=False, default=1, missing=1, example=1)
    per_page = fields.Int(required=False, default=25, missing=25, example=25)

    @post_load
    def deserialize(self, data):
        return PagingParameters(**data)

###############################################################################
# Users
###############################################################################


class NewUserSchema(Parameters):
    id = fields.UUID(required=False, example='fa9fd558-94f4-4fc6-a4dd-1b17b6bfd161')
    email = fields.String(example='minion@egl.org')
    meta = fields.Raw(example={})

    @post_load
    def deserialize(self, data):
        return User(**data)


# class UserSchema(ModelSchema):
#     class Meta:
#         model = User
#         # strict = True
#         exclude = ['password']

class UserSchema(Parameters):
    id = fields.UUID(required=False)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)
    email = fields.String()
    password = fields.String(load_only=True)
    meta = fields.Raw(example={})
    active = fields.Boolean()
    is_system_user = fields.Boolean()

    @post_load
    def deserialize(self, data):
        # Inheriting from ModelSchema doesn't appear to fire the @post_load decorator.
        # I'm not sure it matters, but I did think that worked. Haven't been in front of this code for a minute though.
        # It was nice because you theoretically have already defined your schema in your sql alchemy model class...
        return User(**data)


# alternatively you could inherit that schema and blacklist fields you don't want
class CurrentUserSchema(UserSchema):
    class Meta:
        exclude = ['password']


class UserPageSchema(PageSchema):
    items = fields.Nested(UserSchema, many=True)

    @post_load
    def deserialize(self, data):
        return PageItems(**data)


class Login:
    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')


class LoginSchema(Parameters):
    email = fields.String(required=True, example='minion@egl.org')
    password = fields.String(required=True, example='abc123')

    @post_load
    def deserialize(self, data):
        return Login(**data)
