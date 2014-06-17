clear
# Check if the python script was already running, terminate it
processId=$(ps axf | ack python3 | ack main.py | ack ../bachelorThesis/results/ | ack -v ack | ack  "^([\d]*)"  --output=\$1)
kill $processId > /dev/null 2>&1
python3 main.py ../bachelorThesis/results/ &
