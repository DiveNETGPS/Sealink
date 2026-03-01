# DiveNET: Sealink-OEM Subsea Wireless Modem  
## Protocol Specification v1.0

**Document Date**: February 2026  
**Revision**: 1.0  
**Copyright**: © 2026 DiveNET Subsea Wireless – Beringia Enterprises LLC. All rights reserved.

## Contents

1. Introduction  
   1.1 Physical Layer  
   1.2 NMEA0183 Protocol Standard  

2. Sealink Commands & Responses  

   2.1 ACK Response  
   2.2 Settings Write  
   2.3 Remote Code Request  
   2.4 Remote Code Response  
   2.5 Remote Timeout  
   2.6 Remote Asynchronous Input  
   2.7 Ambient Data Configuration  
   2.8 Ambient Data Output  
   2.9 Device Information Request  
   2.10 Device Information  
   2.11 Packet Mode Settings Read  
   2.12 Packet Mode Settings  
   2.13 Packet Mode Settings Write  
   2.14 Packet Send  
   2.15 Packet Failed  
   2.16 Packet Delivered  
   2.17 Packet Received  
   2.18 Remote Request (Logical Addressing)  
   2.19 Remote Timeout (Logical Addressing)  
   2.20 Remote Response (Logical Addressing)  
   2.21 Incremental Data Configuration (USBL models only)  
   2.22 Incremental Data Output (USBL models only)  

3. Operating Modes  

   3.1 Transparent Channel Mode  
   3.2 Command Mode  
   3.3 Packet Mode  

4. Identifiers  

   4.1 Error Codes  
   4.2 Remote Command IDs  

5. Appendix  

   5.1 Command Mode Examples  
      5.1.1 Example 1 – Requesting Device Information  
      5.1.2 Example 2 – Requesting Remote Depth  
      5.1.3 Example 3 – Ambient Data Configuration  
      5.1.4 Example 4 – Enabling Packet Mode  
      5.1.5 Example 5 – Sending a Packet  
   5.2 Configuration Recipes  

## 1. Introduction

### 1.1 Physical Layer

The Sealink-OEM modem uses an asynchronous RS-232 compatible UART interface with 3.3 V logic levels. Connection requires four wires: Tx (transmit), Rx (receive), Vcc (+3.3 V logic supply), and GND. Maximum guaranteed cable length without repeaters or converters is 2 meters.

**Default UART settings**:
- Baud rate: 9600 bit/s  
- Data bits: 8  
- Stop bits: 1  
- Parity: None  
- Hardware flow control: None  

**Power supply**: +12 V DC nominal (12 V min – 14 V ±0.3 V max)  
**Warning**: Logic lines are 0–3.3 V only. Voltages >5.3 V may cause shutdown or permanent damage.

The modem defaults to Command Mode on power-up.

### 1.2 NMEA0183 Protocol Standard

The Sealink protocol follows the NMEA0183 text-based format with proprietary extensions. All messages are ASCII, start with `$`, use comma separators, and end with `*` + two-digit hex checksum + `<CR><LF>`.

**Sentence example**:
`$PUWV0,1,0*36<CR><LF>`

**Structure**:
- `$` – sentence start  
- `P` – Proprietary  
- `UWV` – manufacturer identifier
- Sentence identifier (e.g. `0`, `2`, etc.)  
- `,` – parameter separator  
- `*` – checksum separator  
- `hh` – two-digit hex checksum (XOR of all bytes from after `$` to before `*`)  
- `<CR><LF>` – end of sentence (hex 0x0D 0x0A)

## 2. Sealink Commands & Responses

All sentences use the `$PUWV` prefix.

### 2.1 ACK Response
Device acknowledgement.

**Format**: `$PUWV0,cmdID,errCode*hh<CR><LF>`

| Field    | Description                                      |
|----------|--------------------------------------------------|
| cmdID    | ID of the incoming sentence causing this ACK     |
| errCode  | Error code (see 4.1 Error Codes)                 |

