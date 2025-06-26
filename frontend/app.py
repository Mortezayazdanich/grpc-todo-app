# frontend/app.py

import grpc
from flask import Flask, render_template, request, redirect, url_for

# Import the generated gRPC files
# Note: You might need to adjust the import path depending on your project structure.
# If your proto files are in a 'protos' directory at the root,
# and you run flask from the root, you might need to add the root to sys.path.
# For simplicity, we assume the generated files are accessible.
import todo_pb2
import todo_pb2_grpc

app = Flask(__name__)

# --- gRPC Client Setup ---
# Create a channel to connect to the gRPC server.
gRPC_channel = grpc.insecure_channel('localhost:50051')
# Create a stub (client) from the generated gRPC code.
gRPC_stub = todo_pb2_grpc.TodoServiceStub(gRPC_channel)

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main page with the list of to-dos."""
    try:
        # Call the GetTodos RPC
        get_todos_request = todo_pb2.GetTodosRequest()
        todos_response = gRPC_stub.GetTodos(get_todos_request)
        return render_template('index.html', todos=todos_response.todos)
    except grpc.RpcError as e:
        # Handle gRPC connection errors
        print(f"Could not connect to gRPC server: {e}")
        return "Error: Could not retrieve To-Do list. Is the backend server running?", 500


@app.route('/add', methods=['POST'])
def add_todo():
    """Adds a new to-do item."""
    title = request.form['title']
    # Call the CreateTodo RPC
    create_request = todo_pb2.CreateTodoRequest(title=title)
    gRPC_stub.CreateTodo(create_request)
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete_todo(todo_id):
    """Marks a to-do item as complete."""
    # Call the UpdateTodo RPC
    update_request = todo_pb2.UpdateTodoRequest(id=todo_id, completed=True)
    gRPC_stub.UpdateTodo(update_request)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    """Deletes a to-do item."""
    # Call the DeleteTodo RPC
    delete_request = todo_pb2.DeleteTodoRequest(id=todo_id)
    gRPC_stub.DeleteTodo(delete_request)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Running on port 5000 to avoid conflict with gRPC's 50051
    app.run(debug=True, port=5000)