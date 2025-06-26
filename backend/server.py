# backend/server.py

from concurrent import futures
import grpc

# Import the generated classes
import todo_pb2
import todo_pb2_grpc

# Import the database components
from .database import SessionLocal, init_db
from . import models

# Create a class that inherits from the generated servicer
class TodoServicer(todo_pb2_grpc.TodoServiceServicer):
    
    def CreateTodo(self, request, context):
        db = SessionLocal()
        try:
            # Create a new Todo item from the request
            new_todo = models.Todo(title=request.title, completed=False)
            db.add(new_todo)
            db.commit()
            db.refresh(new_todo)
            
            # Convert the database object to the protobuf message type
            return todo_pb2.TodoItem(
                id=new_todo.id,
                title=new_todo.title,
                completed=new_todo.completed
            )
        finally:
            db.close()

    def GetTodos(self, request, context):
        db = SessionLocal()
        try:
            todos = db.query(models.Todo).all()
            
            # Convert the list of database objects to a list of protobuf messages
            todo_items = [
                todo_pb2.TodoItem(id=t.id, title=t.title, completed=t.completed) 
                for t in todos
            ]
            return todo_pb2.TodosResponse(todos=todo_items)
        finally:
            db.close()

    def UpdateTodo(self, request, context):
        db = SessionLocal()
        try:
            todo_to_update = db.query(models.Todo).filter(models.Todo.id == request.id).first()
            if todo_to_update is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Todo not found")
                return todo_pb2.TodoItem()

            todo_to_update.completed = request.completed
            db.commit()
            db.refresh(todo_to_update)

            return todo_pb2.TodoItem(
                id=todo_to_update.id, 
                title=todo_to_update.title, 
                completed=todo_to_update.completed
            )
        finally:
            db.close()

    def DeleteTodo(self, request, context):
        db = SessionLocal()
        try:
            todo_to_delete = db.query(models.Todo).filter(models.Todo.id == request.id).first()
            if todo_to_delete is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Todo not found")
                return todo_pb2.Empty()

            db.delete(todo_to_delete)
            db.commit()

            return todo_pb2.Empty()
        finally:
            db.close()

def serve():
    # Initialize the database and create tables
    init_db()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoServicer(), server)
    
    print("gRPC server starting on port 50051...")
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()