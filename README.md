# Concurrency and Parallelism

> Distributed and Networking Programming

## what this code about 

1. A multi-threaded TCP server that communicates with a client.

## Server Implementation


1. Accept a new connection from a client.
2. Spawn a new thread to handle the connection.
3. Generate a list of `250000` random numbers ranging between `-999999999` and `999999999`.
4. Create a string containing the numbers separated by commas.
5. Send the list to the connected client, then close that connection.

> **Note**: the string shouldn't contain any whitespaces.

Additional info :

- The server stay listening all the time and should not terminate unless a `KeyboardInterrupt` is received.
- The server is able to handle multiple connections simultaneously.
- The server socket is marked for address reuse so that the OS would immediately release the bound address after server termination. You can do so by calling the `setsockopt` on the server socket before binding the address as follows:
  ```python
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((SERVER_IP, SERVER_PORT))
  ```

## Client Implementation

The client does the following:
 
1. Connect to the TCP server multiple times to download 100 unsorted lists, one by one.
2. Write each unsorted list into a `.txt` file in a directory called `unsorted_files` (creating the directory if it does not exist).
3. Sort each unsorted list and writes it into a `.txt` file in a directory called `sorted_files` (creating the directory if it does not exist).
4. Use [time](https://docs.python.org/3/library/time.html) module to calculate the total time taken for unsorted lists download and sorting files.


## Example Run

```bash
$ python3 NameSurname_server.py
Listening on 0.0.0.0:12345
Sent a file to ('127.0.0.1', 48168)
Sent a file to ('127.0.0.1', 48174)
...etc

# Before optimizing client
$ python3 client.py
Files download time: 44.49141001701355
Sorting time: 14.114730834960938

# After optimizing client
$ python3 NameSurname_client.py
Files download time: 29.626671075820923
Sorting time: 7.460468053817749
```
