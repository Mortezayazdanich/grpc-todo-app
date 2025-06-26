Simple To-Do List with gRPC Backend and Flask Frontend
This project is a simple yet full-featured To-Do list application built with a modern microservice-style architecture. It demonstrates the separation of concerns between a backend service that handles business logic and database interactions, and a frontend that serves as the user interface.

The backend is a high-performance gRPC service written in Python that exposes methods for creating, retrieving, updating, and deleting to-do items. The frontend is a lightweight Flask web application that communicates with the gRPC service, providing a clean and simple web interface for the user.

✨ Key Features
Create: Add new to-do items.
Read: View all existing to-do items.
Update: Mark items as complete.
Delete: Remove items from the list.
Decoupled Architecture: The frontend and backend are independent services, communicating over a well-defined gRPC contract.
🏗️ Architecture
The application is split into two main components that run as separate processes, communicating over the network via gRPC.

Flask Frontend: A simple web server responsible for rendering the HTML page and translating user actions (button clicks) into gRPC calls to the backend. It does not interact with the database directly.
gRPC Backend: The "brains" of the operation. It implements the service logic defined in the .proto file and is solely responsible for all database operations using SQLAlchemy and SQLite.
🔧 Tech Stack
Backend: Python, gRPC, SQLAlchemy
Frontend: Flask
Database: SQLite
API Definition: Protocol Buffers (.proto)
Tooling: Git, Python Virtual Environment
🚀 Getting Started