### 2.2 Settings Write
Write new configuration settings.

**Format**: `$PUWV1,txChID,rxChID,salinityPSU,isCmdMode,isACKOnTXFinished,gravityAcc*hh<CR><LF>`

| Field                | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| txChID               | Transmit code channel ID (0–19)                                             |
| rxChID               | Receive code channel ID (0–19)                                              |
| salinityPSU          | Water salinity in PSU (e.g. 0 for fresh, 35 for seawater)                   |
| isCmdMode            | 1 = Command mode by default, 0 = Command mode by pin                        |
| isACKOnTXFinished    | 1 = ACK sent after TX buffer empty, 0 = no ACK                              |
| gravityAcc           | Local gravity acceleration (m/s², typical 9.77–9.84)                        |

### 2.3 Remote Code Request
Send a short command to a remote modem.

**Format**: `$PUWV2,txChID,rxChID,rcCmdID*hh<CR><LF>`

| Field     | Description                                    |
|-----------|------------------------------------------------|
| txChID    | Transmit code channel ID                       |
| rxChID    | Receive code channel ID for the request        |
| rcCmdID   | Remote command ID (see 4.2 Remote Command IDs) |

### 2.4 Remote Code Response
Reply from remote modem.

**Format**: `$PUWV3,txChID,rcCmdID,propTime,MSR[,Value][,Azimuth]*hh<CR><LF>`

| Field     | Description                                      |
|-----------|--------------------------------------------------|
| txChID    | Transmit code channel used                       |
| rcCmdID   | Echo of requested command ID                     |
| propTime  | Propagation time in seconds (one-way)            |
| MSR       | Mean signal ratio (dB)                           |
| Value     | Requested value (e.g. depth, temperature)        |
| Azimuth   | Horizontal angle of arrival (USBL models only)   |

### 2.5 Remote Timeout
No reply from remote modem.

**Format**: `$PUWV4,txChID,rcCmdID*hh<CR><LF>`

| Field     | Description                                      |
|-----------|--------------------------------------------------|
| txChID    | Transmit code channel used                       |
| rcCmdID   | Requested command ID                             |

### 2.6 Remote Asynchronous Input
Incoming message from remote modem.

**Format**: `$PUWV5,rcCmdID,MSR[,Azimuth]*hh<CR><LF>`

| Field     | Description                                      |
|-----------|--------------------------------------------------|
| rcCmdID   | Command ID (see 4.2)                             |
| MSR       | Mean signal ratio (dB)                           |
| Azimuth   | Horizontal angle of arrival (USBL models only)   |

### 2.7 Ambient Data Configuration
Configure automatic transmission of ambient parameters and supply voltage.

**Format**: `$PUWV6,isSaveToFlash,PeriodMs,IsPressure,IsTemperature,IsDepth,IsVCC*hh<CR><LF>`

| Field            | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| isSaveToFlash    | 1 = save to flash, 0 = do not save                                          |
| PeriodMs         | Output period (ms): 0 = disabled, 1 = tandem, 500–60000 = timed             |
| IsPressure       | 1 = enable pressure output, 0 = disable                                     |
| IsTemperature    | 1 = enable temperature output, 0 = disable                                  |
| IsDepth          | 1 = enable depth output, 0 = disable                                        |
| IsVCC            | 1 = enable supply voltage output, 0 = disable                               |

### 2.8 Ambient Data Output
Ambient parameters and supply voltage readings.

**Format**: `$PUWV7,Pressure_mBar,Temperature_C,Depth_m,VCC_V*hh<CR><LF>`

| Field           | Description                  |
|-----------------|------------------------------|
| Pressure_mBar   | Pressure in millibars        |
| Temperature_C   | Temperature in °C            |
| Depth_m         | Depth in meters              |
| VCC_V           | Supply voltage in volts      |

### 2.9 Device Information Request
Request device information.

