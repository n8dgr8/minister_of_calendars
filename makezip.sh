#!/usr/bin/env bash

pushd ~/.virtualenvs/minister_of_calendars/lib/python2.7/site-packages
zip -ur ~/src/minister_of_calendars/minister_of_calendars.zip .

popd
zip -u minister_of_calendars.zip minister_of_calendars.py SatStalkerPredictor.json
