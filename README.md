# python_cloud_storage

Handbook for user:
 Comment

Commands will be called in the terminal as following

python3 client_send.py command_name argument1(if exist) argument2(if exist)
command id - id of the command (number)
command_name - how command should be called in the terminal
argument1&2 - additional info
Response - what we got as response from name node when we call the command

Initialize. Initialize the client storage on a new system, should remove any existing file in the dfs root directory and return available size.
command_id: 0
command_name: initialize
argument1: -
argument2: -
Response: text - available size

File create. Should allow to create a new empty file.
command_id: 1
command_name: file_create
argument1: file name
argument2: -
Response: ok

File read. Should allow to read any file from DFS (download a file from the DFS to the Client side).
command_id: 2
command_name: file_read
argument1: file name
argument2: -
Response: FILE

File write. Should allow to put any file to DFS (upload a file from the Client side to the DFS)
command_id: 3
command_name: file_write
argument1: FILE
argument2: -
Response: ok

File delete. Should allow to delete any file from DFS
command_id: 4
command_name: file_delete
argument1: file name
argument2: -
Response: ok

File info. Should provide information about the file (any useful information - size, node id, etc.)
command_id: 5
command_name: file_info
argument1: file name
argument2: -
Response: text - info

File copy. Should allow to create a copy of file.
command_id: 6
command_name: file_copy
argument1: file name
argument2: -
Response: ok

File move. Should allow to move a file to the specified path.
command_id: 7
command_name: file_move
argument1: file name
argument2: path
Response: ok

Open directory. Should allow to change directory
command_id: 8
command_name: open_directory
argument1: dir name use ‘…’ to go back
argument2: -
Response: ok

Read directory. Should return list of files, which are stored in the directory.
command_id: 9
command_name: read_directory
argument1: dir name
argument2: -
Response: text - list of files

Make directory. Should allow to create a new directory.
command_id: 10
command_name: make_directory
argument1: dir name
argument2: -
Response: ok

Delete directory. Should allow to delete directory. If the directory contains files the system should ask for confirmation from the user before deletion.

need (yes/no) confirmation if there are files in the directory
command_id: 11
command_name: delete_directory
argument1: dir name
argument2: -
Response: ok
