#!/bin/zsh

echo "$1" | sed "s|^Document : \(/.*\)$|file://\1|g"

