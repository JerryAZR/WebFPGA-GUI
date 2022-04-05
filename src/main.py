# generic imports
import asyncio
import glob
import os
import sys
import traceback
from docopt import docopt
# webfpga imports
from webfpga           import VERSION
from webfpga.Flash     import Flash
from webfpga.Synthesis import Synthesize
from webfpga.Utilities import SetBitstring
# GUI imports
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from mainScreen import WebFPGA_GUI
from kivy.resources import resource_add_path, resource_find
from easygui import exceptionbox

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
         # Launch the GUI
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        try:
            WebFPGA_GUI().run()
        except Exception as e:
            exceptionbox()


    else:
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
            with open(args["<bitstream>"], "rb") as bitstream:
                Flash(bitstream.read())

        # Set the CPU->FPGA communication bits
        elif (args["setbitstring"]):
            SetBitstring(args["<bitstring>"])
        