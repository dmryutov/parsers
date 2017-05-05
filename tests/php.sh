#/usr/bin/env/sh
set -e

echo "Testing PHP projects..."
git clone https://github.com/squizlabs/PHP_CodeSniffer.git

tasks=("banki.ru" "cbr.ru" "insur-info.ru")

for task in ${tasks[@]}; do
    echo "Testing: $task"
    find $task -iname "*.php" | xargs php PHP_CodeSniffer/bin/phpcs --standard=PSR2
done;