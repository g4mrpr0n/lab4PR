import socket
import signal
import sys
import threading
import json
from time import sleep
# Define the server's IP address and port
HOST = '127.0.0.1' # IP address to bind to (localhost)
PORT = 8080 # Port to listen on
# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen(5) # Increased backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")


# Function to handle client requests
def handle_request(client_socket):
    data = {}
# Read the JSON file
    with open('books.json', 'r') as file:
        data = json.load(file)


    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")
    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]  # Get the HTTP method
    path = request_line[1]    # Get the requested path

    # Initialize the response content and status code
    response_content = ''
    status_code = 200

    # Define a simple routing mechanism
    if method == 'GET':
        if path == '/home':
            sleep(15)
            response_content = 'This is the main page.'
        elif path == '/about':
            response_content = 'About us: we sell nice books!'
        elif path == '/contact':
            response_content = 'Message us at emailtobookstore@gmail.com!<br>Contact number: 0123456789'
        elif path == '/books':
            responsetosend = ''
            for books in range(1, 3):
                # Retrieve information based on the book number
                book_info = data[str(books)]
                
                responsetosend = responsetosend + f'Book #{str(books)}: <a href="/book-items/{str(books)}"> {book_info["name"]}</a>  <br>'
            response_content = responsetosend
        elif path.startswith('/book-items/'):
            # Extract the book number from the path
            book_number = path[len('/book-items/'):]
            # Check if the book number exists in the 'data' dictionary
            if book_number in data:
                book_info = data[book_number]
                response_content = f'<h2>"name" : {book_info["name"]} <br> "author" : {book_info["author"]} <br> "price" : {book_info["price"]} <br> "description" : {book_info["description"]} </h2>'
            else:
                response_content = 'Book not found'
        else:
            response_content = '404 Not Found'
            status_code = 404
    else:
        response_content = '405 Method Not Allowed'
        status_code = 405

    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    # Close the client socket
    client_socket.close()


def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)
    # Register the signal handler


signal.signal(signal.SIGINT, signal_handler)
while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    # Create a thread to handle the client's request
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()