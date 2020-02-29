# mindwave-lsl

This tool is for Mindwave EEG products and it was tested with Mindwave Mobile 2. You can use it to take data from a ThinkGear Connecter service using telnet and output it in a Lab Streaming Layer (LSL) outlet.

It can connect to Mindwave headsets using [mindwave-python](https://github.com/BarkleyUS/mindwave-python)/[python-mindwave](https://github.com/faturita/python-mindwave) as a connector too. Furthermore, you can set `--output` to a directory or CSV file to output the data there.

This package is available through pip
```
pip install mindwavelsl
mindwavelsl
```

If pip doesn't work, run the following to clone the library and install the tool:
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

It has multiple options available including file output, and a mindwave-python connection option:
```
usage: mindwavelsl [-h] [--no-lsl] [--output OUTPUT] [--host HOST]
                   [--port PORT] [--mindwave-python-connect] [--device DEVICE]
                   [--headset-id HEADSET_ID] [--no-open-serial]

Run this tool to push Mind Wave Mobile 2 data from the ThinkGear Connector
socket, to Lab Streaming Layer (LSL).

optional arguments:
  -h, --help            show this help message and exit
  --no-lsl              Set this flag to disable LSL outlet.
  --output OUTPUT       Path to output data to, can include a CSV filename.
  --host HOST           The host for the ThinkGear Connector.
  --port PORT           The port for the ThinkGear Connector.
  --mindwave-python-connect
                        Set this to connect to Mindwave headset using
                        mindwave-python (through the module `mindwave`). It
                        needs to be installed manually, and instructions can
                        be found here: https://github.com/BarkleyUS/mindwave-
                        python. A more up-to-date version exists here as well:
                        https://github.com/faturita/python-mindwave. Must set
                        --device and --headset-id to use.
  --device DEVICE       Set this to the device of the headset to record i.e.
                        /dev/tty.MindWave2.
  --headset-id HEADSET_ID
                        Set this to the headset-id of the headset to record.
  --no-open-serial      If set, then `open_serial` in mindwave.Headset will be
                        set to False.
```

You can also use it as a module:
```
from mindwavelsl import MindwaveLSL

mwlsl = MindwaveLSL('localhost', 13854)

# Setup the LSL outlet and the ThinkGear connection
mwlsl.setup()

# Run the service
mwlsl.run()

```

See how the `TelnetConnector` and `MindwavePythonWrapper` connectors are implemented to add other connection options.
