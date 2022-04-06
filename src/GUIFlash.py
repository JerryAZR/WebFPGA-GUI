"""
Modified by Zerui An <anzerui@126.com> on April 5th, 2022

This file ("GUIFlash.py") is based on the file "Flash.py" included
in the webfpga-cli program, which is covered by the following license:

MIT License

Copyright (c) 2019 Auburn Ventures, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from webfpga.Compress import compress
from webfpga.Utilities import *

import usb.core
import usb.util

from threading import Thread
from easygui import exceptionbox
from kivy.clock import Clock

def startFlashThread(bitstream, progress, callback=None):
    _thread = Thread(target=flashWrapper, args=[bitstream, progress, callback])
    _thread.start()

def flashWrapper(bitstream, progress, callback):
    try:
        with open(bitstream, "rb") as infile:
            Flash(infile.read(), progress)
    except:
        exceptionbox()

    progress.dismiss()
    if (callback):
        Clock.schedule_once(callback)

# Main flash routine:
# Flash device with bitstream
# If the bitstream is uncompressed, then compress it
def Flash(bitstream, progress):
    print("Opening USB device...")
    dev = get_device()

    print("\nPreparing device for flashing...")
    prepare(dev)

    print("\nErasing device...")
    erase(dev)

    print("\nFlashing device...")
    flash(dev, compress(bitstream), progress)

def prepare(device):
    handshake(device, "AT", "Hi")
    handshake(device, "API", "C_WEBUSB|CWEBUSB+")
    handshake(device, "APR", "000921|01010(4|5|6|7)")
    print("Found programmer.")

    print("Checking for FPGA module and its flash configuration...")
    handshake(device, "APWE", "wren")
    amq = handshake(device, "AMQ", ".*")

    assert len(amq) >= 9, "Bad AMQ response, too short."
    assert amq[0] == "S", "Flash device not supported."
    assert amq[6] == "H", "Flash device has bad Cascadia header."

def erase(device):
    handshake(device, "AMBE", "DONE")
    amq = handshake(device, "AMQ", ".*")

    assert len(amq) >= 9, "Bad AMQ response, too short."
    assert amq[0] == "S", "Flash device not supported."
    assert amq[5] == "W", "Flash device is write protected."
    assert amq[6] == "H", "Flash device has bad Cascadia header."
    assert amq[8] == "E", "Flash device is not erased."

def flash(device, buf, progress):
    handshake(device, "AMW", "OK")

    idx = 0
    progress.max = len(buf)
    while idx < len(buf):
        # Update progress bar
        progress.value = idx
        # Read the block size,
        # then and use that to slice a block
        block_size = buf[idx]
        block = buf[idx:idx+block_size]
        idx += block_size

        # transmit the block
        res = issue_command(device, "AMWD", wIndex=0, data=block)
        expect(device, ".*")

    progress.value = progress.max
