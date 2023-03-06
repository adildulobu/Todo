from typing import List
from ninja import NinjaAPI
from todo.models import Todo
from todo.schema import TodoSchema, NotFoundSchema


api = NinjaAPI()

@api.get("/todos", response=List[TodoSchema])
def todos(request):
    return Todo.objects.all()

@api.get("/todos/{todo_id}", response={200: TodoSchema})
def todo(request, todo_id: int):
    try:
        todo = Todo.objects.get(pk=todo_id)
        return 200, todo
    except Todo.DoesNotExist as e:
        return 404, {"message": "This to do does not exist"}

@api.post("/todos", response={201: TodoSchema})
def create_todo(request, todo: TodoSchema):
    todo = Todo.objects.create(**todo.dict())
    return todo

@api.put("/todos/{todo_id}", response={200: TodoSchema, 404: NotFoundSchema})
def change_todo(request, todo_id: int, data: TodoSchema):
    try:
        todo = Todo.objects.get(pk=todo_id)
        for attribute, value in data.dict().items():
            setattr(todo, attribute, value)
        todo.save()
        return 200, todo
    except Todo.DoesNotExist as e:
        return 404, {"message": "This to do does not exist"}

@api.delete("/todos/{todo_id}", response={200: None})
def delete_todo(request, todo_id: int):
    try:
        todo = Todo.objects.get(pk=todo_id)
        todo.delete()
        return 200
    except Todo.DoesNotExist as e:
        return 404, {"message": "This to do does not exist"}