**Format**: `$PUWV?,reserved*hh<CR><LF>`

| Field     | Description   |
|-----------|---------------|
| reserved  | Set to 0      |

### 2.10 Device Information
Device information response.

**Format**: `$PUWV!,serialNumber,systemMoniker,systemVersion,coreMoniker,coreVersion,acBaudrate,rxChID,txChID,maxChannels,styPSU,isPTS,isCmdMode*hh<CR><LF>`

| Field           | Description                                      |
|-----------------|--------------------------------------------------|
| serialNumber    | Device serial number                             |
| systemMoniker   | System name                                      |
| systemVersion   | System version                                   |
| coreMoniker     | Communication subsystem name                     |
| coreVersion     | Communication subsystem version                  |
| acBaudrate      | Acoustic channel baud rate (bit/s)               |
| rxChID          | Receive code channel ID                          |
| txChID          | Transmit code channel ID                         |
| maxChannels     | Total number of code channels                    |
| styPSU          | Salinity setting (PSU)                           |
| isPTS           | 1 = pressure/temperature sensor present          |
| isCmdMode       | 1 = Command mode by default                      |

### 2.11 Packet Mode Settings Read
Read current packet mode settings. The modem responds with IC_D2H_PT_SETTINGS.

**Format**: `$PUWVD,reserved*hh<CR><LF>`

| Field     | Description                  |
|-----------|------------------------------|
| reserved  | Set to 0                     |

### 2.12 Packet Mode Settings
Current packet mode configuration.

**Format**: `$PUWVE,isPTMode,ptLocalAddress*hh<CR><LF>`

| Field          | Description                                      |
|----------------|--------------------------------------------------|
| isPTMode       | 1 = packet mode enabled, 0 = disabled            |
| ptLocalAddress | Local modem address (0–254)                      |

**Note**: Since firmware 1.20, packet mode is active whenever the modem is in Command Mode — no separate enable flag is required.

### 2.13 Packet Mode Settings Write
Set new packet mode settings. The modem responds with IC_D2H_PT_SETTINGS.

**Format**: `$PUWVF,isSaveToFlash,isPTMode,ptLocalAddress*hh<CR><LF>`

| Field           | Description                                      |
|-----------------|--------------------------------------------------|
| isSaveToFlash   | 1 = save to flash, 0 = do not save               |
| isPTMode        | 1 = enable packet mode, 0 = disable              |
| ptLocalAddress  | Local modem address (0–254)                      |

**Note**: isPTMode is legacy (firmware 1.20+ ignores it — Command Mode enables packet mode automatically).

### 2.14 Packet Send
Send a data packet in packet mode.

**Format**: `$PUWVG,target_ptAddress,maxTries,dataPacket*hh<CR><LF>`

| Field              | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| target_ptAddress   | Destination address (0–254 unicast, 255 broadcast)                          |
| maxTries           | Maximum retransmission attempts (0–255; empty = default 255)                |
| dataPacket         | Hex bytes with `0x` prefix (e.g. `0x313233` for “123”). Max 64 bytes. Empty = cancel current transfer. |

### 2.15 Packet Failed
Transmission failed (max tries exceeded or other error).

**Format**: `$PUWVH,target_ptAddress,maxTries,dataPacket*hh<CR><LF>`

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| target_ptAddress   | Destination address                              |
| maxTries           | Number of attempts made                          |
| dataPacket         | Hex bytes sent (same as request)                 |

### 2.16 Packet Delivered
Packet successfully delivered with acknowledgement.

**Format**: `$PUWVI,target_ptAddress,maxTries[,azimuth],dataPacket*hh<CR><LF>`

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| target_ptAddress   | Destination address                              |
| maxTries           | Number of attempts made                          |
| azimuth            | Horizontal angle of arrival (USBL models only; empty otherwise) |
| dataPacket         | Hex bytes sent (same as request)                 |

### 2.17 Packet Received
Incoming packet from another modem.

