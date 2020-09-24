#!/bin/bash

image_in_hub() {
  echo "Checking in dockerhub for $1"
  echo "Running docker pull $1"
  pull=$(env LANG=C docker pull --quiet "$1" 2>&1 1> /dev/null)
  pull_result=$?
  if test ${pull_result} -eq 0; then
    echo "IN DOCKERHUB"
    return 0
  elif echo "${pull}" | grep -q 'manifest unknown'; then
    echo "NOT IN DOCKERHUB"
    return 1
  else
    echo "UNKNOWN: ${pull}"
    return 2
  fi;
}

image_in_hub "$1"
RC=$?
if test ${RC} -eq 0; then
  echo "No hago nada"
elif test ${RC} -eq 1; then
  echo "Toca hacer tag y push"
else
  echo "Condicion no gestionada"
fi;
