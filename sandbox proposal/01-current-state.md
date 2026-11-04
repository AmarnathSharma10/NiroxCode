# Current-state assessment

## Execution path

The current execution path is implemented in `Main/home/views.py`:

1. `problem_desc` accepts the submitted language, source, and input from the
   authenticated request.
2. `run_code` creates `codes`, `inputs`, and `outputs` below the Django
   project directory.
3. It writes the submitted source and input to those paths.
4. It invokes `gcc`, `g++`, `javac`, `java`, or `python` with
   `subprocess.run`.
5. `Submit` calls `run_code` once for every stored test case and compares the
   returned text.

The same Django/Gunicorn process therefore handles HTTP requests, filesystem
writes, compilation, execution, output capture, and judging.

## Main isolation gaps

- **Host/process exposure:** user programs execute as the application’s OS
  identity, in the web container, without a separate privilege boundary.
- **No timeout:** a program can hang indefinitely and consume a Gunicorn worker.
- **No resource ceilings:** CPU, memory, process count, output size, open files,
  compiler work, and temporary storage are not bounded.
- **Network is not denied:** a child process may inherit whatever network access
  the application container has.
- **Shared writable paths:** code, binaries, inputs, and outputs are created in
  application directories and are not reliably cleaned up.
- **Cross-run interference:** predictable shared directories and concurrent
  requests create opportunities for collisions, disk exhaustion, or reading
  another run’s artifacts.
- **Compilation is also untrusted execution:** compiler input and compiler
  subprocesses receive no separate policy from the final program.
- **Submission amplification:** one request can execute the user program for
  every test case synchronously.
- **Result leakage:** rejected submissions currently include test input and
  expected output in the response, which can expose hidden tests.
- **Error ambiguity:** timeout, signal termination, compilation failure, runtime
  failure, and output-limit failure are not represented as distinct results.
- **Web availability risk:** expensive submissions consume request workers and
  compete with normal application traffic.

## Existing deployment implications

`Main/Dockerfile` installs `gcc`, `g++`, and OpenJDK into the application image.
The deployment workflow builds and deploys a single `web` service. The README
describes Docker Compose and a private network, but the Compose policy is not
stored in this repository. These facts should be treated as migration concerns:
the runner must be deployed separately and the web image should eventually no
longer contain compilers.