**Format**: `$PUWVJ,sender_ptAddress[,azimuth],dataPacket*hh<CR><LF>`

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| sender_ptAddress   | Sender address (0–254)                           |
| azimuth            | Horizontal angle of arrival (USBL models only; empty otherwise) |
| dataPacket         | Received hex bytes (max 64)                      |

### 2.18 Remote Request (Logical Addressing)
Request a parameter from a remote modem using logical addressing.

**Format**: `$PUWVK,target_ptAddress,dataID*hh<CR><LF>`

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| target_ptAddress   | Remote modem address (0–254)                     |
| dataID             | Requested parameter: 0 = depth, 1 = temperature, 2 = supply voltage |

### 2.19 Remote Timeout (Logical Addressing)
No response to logical-addressed remote request.

**Format**: `$PUWVL,target_ptAddress,dataID*hh<CR><LF>`

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| target_ptAddress   | Remote modem address                             |
| dataID             | Requested parameter ID                           |

### 2.20 Remote Response (Logical Addressing)
Response to logical-addressed remote request.

**Format**: `$PUWVM,target_ptAddress,dataID,dataValue,pTime[,azimuth]*hh<CR><LF>`

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| target_ptAddress   | Remote modem address                             |
| dataID             | Requested parameter ID                           |
| dataValue          | Returned value (e.g. depth in m, temp in °C, voltage in V) |
| pTime              | Propagation time in seconds                      |
| azimuth            | Horizontal angle of arrival (USBL models only; empty otherwise) |

### 2.21 Incremental Data Configuration (USBL models only)
Configure output of pitch and roll data.

**Format**: `$PUWV8,isSaveToFlash,PeriodMs*hh<CR><LF>`

| Field           | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| isSaveToFlash   | 1 = save to flash, 0 = do not save                                          |
| PeriodMs        | Output period (ms): 0 = disabled, 1 = tandem, 500–60000 = timed             |

### 2.22 Incremental Data Output (USBL models only)
Pitch and roll readings.

**Format**: `$PUWV9,reserved,Pitch,Roll*hh<CR><LF>`

| Field     | Description                          |
|-----------|--------------------------------------|
| reserved  | Reserved (empty)                     |
| Pitch     | Device pitch in degrees              |
| Roll      | Device roll in degrees               |
### 3. Operating Modes

3.1 Transparent Channel Mode  
In Transparent mode, all data from the host is sent unchanged over the acoustic channel and received unchanged by another modem on the same code channel.

3.2 Command Mode  
Command mode allows configuration, ranging, and advanced control. Modems analyze incoming data only in this mode.  
- Default on power-up  
- Can be set permanently via Settings Write (isCmdMode = 1)  
- SVC/CMD pin (XP5 Pin 3) becomes a strobe output for Tx/Rx timing

3.3 Packet Mode  
Packet mode enables reliable data transfer up to 64 bytes, including arbitrary data, with guaranteed delivery and acknowledgement.  
- Active automatically in Command Mode (no separate enable needed since firmware 1.20+)  
- Supports 255 logical addresses (0–254 unicast, 255 broadcast)  
- See commands 2.11–2.20

### 4. Identifiers

4.1 Error Codes

| Code | Value | Description                          |
|------|-------|--------------------------------------|
| LOC_ERR_NO_ERROR             | 0     | Request accepted                     |
| LOC_ERR_INVALID_SYNTAX       | 1     | Syntax error                         |
| LOC_ERR_UNSUPPORTED          | 2     | Request not supported                |
| LOC_ERR_TRANSMITTER_BUSY     | 3     | Transmitter busy                     |
| LOC_ERR_ARGUMENT_OUT_OF_RANGE| 4     | Parameter out of range               |
| LOC_ERR_INVALID_OPERATION    | 5     | Invalid operation                    |
| LOC_ERR_UNKNOWN_FIELD_ID     | 6     | Unknown field ID                     |
| LOC_ERR_VALUE_UNAVAILABLE    | 7     | Value not available                  |
| LOC_ERR_RECEIVER_BUSY        | 8     | Receiver busy                        |
| LOC_ERR_TX_BUFFER_OVERRUN    | 9     | TX buffer overrun                    |
| LOC_ERR_CHKSUM_ERROR         | 10    | Checksum error                       |
| LOC_ACK_TX_FINISHED          | 11    | TX buffer empty                      |
| LOC_ACK_BEFORE_STANDBY       | 12    | Entering standby                     |
| LOC_ACK_AFTER_WAKEUP         | 13    | Exited standby                       |
| LOC_ERR_SVOLTAGE_TOO_HIGH    | 14    | Supply voltage too high              |

