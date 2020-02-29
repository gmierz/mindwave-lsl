# mindwave-lsl

This tool is for Mindwave EEG products and it was tested with Mindwave Mobile 2. You can use it to take data from a ThinkGear Connecter service using telnet and output it in a Lab Streaming Layer (LSL) outlet.

Run the following to clone the library and install the tool:
```
cd ~
git clone https://github.com/gmierz/mindwave-lsl
cd mindwave-lsl
py setup.py install 
```

Then, to run it you can call it through the command line:
```
mindwavelsl
```

It has two options available:
```
usage: mindwavelsl [-h] [--host HOST] [--port PORT]

Run this tool to push Mind Wave Mobile 2 data from the ThinkGear Connector socket, to Lab Streaming Layer (LSL).

optional arguments:
-h, --help   show this help message and exit
--host HOST  The host for the ThinkGear Connector.
--port PORT  The port for the ThinkGear Connector. 
```

You can also use it as a module:
```
from mindwavelsl import MindwaveLSL

mwlsl = MindwaveLSL('localhost', 13854)

# Setup the LSL outlet and the ThinkGear connection
mwlsl.setup_lsl()

# Run the service
mwlsl.run()

```

To add different Mindwave data connection methods (other than telnet, like serial com port) you will need to modify the read/write method found here as well as the connection method. The read method must return a stringified `dict` that contains a key (and value) for all the entries in `EXPECTED_FIELDS`.
