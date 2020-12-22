#!/bin/bash

set -e
errors=0

# Run unit tests
python umitrans/umitrans_test.py || {
    echo "'python python/umitrans/umitrans_test.py' failed"
    let errors+=1
}

# Check program style
pylint -E umitrans/*.py || {
    echo 'pylint -E umitrans/*.py failed'
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"
