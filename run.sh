#!/bin/bash

set -euo pipefail


Help()
{
   # Display Help
   echo "Runs the specified kind of tests or the service"
   echo
   echo "Syntax: [main | unit | integration | smoke | help]"
   echo "options:"
   echo "main           Runs the app by invoking main.py"
   echo "unit           Runs unit test"
   echo "integration    Runs integration test"
   echo "smoke          Runs smoke test"
   echo "help           Print this help"
   echo
}

case ${1:-} in
    main)
    echo "Running application..."
    source .env
    export PYTHONPATH=$(pwd)
    poetry run python main.py
    
    ;;

    unit)
    echo "Running unit tests..."
    export PYTHONPATH=$(pwd)
    poetry run pytest --mypy tests/
    
    ;;
    
    smoke|integration)
    echo "The tests have not been implemented yet"
    ;;

    help)
    Help
    ;;

    *)
    echo "Please provide a valid command."
    Help
    ;;
esac