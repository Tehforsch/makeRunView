clear
# Check if the python script was already running, terminate it
processId=$(ps axf | ack python3.4 | ack main.py | ack example | ack -v ack | ack  "^([\s]*[\d]*)"  --output=\$1)
kill $processId > /dev/null 2>&1
python3.4 -B main.py -v example & 