4.2 Remote Command IDs

| Command             | Value | Description                          |
|---------------------|-------|--------------------------------------|
| RC_PING             | 0     | Ping                                 |
| RC_PONG             | 1     | Pong                                 |
| RC_DPT_GET          | 2     | Get remote depth                     |
| RC_TMP_GET          | 3     | Get remote temperature               |
| RC_BAT_V_GET        | 4     | Get remote battery voltage           |
| RC_ERR_NSUP         | 5     | Request not supported                |
| RC_ACK              | 6     | Request accepted                     |
| RC_USR_CMD_000–007  | 7–14  | User-defined commands                |
| RC_MSG_ASYNC_IN     | 16    | Incoming transparent message         |

### 5. Appendix

5.1 Command Mode Examples  
- Examples use correct checksums and <CR><LF> terminators. Replace `hh` with actual calculated checksum.
- Examples use "<<" to indicate outbound messages/querries and ">>" to indicate inbound messages/responses.

**5.1.1 Example 1 – Requesting Device Information**  

`<< $PUWV?,0*27<CR><LF>`

`>> $PUWV!,3A001E000E51363437333330,SEALINK,1.00,SEALINK_CORE,1.01,9600,0,0,20,35.0,1,1*XX<CR><LF>`

**Explanation**:  

- PUWV? = IC_H2D_DINFO_GET  
- Response includes serial number, system/core versions, baud rate, channel IDs, salinity, sensor presence, and Command Mode status.

**5.1.2 Example 2 – Requesting Remote Depth**  

`<< $PUWV2,0,0,2*28<CR><LF>`

`>> $PUWV0,2,036<CR><LF>` (ACK: request accepted, no error)

`>> $PUWV3,0,2,0.667,25.40,12.34XX<CR><LF>` (response: propTime=0.667 s, depth=12.34 m)

**Explanation**:  

- PUWV2 = IC_H2D_RC_REQUEST  
- 2 = RC_DPT_GET  
- Response: propagation time (s), signal quality (MSR in dB), and remote depth (m)

**5.1.3 Example 3 – Setting up the Ambient Data Configuration**

`<< $PUWV6,1,1000,1,1,1,1*03<CR><LF>`

`>> $PUWV0,6,032<CR><LF>` (ACK: request accepted, no error)

`>> $PUWV7,1025.2,29.9,-0.014,5.018<CR><LF>`  (periodic ambient data)

`>> $PUWV7,1026.3,29.9,-0.002,5.0*1D<CR><LF>`  (next reading)

**Explanation**:  

- PUWV6 = IC_H2D_AMB_DTA_CFG  
- 1 = save to flash  
- 1000 = 1-second interval  
- 1,1,1,1 = enable pressure, temperature, depth, VCC  
- PUWV7 = IC_D2H_AMB_DTA (pressure in mBar, temperature in °C, depth in m, VCC in V)

**5.1.4 Example 4 – Enabling Packet Mode**  

`<< $PUWVF,1,1,0*5E<CR><LF>`

`>> $PUWVE,1,0*40<CR><LF>`

**Explanation**:  

