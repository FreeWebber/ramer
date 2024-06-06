# RAMer - cli app to free up RAM memory for GNU/Linux distros

### Description
On launch RAMer start monitoring memory, and if it low - start killing programs that defined for killing
For example, if list will be `discord,/code/code,brave/brave,brave-beta,sublime_text`, than RAMer kill `Discord` for first, than `Visual Studio Code`, than `Brave`, than `Brave Beta`, etc

### Show processes list
./ramer.py --processes 1

### Dependencies install for Ubuntu 22.04

pip3 install print-position
pip3 install psutil

if you want launch w/ sudo, you need install packages under root

### Launch w/ drop_caches

sudo ./ramer.py

### Launch w/o drop_caches

./ramer.py

For debug:

add options --showlog 1

### Options

To see options launch ./ramer.py -h

Example w/ custom priority list: `./ramer.py --showlog 1 --sound 1 --priority discord,/code/code,brave`

### LICENSE

See LICENSE.txt file