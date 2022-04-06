"""
Modified by Zerui An <anzerui@126.com> on April 4th, 2022

This file ("GUISynthesis.py") is based on the file "Synthesis.py" included
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

import json
import base64
import pprint
import requests
import asyncio
import websockets
import colorama
import termcolor
from termcolor import colored
from threading import Thread
from easygui import exceptionbox
from kivy.clock import Clock

# Cross-platform Colorama support
colorama.init()

BACKEND_URL = "https://backend.webfpga.com/v1/api"
WSS_URL     = "wss://backend.webfpga.com/v1/ws"

def startSynthThread(output_bitstream, input_verilog, no_cache, collection):
    # It's probabily better to use multiprocessing here if systhesis runs
    # on local machine
    # But since we are using a server, multithreading makes variable
    # sharing easy
    _thread = Thread(
        target=synthWrapper,
        args=[output_bitstream, input_verilog, no_cache, collection]
    )
    _thread.start()

def synthWrapper(output_bitstream, input_verilog, no_cache, collection):
    try:
        # open files
        outfile = open(output_bitstream, "wb")
        infiles = []
        for v in input_verilog:
            infiles.append(open(v, "r"))
        # start synthesis
        asyncio.run(Synthesize(outfile, infiles, no_cache, collection))
        # close used files
        for v in infiles:
            v.close()
        outfile.close()
    except:
        exceptionbox()
    # execute callback
    if (collection.onComplete):
        Clock.schedule_once(collection.onComplete)

async def Synthesize(output_bitstream, input_verilog, no_cache, collection):
    # Ensure that the backend is online
    print("Connecting to remote synthesis engine...")
    assert_connection()

    # Submit synthesis job to the backend
    print(f"Attempting synthesis (saving to {output_bitstream.name})...")
    for f in input_verilog:
        print("  -", f.name)
    res = request_synthesis(input_verilog, no_cache)
    id = res["id"]
    print("")

    # Check if the cached result already exists
    if res["cached"]:
        print("Cached bitstream already exists!")
        bitstream = download_bitstream(id)
        if bitstream["ready"]:
            save_bitstream(bitstream, output_bitstream)
            collection.success = True
            collection.done = True
            return

    # Follow synthesis log
    print(f"\nSubscribing to synthesis log (id={id})...")
    async with websockets.connect(WSS_URL) as ws:
        payload = {"type": "subscribe", "id": id}
        await ws.send(json.dumps(payload))

        while collection.run:
            # Block websocket until we receive a message
            raw_msg = await ws.recv()
            data = json.loads(raw_msg)

            # Confirm subscription registration
            if (data["type"] == "subscribe"):
                if data["success"]:
                    print("Subscription success!\n")
                else:
                    raise Exception("Failed to subscribe to synthesis log stream")

            # not a message, just print the json response
            if not "msg" in data:
                print(data)
                continue

            # print the message and break when synthesis is complete
            print_ws_msg(data)
            for msg in data["msg"]:
                # Check for keywords
                for keyword in collection.keywords:
                    if keyword in msg:
                        Clock.schedule_once(collection.onKeyword)
                        collection.keywords.remove(keyword)
                        break
                # Check for errors and warnings
                if ("ERROR" in msg) and (msg not in collection.errors):
                    collection.errors.append(msg)
                # We don't care about having duplicate warnings
                if ("WARNING" in msg):
                    collection.warnings.append(msg)
                # Check if synthesis has completed (or failed)
                if "synthesis complete" in msg:
                    print("Synthesis complete! Downloading bitstream...")
                    bitstream = download_bitstream(id)
                    save_bitstream(bitstream, output_bitstream)
                    collection.done = True
                    collection.success = True
                    return
                elif "synthesis failed" in msg:
                    collection.done = True
                    collection.success = False
                    return

# Raise error if we are unable to ascertain a positive status
# from the backend server
def assert_connection():
    r = requests.get(BACKEND_URL + "/status")
    print(r.status_code, r.text, "\n")
    if r.status_code != 200 or r.json()["status"] != "ok":
        raise Exception("Backend is unreachable")

# Submit Verilog source files to the synthesis engine
def request_synthesis(input_verilog, no_cache):
    # Assemble file name and contents into JSON object for transmission
    files = []
    for f in input_verilog:
        body = f.read()
        files.append({"name": f.name, "body": body})
    #print(files)

    headers = {"X-WEBFPGA-CACHE": ("false" if no_cache else "true")}
    #print("request headers", headers)

    payload = json.dumps({"files": files})
    url = BACKEND_URL + "/synthesize"
    res = requests.post(url, data=payload, headers=headers)
    pprint.pprint(res.json())

    return res.json()

# Print a websocket synthesis-log message
def print_ws_msg(data):
    for msg in data["msg"]:
        if msg.startswith("#*"):
            fields = msg.split(" ")
            color  = fields[0][2:]
            # Colorama+Termcolors doens't support 256 colors
            # We could use a different library (e.g. Colored), but
            # then we would lose Windows support
            if not color in termcolor.COLORS:
                color = "yellow"
            print(colored(" ".join(fields[1:]), color))
        else:
            print(msg)

def download_bitstream(id):
    res = requests.get(BACKEND_URL + "/bitstream/" + id).json()
    print(res)
    return res

def save_bitstream(bitstream, output_file):
    print("Saving bitstream...")
    b = base64.b64decode(bitstream["bitstream"])
    output_file.write(b)