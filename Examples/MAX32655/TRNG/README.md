## Description

The true random number generator (TRNG) hardware is exercised in this example.  Random values are generated both using the blocking and non-blocking (asynchronous) functions.

## Software

### Project Usage

Universal instructions on building, flashing, and debugging this project can be found in the **[MSDK User Guide](https://analog-devices-msdk.github.io/msdk/USERGUIDE/)**.

### Project-Specific Build Notes

* This project comes pre-configured for the MAX32655EVKIT.  See [Board Support Packages](https://analog-devices-msdk.github.io/msdk/USERGUIDE/#board-support-packages) in the MSDK User Guide for instructions on changing the target board.

## Required Connections
If using the MAX32655EVKIT (EvKit\_V1):
-   Connect a USB cable between the PC and the CN1 (USB/PWR) connector.
-   Connect pins JP4(RX\_SEL) and JP5(TX\_SEL) to RX0 and TX0  header.
-   Open an terminal application on the PC and connect to the EV kit's console UART at 115200, 8-N-1.

If using the MAX32655FTHR (FTHR\_Apps\_P1):
-   Connect a USB cable between the PC and the J4 (USB/PWR) connector.
-   Open an terminal application on the PC and connect to the board's console UART at 115200, 8-N-1.

## Expected Output

The Console UART of the device will output these messages:

```
********** TRNG Example **********

Test TRNG Sync
0x98 0x0b 0x11 0xd9
0x40 0x06 0xe1 0x73
0xf4 0xe6 0x99 0xd5
0x50 0x15 0x37 0x8d

Test TRNG Async
0x7c 0x05 0xe6 0x47
0x25 0x69 0xd2 0x59
0xa7 0x11 0xa9 0xb5
0x8d 0x7d 0x83 0xda

********** Test Complete **********
```

