# ADSB Dashboard

This is a Python Django webapp that displays a dashboard of received
ADSB data from PiAware running on a Raspberry Pi.

# Running locally

This dashboard requires the following:

- PiAware (or similar dum1090) running on your network and receiving ADSB signals
- dump1090kafkaproducer running locally, consuming the feed on port 30003
from PiAware

Configure dump1090kafkaproducer to POST data to adbs-dashboard by changing
app.properties:

`runmode=rest`

Start dump1090kafkaproducer locally, consuming from PiAware's port 30003 with:

`nc piaware.local 30003 | java -jar target/dump1090-kafkaproducer-0.0.1-SNAPSHOT-jar-with-dependencies.jar`

Start up adsb-dashboard locally. with `./run-dev-server.sh`

dump1090kafkaproducer will post parsed ADBS messages into adsb-dasboard which
stores them in a local Postres db.

Work in progress.
