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