# H<sub>2</sub>O harvesting
This repository contains code and descriptions for a system which controls thermoelectric coolers for condensation-based harvesting of atmospheric water.

## Physical Connections


### Bosch-Sensortec BME280
Temperature, pressure, and relative humidity (RH) are measured using a BME280 digital barometric sensor. The sensor communicates with the raspberry pi using I2C interface. The sensor pins should be connected  as follows:

1. VIN -> 3.3V
2. GND -> ground
3. SCL -> I2C SCL
4. SDA -> I2C SDA


### Hanmatek HM310P DC power supply
The DC power supply is connected to hte raspberry pi through a USB connection which uses the modbus protocol for communication. For communication in Python, the *pymodbus* library is used.