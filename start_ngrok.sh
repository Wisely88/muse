#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

killall -9 ngrok 2>/dev/null
sleep 1

/opt/homebrew/bin/ngrok http 8080 --log=stdout > ngrok.log 2>&1
