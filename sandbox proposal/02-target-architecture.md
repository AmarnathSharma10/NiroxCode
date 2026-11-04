# Target architecture

## Trust boundaries

Use four distinct zones:

```text
Browser
  |
  v
Web/API service  --->  Queue  --->  Runner control service  --->  disposable sandbox
  |                         ^                  |
  +--> database             |                  +--> result store
                            +---------------------+
```

- **Web/API:** handles authentication, validation, job creation, status
  responses, and persistence. It must not compile or execute user code.
- **Queue:** carries an opaque job identifier and bounded metadata. It must not
  contain hidden test data in user-readable responses.
- **Runner control service:** trusted orchestration code that claims jobs,
  selects an approved language image, enforces admission limits, and records
  results. It should have no public route.
- **Sandbox:** the least-trusted zone. It receives only the source and input
  needed for one execution, then is destroyed.

The database and result store must be reachable only by the control service
through narrowly scoped credentials. The sandbox must not reach either.

## Per-job lifecycle

1. Validate language, source size, input size, and request rate at the API.
2. Create a job with an idempotency key and a short expiry.
3. Store source and input in a private job workspace, not under the web code
   tree. Prefer encrypted object storage or a restricted worker volume.
4. Enqueue only the job identifier and execution policy version.
5. The runner claims the job with a lease and an overall deadline.
6. Create a fresh sandbox from an immutable, language-specific image.
7. Copy in source and input as read-only data; mount only a bounded writable
   temporary directory.
8. Compile and execute inside the same sandbox under the limits in
   `03-security-controls.md`.
9. Stream only bounded stdout/stderr to the runner; truncate or classify excess.
10. Destroy the sandbox and workspace in a `finally`-equivalent cleanup path.
11. Persist a normalized result and release the job lease.
12. Return a safe verdict/status to the user without exposing hidden tests or
    internal paths.

## Run versus submit

`Run code` should execute one user-provided input. `Submit solution` should be
one queued job whose test cases are selected by the trusted runner, not one
HTTP request that loops synchronously. The runner may reuse one sandbox for the
test-case set only if the workspace is reset between cases; the safer v1
default is one fresh process and clean input per case, with a job-level cap.

Hidden tests and expected outputs should be fetched only by the runner through a
private channel, or mounted into a trusted runner process that compares output.
They must never be copied into user-visible result fields.

## Sandbox implementation tiers

1. **Preferred:** dedicated runner VM/worker pool plus Firecracker or gVisor,
   with one disposable sandbox per job.
2. **Acceptable transitional design:** rootless Docker/Podman with a dedicated
   runner host, `--network=none`, read-only root filesystem, dropped
   capabilities, seccomp/AppArmor, no host mounts, and cgroup limits.
3. **Not acceptable:** invoking `subprocess.run` from Django, privileged
   containers, host PID/network namespaces, Docker socket access, arbitrary
   bind mounts, or a shared long-lived execution container.
