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