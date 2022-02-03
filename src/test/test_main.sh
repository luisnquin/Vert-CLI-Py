sql() {
    psql vert -c $line
}

test() {
    # Categories
    py ./../vert/app.py categories get
    echo -ne 'useful category, or not?' | py ./../vert/app.py categories add
    py ./../vert/app.py categories remove 1 2

    # Core 
    py ./../vert/app.py core version
    py ./../vert/app.py core ping
    # echo -ne '' py ./../vert/app.py core config
    # py ./../vert/app.py core tasker

    # Gen
    echo -ne '1' | py ./../vert/app.py gen py
    rm -r ~/worspace/projects/1
    echo -ne '2' | py ./../vert/app.py gen go
    rm -r ~/worspace/projects/2
    echo -ne '3' | py ./../vert/app.py gen static
    rm -r ~/worspace/projects/3

    # Ideas
    py ./../vert/app.py ideas get
    echo -ne 'aesda' | py ./../vert/app.py ideas add
    py ./../vert/app.py ideas remove 1

    # Tasks
    py ./../vert/app.py tasks get
    # py ./../vert/app.py tasks add
    py ./../vert/app.py tasks clean
    py ./../vert/app.py tasks check 1 2
    py ./../vert/app.py tasks remove 1 2

    # Urls
    py ./../vert/app.py urls get
    echo -ne 'https://github.com' | py ./../vert/app.py urls add
    py ./../vert/app.py urls remove 1

    # Tables
    py ./../vert/app.py tables get
    py ./../vert/app.py tables rebuild
}

while read line; do sql "$line"; done < ./statements.sql

FUNCTION_START="$(date +%s)"
test
FUNCTION_END="$(date +%s)"
sleep 2
echo "All the program commands takes $[ ${FUNCTION_END} - ${FUNCTION_START} ] seconds to run"
