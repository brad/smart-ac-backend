# Device
Supports registering devices.

## Register a new device

**Request**:

`POST` `/devices/`

Parameters:

Name            | Type  | Required | Description
----------------|-------|----------|------------
serial_number   | uuid4 | Yes      | The serial number of the device.

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
201 Created

{
  "serial_number": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011",
  "registered": "2019-06-02T00:08:09+0000",
  "auth_token": "132cf952e0165a274bf99e115ab483671b3d9ff6"
}
```

The `auth_token` returned with this response should be stored by the client for
authenticating future requests to the API. See [Authentication](authentication.md).