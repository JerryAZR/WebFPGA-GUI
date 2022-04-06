"""
This file is part of the WebFPGA-GUI program
(https://github.com/JerryAZR/WebFPGA-GUI).

Copyright (c) 2022, Zerui An <anzerui@126.com / jerryazr@gmail.com>.

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.

The WebFPGA-GUI program is based on the WebFPGA CLI tool developed
by the WebFPGA Team (https://github.com/webfpga/cli). The Copyright
of the original program belongs to Auburn Ventures, LLC and is
covered by the MIT License (https://opensource.org/licenses/MIT).
"""

# generic imports
import asyncio
import glob
import os
import sys
from docopt import docopt
# webfpga imports
from webfpga           import VERSION
from webfpga.Flash     import Flash
from webfpga.Synthesis import Synthesize
from webfpga.Utilities import SetBitstring

usage = """
webfpga-gui (cli mode)

Usage:
    webfpga-gui
    webfpga-gui synth [-o FILENAME] [--no-cache] <verilog> ...
    webfpga-gui flash <bitstream>
    webfpga-gui setbitstring <bitstring>
    webfpga-gui -v | --version
    webfpga-gui -h | --help

Options:
    synth           Synthesis the selected files
    flash           Flash the selected bitstream onto webFPGA
    setbitstring    Set the CPU->FPGA communication bits
    -o FILENAME     File name of generated bitstream [default: bitstream.bin]
    --no-cache      Disable bitstream caching
    -v --version    Show version number of the webfpga-cli backend
    -h --help       Show this screen
Arguments:
    verilog         Verilog files to be synthesized
    bitstream       Bitstream file to be flashed [default: bitstream.bin]
    bitstring       CPU->FPGA communication bits

"""

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        # GUI imports
        os.environ["KIVY_NO_ARGS"] = "1"
        from kivy.config import Config
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        from mainScreen import WebFPGA_GUI
        from kivy.resources import resource_add_path, resource_find
        from easygui import exceptionbox
        # Launch the GUI
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        try:
            WebFPGA_GUI().run()
        except Exception as e:
            exceptionbox()
    else:
        print("Command Line Mode")
        # Get arguments
        args = docopt(usage)

        # Print webfpga-cli version
        if (args["--version"]):
            print(f"WebFPGA CLI version {VERSION}")
            print("Copyright (C) Auburn Ventures, LLC. MIT License.")

        elif (args["synth"]):
            # Open the output file
            outfile = open(args["-o"], "wb")
            # Open the input files
            infiles = []
            for pattern in args["<verilog>"]:
                for fname in glob.glob(pattern):
                    infiles.append(open(fname, "r"))
            
            asyncio.run(Synthesize(
                input_verilog=infiles,
                output_bitstream=outfile,
                no_cache=args["--no-cache"])
            )

            # close used files
            for infile in infiles:
                infile.close()
            outfile.close()

        # Program the FPGA
        elif (args["flash"]):
            try:
                with open(args["<bitstream>"], "rb") as bitstream:
                    Flash(bitstream.read())
            except ValueError as e:
                if e.args[0] == "Device not found":
                    # we are expecting a "Device not found" error
                    print(e)
                else:
                    # but not a "No backend available" error
                    raise e

        # Set the CPU->FPGA communication bits
        elif (args["setbitstring"]):
            SetBitstring(args["<bitstring>"])
        
