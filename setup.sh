#!/bin/bash

# download chromedriver for mac/arm64
wget https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.88/mac-arm64/chromedriver-mac-arm64.zip
unzip chromedriver-mac-arm64.zip
mv chromedriver-mac-arm64/chromedriver .
rm -rf chromedriver-mac-arm64*
