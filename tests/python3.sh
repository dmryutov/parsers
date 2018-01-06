#/usr/bin/env/sh
set -e

echo "Testing Python 3.x projects..."
sudo apt-get remove python3-pip
sudo apt-get install python3
sudo apt-get install python3-pip
sudo python3 -m pip install pylint
sudo python3 -m pip install lxml
sudo python3 -m pip install selenium
sudo python3 -m pip install dryscrape

tasks=("bsr.sudrf.ru/selenium" "bsr.sudrf.ru/dryscrape" "bulgarian_declaration")

for task in ${tasks[@]}; do
    echo "Testing: $task"
    find $task -iname "*.py" | xargs python3 -m pylint --rcfile="tests/pylintrc"
done;