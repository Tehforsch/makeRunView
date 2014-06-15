clear
# Check if the python script was already running, terminate it
processId=$(ps axf | ack python3 | ack main.py | ack example | ack -v ack | ack  "^([\d]*)"  --output=\$1)
echo "Killing $processId"
kill $processId
echo "-----------------------"
python3 main.py example &
echo "-----------------------"
