#/usr/bin/env/sh
set -e

echo "Testing Python 2.x projects..."
python2 -m pip install pylint

tasks=("declarator.org" "income_declaration")

for task in ${tasks[@]}; do
    echo "Testing: $task"
    find $task -iname "*.py" | xargs python2 -m pylint --rcfile="tests/pylintrc"
done;