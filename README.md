# A simplified client-server solution for file management - Applied Python Programming
 This repo contains source code of project A simplified client-server solution for file management  done using Python Programming

# File Management System
This project is a client-server application designed to handle file management tasks. The server is capable of handling multiple clients, each with their own directory and files inaccessible to other users. It supports a subset of commands similar to those found in UNIX-based systems. The client allows users to interact with the server by issuing commands and receiving responses.

# Server Features
+ Multiple Clients: The server can handle multiple clients connecting simultaneously.
+ User Authentication: Users can register and log in with unique usernames and passwords.
+ Directory Management: Users can navigate through directories, create new folders, and view files.
+ File Operations: Users can read from, write to, and create files within their directory.
+ Error Handling: Proper error messages are returned for invalid commands or operations.

# Client Features
+ User Interface: The client provides a simple interface for users to register, log in, and issue commands.
+ Command History: The client logs all commands issued by each user.
+ Built-in Commands: Users can view available commands and quit the application easily.

# Testing and Error Handling
+ Unit Tests: Tests are implemented using assertions, as well as the unittest module, to ensure code correctness.
+ Test Report: A comprehensive test report is provided, explaining the rationale behind the tests and areas covered.
