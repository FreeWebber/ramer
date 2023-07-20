# RAMer - cli app to free up RAM memory
### Description
On launch RAMer start monitoring memory, and if it low - start killing programs that defined for killing
For example, if list will be `discord,/code/code,brave/brave,brave-beta,sublime_text`, than RAMer kill `Discord` for first, than `Visual Studio Code`, than `Brave`, than `Brave Beta`, etc

### Show processes list
./ramer.py --processes 1

### Dependencies install for Ubuntu 22.04

pip3 install psutil

### Launch

./ramer.py

  ### Options
  ```
./ramer.py -h
-h, --help show this help message and exit
--limit [LIMIT] set limit of minimum free memory since start killing programs, megabytes, default 500, always >100
--intval [INTVAL] set interval in seconds, default 10
--sound [SOUND] 1 for play sound on killing process
--showlog [SHOWLOG] 1 for showing log
--priority [PRIORITY]
set penultimate part of name of cli proccess that must be killed in case the lack of RAM. The longer string the better for
definition. Must be divded by comma, ex: discord,/code/code,brave/brave,brave-beta,sublime_text
Default list: `discord,/code/code,brave/brave,brave-beta,sublime_text`
--processes [PROCESSES]
for showing names for creating list of processes that must be killed
--kill [KILL] kill process?, default 1
```
Example: `./ramer.py --showlog 1 --priority discord,/code/code,brave`

### LICENSE

See LICENSE file