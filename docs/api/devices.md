# Device
Supports registering devices.

## Register a new device

**Request**:

`POST` `/devices/`

Parameters:

Name             | Type  | Required | Description
-----------------|-------|----------|------------
serial_number    | uuid4 | Yes      | The serial number of the device.
firmware_version | char  | Yes      | The firmware version on the device.

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
201 Created

{
  "id": 6,
  "serial_number": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011",
  "firmware_version": "v1.0.0",
  "registered": "2019-06-02T00:08:09+0000",
  "auth_token": "132cf952e0165a274bf99e115ab483671b3d9ff6"
}
```

The `auth_token` returned with this response should be stored by the client for
authenticating future requests to the API. See [Authentication](authentication.md).

## Create a device sensor log

**Request**:

`POST` `/sensor_logs/`

Parameters:

Name        | Type     | Required | Description
------------|----------|----------|------------
sensor_type | char     | Yes      | The type of sensor data. TM = Temperature (in Celsius), HM = Air humidity percentage, CO = Carbon Monoxide level in the air (PPM)
value       | decimal  | Yes      | The value from the sensor

*Example:*

```
curl -X POST http://127.0.0.1:8000/api/v1/sensor_logs/ -H "Content-Type: application/json" -H 'Authorization: Token 73c8a8ad8a51ad207d10087981e882516c7dd80c' -d '{"value":"12","sensor_type":"TM"}'
```

*Note:*

- Autthentication header must be specified. See [Authentication](authentication.md).

**Response**:

```json
Content-Type application/json
201 Created

{
  "sensor_type": "TM",
  "stamp": "2019-06-02T06:00:53+0000", 
  "value":"12.00000"
}
```

## Create a device health status log

**Request**:

`POST` `/health_status/`

Parameters:

Name        | Type | Required | Description
------------|------|----------|------------
value       | char | Yes      | The health status of the device, less than 150 chars

*Example:*

```
curl -X POST http://127.0.0.1:8000/api/v1/health_status/ -H "Content-Type: application/json" -H 'Authorization: Token 73c8a8ad8a51ad207d10087981e882516c7dd80c' -d '{"value":"needs_service"}'
```

*Note:*

- Autthentication header must be specified. See [Authentication](authentication.md).

**Response**:

```json
Content-Type application/json
201 Created

{
  "stamp":"2019-06-02T06:12:02+0000",
  "value":"needs_service"
}
```