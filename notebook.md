# Design exercises: scale models and logical clocks
## Ari Troper, Liam McInroy, Max Snyder

### 2023.03.01

Liam made a barebones commit of the general file structure.
Basically the same as in [`wire`](https://github.com/ariliammax/wire).

### 2023.03.02

We started by making a `logical_step` function, which takes in a `target`
to run and then times how long it takes. It then sleeps until the next logical
step is over (i.e., if it goes slightly over the length of one logical step, it
waits until the second logical step). That's a design decision, which will
likely be irrelevant. If it doesn't make sense in the logs, we'll ignore it.

##### A second session

All of the pipes keep breaking on `recv`...

### 2023.03.03

It turns out we were trying to `recv` on a `socket` not a `connection`...
D'oh.

### 2023.03.04

Discussed how we'll test and what-not. Couple of important steps:

- make a `max_logical_steps` for testing, so it doesn't all run endlessly.

- make the `rand.randint` a parameter, so we can make deterministic
(up to race conditions) tests.

- make `logical_step` return the number of taken steps, so if we increment
differently than that logic determines (e.g. due to message received "from
the future"). This makes it functional instead of a global state thing, which
is nice.

Hey! Ari here...

We're working on building the testing suite. To begin we decided that we would
make a mock Machine object because we don't want to run into "PORT in use"
errors using real sockets.

The dummy Machine writes directly into a message queue instead of through 
a socket with sendall.

Using our dummy machine will redirect the logs to standard output, which won't
show when testing. Therefore, we also created a mock Log object which will have
a property 'logicalClock' we can use in our asserts.

Since we will want to deterministically test the "random dice roll" we decided
to pass in the random generator function into main, which is then called
during the dice roll. The mock objects pass deterministic functions to
generate numbers into the "random" argument.

### 2023.03.07

Planning for the experiments: since there is the "initial" run of experiments,
and another run with "smaller" variation in logical clock rates and "smaller"
probability of internal events, we'll use the following configurations

#### "initial run"

For all runs, the probability of internal events `p(i)` will be `7/10`,
per the specifications. So we'll just list the durations of each machine's
logical steps:

- A1: `[1/6, 1/6, 1/6]`
(all same)

- A2: `[1/6, 1, 1]`
(one faster than two same, high variation)

- A3: `[1/6, 1/6, 1]`
(one slower than two same, high variation)

- A4: `[1/6, 1/2, 1]`
(all different, high variation)

- A5: `[1/6, 1/4, 1/2]`
(all different, mid variation)

#### "variation runs"

Here, we'll also specify the `p(i)`.


- B1: `p(i) = 1/4`, `durs = [1/6, 1/6, 1/6]`
(lower internal, all same)

- B2: `p(i) = 1/4`, `durs = [1/6, 1/5, 1/5]`
(lower internal, one faster than two same, low variation)

- B3: `p(i) = 1/4`, `durs = [1/6, 1/6, 1/5]`
(lower internal, one slower than two same, low variation)

- B4: `p(i) = 1/4`, `durs = [1/6, 1/5, 1/4]`
(lower internal, all different, low variation)

To explain: the A-series gives just a heuristic of varying the variation
(and a bit about how this variation is found, i.e. the shape of the
distribution of times).

Then the B-series shrinks the variation and probability of internal events,
but tests the same shapes of the distribution of times.

### 2023.03.08

Many tests and experiments have been written.

The experiments also nicely autogenerate graphs; they are very pretty.

In the tests, we found a funny bug: if a default argument is a list, then it
is bound to all instances... It's an easy fix (just initialize the list
you want as a non-default), but c'mon python.

#### Results

Discussion may be found in the main [`README.md`](README.md)

| Experiment | Figure |
| ---------- | ------ |
| A1 | ![experiment A1](figures/A1.png) |
| A2 | ![experiment A2](figures/A2.png) |
| A3 | ![experiment A3](figures/A3.png) |
| A4 | ![experiment A4](figures/A4.png) |
| A5 | ![experiment A5](figures/A5.png) |
| B1 | ![experiment B1](figures/B1.png) |
| B2 | ![experiment B2](figures/B2.png) |
| B3 | ![experiment B3](figures/B3.png) |
| B4 | ![experiment B4](figures/B4.png) |
