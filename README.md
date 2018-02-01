# telldus-mqtt
Telldus Live! to MQTT

## Installation

Clone this repository and make a production configuration file

```
$ clone https://github.com/xibriz/telldus-mqtt.git
$ cd telldus-mqtt/
$ sudo pip install -r requirements.txr
$ cp config/default.cfg config/prod.cfg
```

Change all the FIXME values in `config/prod.cfg`

Change the `WorkingDirectory` in `telldus-mqtt.service`

Copy the service file to the system-folder and enable the service

```
$ sudo cp telldus-mqtt.service /etc/systemd/service/
$ sudo systemctl enable telldus-mqtt.service
$ sudo systemctl start telldus-mqtt.service
```

## Test

From a MQTT-client:

Get status from light
` $ mosquitto_pub -t 'telldus/{light_name}/status' -m '' `

Dim light to 40%
` $ mosquitto_pub -t 'telldus/{light_name}/set' -m '40' `

Turn off light
` $ mosquitto_pub -t 'telldus/{light_name}/set' -m 'OFF' `

Turn on light
` $ mosquitto_pub -t 'telldus/{light_name}/set' -m 'ON' `


Note that the `{light_name}` is the defined names in Telldus Live! without spaces but case sensitive.
