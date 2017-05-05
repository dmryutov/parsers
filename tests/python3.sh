#/usr/bin/env/sh
set -e

echo "Testing Python 3.x projects..."
python3 -m pip install pylint
python3 -m pip install lxml
python3 -m pip install selenium
python3 -m pip install dryscrape

tasks=("bsr.sudrf.ru/selenium" "bsr.sudrf.ru/dryscrape")

for task in ${tasks[@]}; do
    echo "Testing: $task"
    find $task -iname "*.py" | xargs python3 -m pylint --rcfile="tests/pylintrc"
done;