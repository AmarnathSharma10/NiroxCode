# Sandboxing proposal

This folder proposes how NiroxCode should isolate code supplied by users before
the backend runs or submits it. It is documentation only: no application code,
container configuration, dependency manifest, or workflow has been changed in
this branch.

## Scope and objective

The objective is to make an untrusted program unable to meaningfully affect the
web application, host filesystem, database, network, other submissions, or
service availability. The design covers both **Run code** and **Submit
solution**, including compilation, execution, test-case orchestration, result
collection, cleanup, and operational monitoring.

## Documents

- [Current-state assessment](./01-current-state.md)
- [Target architecture](./02-target-architecture.md)
- [Security controls and threat model](./03-security-controls.md)
- [Implementation plan and acceptance criteria](./04-implementation-plan.md)
- [Operations and incident response](./05-operations.md)

## Recommended direction

The web process should never invoke a compiler or interpreter. It should create
a bounded execution job, place it on a queue, and return a job identifier. A
separate runner service should claim the job and launch a fresh, short-lived
sandbox for it. The sandbox should have no network, a read-only runtime image,
an isolated temporary filesystem, a non-root identity, dropped Linux
capabilities, a restrictive seccomp profile, and explicit CPU, memory, process,
file-size, output-size, and wall-clock limits.

For the strongest practical isolation, run the sandbox inside a dedicated
worker VM or a hardened container runtime such as Firecracker or gVisor. Plain
Docker containers are useful defense in depth but should not be treated as a
complete security boundary for hostile code.

## Non-goals for v1

- Supporting arbitrary packages, downloads, interpreters, or compiler flags.
- Allowing user code to access the application database or internal services.
- Guaranteeing perfect protection against a kernel or hypervisor compromise.
- Exposing hidden test cases, expected outputs, or host diagnostics to users.
