from ninja import Schema

class TodoSchema(Schema):
    name: str


class NotFoundSchema(Schema):
    message: str