- PUWVF = IC_H2D_PT_SETTINGS_WRITE  
- 1 = save to flash  
- 1 = enable packet mode  
- 0 = local modem address  
- PUWVE = IC_D2H_PT_SETTINGS (confirms packet mode enabled, address 0)

**Note**: Since firmware 1.20+, packet mode is active in Command Mode — no separate enable required.

**5.1.5 Example 5 – Sending a Packet in Packet Mode and Receiving Acknowledgement**  

`<< $PUWVG,0,8,0x313233*2C<CR><LF>`

`>> $PUWV0,G,043<CR><LF>` (ACK: request accepted, no error)

`>> $PUWVI,0,1,,0x31323307<CR><LF>` (packet delivered successfully)
  
**Explanation**:  

- PUWVG = IC_H2D_PT_SEND  
- 0 = target address  
- 8 = max attempts  
- 0x313233 = hex bytes for "123"  
- PUWVI = IC_D2H_PT_DLVRD (0 = target, 1 = attempts, empty = no azimuth)

**5.1.6 Example 6 – Receiving an Incoming Packet**  

`>> $PUWVJ,42,,0x48656C6C6F*XX<CR><LF>`

**Explanation**:  

- PUWVJ = IC_D2H_PT_RCVD  
- 42 = sender address  
- (empty) = no azimuth  
- 0x48656C6C6F = hex bytes for "Hello"  

No host action required — incoming packet is delivered automatically.

**5.1.7 Example 7 – Requesting Remote Temperature (Logical Addressing)**  

`<< $PUWVK,10,1*XX<CR><LF>`

`>> $PUWVM,10,1,28.50,0.667,XX<CR><LF>` (success)

`>> $PUWVL,10,1XX<CR><LF>` (timeout)

**Explanation**:  

- PUWVK = IC_H2D_PT_ITG  
- 10 = target address  
- 1 = dataID (temperature)  
- PUWVM = IC_D2H_PT_ITG_RESP (temperature 28.50 °C, propTime 0.667 s)  
- PUWVL = IC_D2H_PT_ITG_TMO (timeout)

**5.1.8 Example 8 – Enabling Automatic Ambient Data Output (1-second interval)**  

`<< $PUWV6,1,1000,1,1,1,1*03<CR><LF>`

`>> $PUWV0,6,032<CR><LF>` (ACK: request accepted, no error)

`>> $PUWV7,1025.2,29.9,-0.014,5.018<CR><LF>` (periodic output)

`>> $PUWV7,1026.3,29.9,-0.002,5.0*1D<CR><LF>`

**Explanation**:  

- PUWV6 = IC_H2D_AMB_DTA_CFG  
- 1 = save to flash  
- 1000 ms interval  
- 1,1,1,1 = enable pressure, temperature, depth, VCC

**5.1.9 Example 9 – Requesting Device Information (Alternative Syntax)**  

`<< $PUWV?,0*27<CR><LF>`

`>> $PUWV!,3A001E000E51363437333330,SEALINK,1.00,SEALINK_CORE,1.01,9600,0,0,20,35.0,1,1*XX<CR><LF>`

**Explanation**:  

- Same as 5.1.1 — included here for completeness. Shows legacy syntax still works.

### 5.2 Configuration Recipes

1. **Set default settings (fresh water, Command mode disabled)**  
`$PUWV1,0,0,0.0,0,0,9.8067*XX<CR><LF>`

2. **Enable Command mode by default, seawater salinity**  
`$PUWV1,0,0,35.0,1,0,9.8067*XX<CR><LF>`

3. **Disable automatic ambient data output**  
`$PUWV6,0,0,0,0,0,0*32<CR><LF>`

5. **Enable ambient data every 5 seconds (pressure + temperature only)**  
`$PUWV6,0,5000,1,1,0,0*XX<CR><LF>`

7. **Request local depth (basic)**  
`$PUWV2,0,0,2*28<CR><LF>`

(Checksums must be calculated correctly before sending.)

___
Questions or support? Contact support@divenetgps.com
