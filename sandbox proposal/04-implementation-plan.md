# Implementation plan and acceptance criteria

This is a proposal for later implementation. The current branch intentionally
contains no code changes.

## Phase 0: establish policy

- Define supported language versions and exact limits.
- Define public result states and an internal diagnostic schema.
- Decide queue, result-store, runner-runtime, and worker-host choices.
- Add a threat-model review and an emergency kill-switch procedure.

**Exit criteria:** approved policy table, abuse cases, and rollback plan.

## Phase 1: extract execution from Django

- Introduce a runner boundary behind a queue; the web process submits jobs and
  polls or receives status.
- Preserve existing Run and Submit behavior through normalized job results.
- Add idempotency, job leases, retry rules, cancellation, and stale-job expiry.
- Move source/input workspaces outside the web container and clean them up.

**Exit criteria:** no web request invokes a compiler/interpreter; a runner
handles concurrent jobs without blocking Gunicorn; jobs survive a web restart
without duplicate judging.

## Phase 2: enforce disposable sandboxing

- Build separate, minimal, pinned images per language.
- Launch one disposable sandbox per job or test case.
- Enforce rootless identity, read-only root, no network, dropped capabilities,
  seccomp/AppArmor, PID namespace, cgroups, and filesystem quotas.
- Apply limits to compile and run phases independently.
- Ensure cleanup occurs for success, failure, timeout, cancellation, and runner
  crash.

**Exit criteria:** automated tests demonstrate that code cannot access the
  database, queue, web endpoint, host mounts, network, sibling workspace, or
  runner credentials.

## Phase 3: harden judging and production operations

- Remove compilers and JDK from the web image.
- Keep hidden tests in the trusted runner path and sanitize rejection details.
- Add per-user/global quotas, backpressure, circuit breakers, and runner
  health checks.
- Add security scanning and signature verification for runner images.
- Run adversarial tests continuously: fork bombs, memory bombs, huge output,
  deep recursion, symlink traversal, `/proc` inspection, network probes,
  compiler abuse, and concurrent workspace collisions.

**Exit criteria:** security review approval, load test results, alerting tested,
and documented rollback to a disabled-execution mode.

## Acceptance checklist

- [ ] Web/API has no compiler or interpreter subprocess path.
- [ ] Every job has a unique ID, lease, deadline, and terminal state.
- [ ] Every sandbox has no network and no host/secret/database mounts.
- [ ] Every execution has enforced CPU, memory, PID, disk, output, and wall-time
      limits.
- [ ] Compiler and runtime failures are classified separately.
- [ ] Cleanup is verified after every terminal outcome.
- [ ] Hidden tests and expected outputs never appear in user responses or logs.
- [ ] Runner images are pinned, minimal, scanned, and reproducible.
- [ ] Per-user and global concurrency limits prevent queue starvation.
- [ ] Metrics and alerts cover queue depth, timeouts, resource kills, cleanup
      failures, and sandbox-start failures.
- [ ] A kill switch prevents new execution jobs while preserving the web app.
