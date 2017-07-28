#!/bin/bash

if [ "$DEPLOY" = "" ]
then
   python main.py runserver

else
   python main.py createdb "$SENHA"
fi
