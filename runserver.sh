#!/bin/bash
source djenv/bin/activate
cd djbotapp
daphne -p 8000 djbotapp.asgi:application
