# Design exercises: scale models and logical clocks
## Ari Troper, Liam McInroy, Max Snyder

### 2023.03.01

Liam made a barebones commit of the general file structure.
Basically the same as in [`wire`](https://github.com/ariliammax/wire).

### 2023.03.02

We started by making a `logical_step` function, which takes in a `target`
to run and then times how long it takes. It then sleeps until the next logical
step is over (i.e., if it goes slightly over the length of one logical step, it
waits until the second logical step). That's a design decision, which will likely
be irrelevant. If it doesn't make sense in the logs, we'll ignore it.

##### A second session

Max made Ari stop before he coded the machines to reecive any data.
Then suddenly all of the pipes broke.

Max **CLOGGED** the _pipes_. ~ Frank Zapppa

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
make a mock Machine object because we don't want to run into "PORT in use" errors
using real sockets.

The dummy Machine writes directly into a message queue instead of through 
a socket with sendall.

Using our dummy machine will redirect the logs to standard output, which won't
show when testing. Therefore, we also created a mock Log object which will have
a property 'logicalClock' we can use in our asserts.

Since we will want to deterministically test the "random dice roll" we decided to
pass in the random generator function into main, which is then called during the dice
roll. The mock objects pass deterministic functions to generate numbers into the "random"
argument.