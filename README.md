# python_cloud_storage

### Handbook for user:
#### Commands will be called in the terminal as following
python3 client_send.py command_name argument1(if exist) argument2(if exist)
*command id* - id of the command (number)
*command_name* - how command should be called in the terminal
*argument1&2* - additional info
*Response* - what we got as response from name node when we call the command 

Initialize. Initialize the client storage on a new system, should remove any existing file in the dfs root directory and return available size.
$\quad$*command_id*: 0
$\quad$*command_name*: initialize
$\quad$*argument1*: -
$\quad$*argument2*: -
$\quad$*Response*: text - available size

File create. Should allow to create a new empty file.
$\quad$*command_id*: 1
$\quad$*command_name*: file_create
$\quad$*argument1*: file name
$\quad$*argument2*: -
$\quad$*Response*: ok

File read. Should allow to read any file from DFS (download a file from the DFS to the Client side).
$\quad$*command_id*: 2
$\quad$*command_name*: file_read
$\quad$*argument1*: file name
$\quad$*argument2*: -
$\quad$*Response*: FILE

File write. Should allow to put any file to DFS (upload a file from the Client side to the DFS)
$\quad$*command_id*: 3
$\quad$*command_name*: file_write
$\quad$*argument1*: FILE
$\quad$*argument2*: -
$\quad$*Response*: ok

File delete. Should allow to delete any file from DFS
$\quad$*command_id*: 4
$\quad$*command_name*: file_delete
$\quad$*argument1*: file name 
$\quad$*argument2*: -
$\quad$*Response*: ok

File info. Should provide information about the file (any useful information - size, node id, etc.)
$\quad$*command_id*: 5
$\quad$*command_name*: file_info
$\quad$*argument1*: file name
$\quad$*argument2*: -
$\quad$*Response*: text - info 

File copy. Should allow to create a copy of file.
$\quad$*command_id*: 6
$\quad$*command_name*: file_copy
$\quad$*argument1*: file name
$\quad$*argument2*: -
$\quad$*Response*: ok

File move. Should allow to move a file to the specified path.
$\quad$*command_id*: 7
$\quad$*command_name*: file_move
$\quad$*argument1*: file name
$\quad$*argument2*: path 
$\quad$*Response*: ok

Open directory. Should allow to change directory
*command_id*: 8
$\quad$*command_name*: open_directory
$\quad$*argument1*: dir name use '..' to go back
$\quad$*argument2*: -
$\quad$*Response*: ok

Read directory. Should return list of files, which are stored in the directory.
$\quad$*command_id*: 9
$\quad$*command_name*: read_directory
$\quad$*argument1*: dir name 
$\quad$*argument2*: -
$\quad$*Response*: text - list of files

Make directory. Should allow to create a new directory.
$\quad$*command_id*: 10
$\quad$*command_name*: make_directory
$\quad$*argument1*: dir name
$\quad$*argument2*: -
$\quad$*Response*: ok

Delete directory. Should allow to delete directory.  If the directory contains files the system should ask for confirmation from the user before deletion.
> need  (yes/no) confirmation if there are files in the directory

$\quad$*command_id*: 11
$\quad$*command_name*: delete_directory
$\quad$*argument1*: dir name
$\quad$*argument2*: -
$\quad$*Response*: ok
