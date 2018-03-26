# pybabblesdk

## Installation

```bash
git clone https://github.com/babbleio/pybabblesdk.git
cd pybabblesdk
python setup.py install --user
```

## Examples

An example of how to use the SDK is given in the examples/sendmessage directory.
To run this application, first start a babble network consisting of four nodes:

```bash
cd examples/sendmessage
make
```

Now run the sendmessage client from the same directory:

```bash
./sendmessage
```