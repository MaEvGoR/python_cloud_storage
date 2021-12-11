# Python Cloud Storage

Homework assignment for Distributed File Systems course

## General information

There are 3 nodes:
* client node (x2)
* name node
* storage node (x2)

All nodes run on virtual machine and communicate via sockets.
There are 2 users (*client* node), 1 name node, and 2 data nodes.

## Client Node

There are commands that can be executed from **client node**.
See **handbook for users** below.
It connect to **name node** that always hold connection oppened. Client does connection each time, when we run the script.

### What happens in client_send.py?


1. It run the python script and receive command_name and arguments as file/dir name(if needed) and path (if needed), or FILE.
2. Then it send *command_id* and *arguments* to **name_node** via socket.
3. When **name_node** run needed command by itself or with **data_node**(storage), it send back response informatoin that was asked or message as “*command_name* was successfully executed”
4. After that, client will print and observe the response.

### About users

There are can be several users on the *client node*. They all can connect to the *name node* and run commands on the file system and get access to the same file. According to the specification of our project, maximum number of users are 2, but can be increased easily.

## Name Node

There are two main parts in the namenode implementation. First part is the connection between clients and namenode and second one is connection between namenode and datanode.

The main idea is that in **name node** connection for users are always open. When **client** run the command, **name node** receive command id and run the function and send response.

Connection between namenode and all datanodes is established at the start of the script before the main loop.

In main loop mamenode waits for the connection from clients. When it gets the command, it check every datanode to get information about alive nodes. When namenode resolves command from client and send required instructions only to alive datanodes. After this it tries to accept connection from datanodes that were dead, but already burn from hell. If there is some, namenodes asks already lived datanodes to restore birthded one.

### What happens in name_node.py?

In the very beginning python script will be run. It will open and hold socket to communicate with **client_node** (*in order to receive commands and send response*) and with **data_node** (*to perform operations on files and directories*)


1. **Name node** receive *command_id* and *arguments* from client (file / dir name or file).
2. It runs one of the functions according on id. Function will be done only in **name node**, if there are operations only on hirerarchical tree of directories, and on **data node** otherwise.
3. After that, it send response to the client information that was asked, or “*command id* was executed”, or file.

## Data node

At the start of the script datanode creates its own socket for namenode connection. After this it starts infinite loop for namenode commands. When datanode recieve command from namenode it performs required actions.

### Restore

There is also possiblity, that namenode send command to restore other datanode. It ask datanode to restore required files on datanode which IP datanode will send with message. It will be performed with *scp* command. 

### What happens in data_node.py?

In the very beginning python script will be executed. It will open and hold socket to communicate with namenode (in order to receive commands).


## Handbook for user

**Commands will be called in the terminal as following**

```bash
python3 client_send.py command_name argument1(if exist) argument2(if exists)
```

* *command id* - id of the command (number)
* *command_name* - how command should be called in the terminal
* *argument1&2* - additional info
* *Response* - what we got as response from name node when we call the command

**Initialize**. Initialize the client storage on a new system, should remove any existing file in the dfs root directory and return available size.

* *command_id*: 0
* *command_name*: initialize
* *argument1*: -
* *argument2*: -
* *Response*: text - available size

**File create**. Should allow to create a new empty file.

* *command_id*: 1
* *command_name:* file_create
* *argument1:* file name
* *argument2:* - 
* *Response*: ok

**File read**. Should allow to read any file from DFS (download a file from the DFS to the Client side).
* *command_id:* 2
* *command_name*: file_read
* *argument1*: file name
* *argument2*: -
* *Response:* FILE

**File write**. Should allow to put any file to DFS (upload a file from the Client side to the DFS)
* *command_id:* 3
* *command_name*: file_write
* *argument1*: FILE
* *argument2*: -
* *Response:* ok

**File delete**. Should allow to delete any file from DFS 
* *command_id*: 4
* *command_name:* file_delete
* *argument1:* file name
* *argument2:* -
* *Response*: ok

**File info**. Should provide information about the file (any useful information - size, node id, etc.)
* *command_id:* 5
* *command_name*: file_info
* *argument1*: file name
* *argument2*: -
* *Response:* text - info

**File copy**. Should allow to create a copy of file. 
* *command_id*: 6
* *command_name:* file_copy
* *argument1:* file name
* *argument2:* - 
* *Response*: ok

**File move**. Should allow to move a file to the specified path. 
* *command_id*: 7
* *command_name:* file_move
* *argument1:* file name
* *argument2:* path
* *Response*: ok

**Open directory**. Should allow to change directory
* *command_id*: 8
* *command_name:* open_directory
* *argument1*: dir name use ‘...’ to go back
* *argument2*: -
* *Response:* ok

**Read directory**. Should return list of files, which are stored in the directory. 
* *command_id*: 9
* *command_name:* read_directory
* *argument1:* dir name
* *argument2:* -
* *Response:* text - list of files

**Make directory**. Should allow to create a new directory. 
* *command_id*: 10
* *command_name:* make_directory
* *argument1:* dir name
* *argument2:* - 
* *Response*: ok

**Delete directory**. Should allow to delete directory. If the directory contains files the system should ask for confirmation from the user before deletion. 
> need (yes/no) confirmation if there are files in the directory
* *command_id:* 11
* *command_name:* delete_directory 
* *argument1*: dir name
* *argument2:* -
* *Response:* ok
