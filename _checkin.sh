#!/bin/bash
if [[ "$1" == "" ]]; then
  echo
  echo "Usage: $0 <commit-comment>"
  echo
  exit -1
fi
mv chromedriver ..
git add .
git commit -m "$1"
git push origin main
mv ../chromedriver .
