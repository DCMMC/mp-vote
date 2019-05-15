#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
env QT_QPA_PLATFORM="" node $SHELL_FOLDER/shoot.js $1 $2
