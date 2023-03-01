# Design Exercise: scale models and logical clocks
## Ari Troper, Liam McInroy, Max Snyder

### Setup and scripts

#### Module installation

First, you should (preferably) setup and use a `virtualenv`.
This isn't required, but it is best practice.

```bash
source install.sh
```

#### Configuring IP

To get the IP address of the host, run

```bash
ipconfig getifaddr en0
```

#### Running

##### Start the system

To start the whole system of 3 machines, run

```bash
python -m clocks.system.main \
    [MACHINEN_ADRS ...]
```

where

- `MACHINEN_ADRS` are variadic arguments for all of the machines' addresses.
Each address should be formatted as `HOST:PORT`. The list is space delimited.

##### Single machines

To start a single machine, run 

```bash
python -m clocks.machine.main \
    [--host=HOST] \
    [--port=PORT] \
    MACHINE0_ADR [, MACHINEN_ADRS]
```

where

- `HOST` is the host of this machine (default `localhost`)

- `PORT` is the port of this machine.

- `MACHINE0_ADR` is at least one other machine's address, formatted as
`HOST:PORT`.

- `MACHINEN_ADRS` are variadic arguments for more machines, space delimited,
all formatted as `HOST:PORT`.

#### Testing

To run the tests, run

```bash
source runtests.sh
```

#### Documentation

To view the auto-generated documentation at
[`localhost:1234`](http://localhost:1234/clocks), run

```bash
source docshtml.sh
```

#### Linting

To lint all of the source code, run

```bash
source lint.sh
```