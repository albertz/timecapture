#!/bin/bash

dir="$(sh "$(dirname "$0")/../get_foregroundterminal_curdir.sh")"

echo "file://$dir"
