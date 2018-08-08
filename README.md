# PyBabble SDK

An SDK to connect to a Babble node in Python. Compatible with both Python 2 & 3.

## Installation

```bash
pip install pybabblesdk
```

## Examples

An example of how to use the SDK is given in the `demo/sendmessage` directory.
To run this application, first change your working directory:

```bash
cd demo/sendmessage
```

Then you will need to run a test network with 4 Babble nodes:
```bash
make
```

Now you will need to build the Docker image and run the `sendmessage` demo:
```
make demo
```
