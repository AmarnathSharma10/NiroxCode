# Security controls and threat model

## Required controls

### Input and policy

- Allowlist languages and exact compiler/runtime versions.
- Reject unsupported filenames, compiler flags, package managers, binary
  uploads, and archive inputs.
- Set maximum source, input, and submission sizes before queueing.
- Normalize language identifiers server-side; never use user input as a command
  or image name.
- Add per-user, per-IP, and global concurrency/rate limits.
- Use a queue deadline and reject stale jobs.

### Sandbox identity and kernel boundary

- Run as a dedicated non-root UID/GID with no supplementary groups.
- Use a rootless runtime where practical.
- Drop all Linux capabilities; do not grant `SYS_ADMIN`, `SYS_PTRACE`, or
  device access.
- Use a restrictive seccomp profile and AppArmor/SELinux policy.
- Isolate PID, mount, IPC, UTS, and network namespaces.
- Set `no_new_privs`; disable privilege escalation and setuid behavior.
- Do not mount the Docker/Podman socket, host `/proc`, host `/sys`, host
  filesystem paths, secrets, credentials, or the database.

### Filesystem and data

- Use an immutable, signed, pinned runner image.
- Make the image filesystem read-only.
- Mount only a per-job temporary workspace with a small size limit.
- Mount source and input read-only where possible.
- Use unique unguessable job paths and restrictive permissions.
- Delete the workspace and sandbox after every terminal state.
- Keep hidden tests and expected outputs outside the sandbox.

### Network

- Set network namespace to none, with no DNS, loopback exceptions, or proxy
  environment variables unless a future language explicitly requires them.
- Enforce egress at the runner host as well as inside the sandbox.
- Do not allow metadata-service, private-network, database, queue, or web-service
  access.

### Resource limits

Apply limits to both compilation and execution:

| Resource | v1 policy requirement |
|---|---|
| Wall time | Hard timeout for each process and job |
| CPU | Cgroup quota plus CPU accounting |
| Memory | Cgroup memory and swap limits |
| Processes/threads | PID limit; prevent fork bombs |
| Output | Separate stdout/stderr byte caps |
| Files | Workspace byte quota and file-count limit |
| Open files | `RLIMIT_NOFILE` |
| Core dumps | Disabled |
| Stack/address space | Explicit `rlimit`/cgroup policy |
| Concurrent jobs | Runner pool and per-user quotas |

The values must be configurable by language and measured in tests. A killed
process should produce a specific status such as `TIME_LIMIT`, `MEMORY_LIMIT`,
`OUTPUT_LIMIT`, or `PROCESS_LIMIT`, not a generic rejection.

## Threats and mitigations

| Threat | Primary mitigation |
|---|---|
| Infinite loop | Wall-clock timeout and process-group termination |
| Fork bomb | PID namespace and process limit |
| Memory exhaustion | Cgroup memory/swap ceiling |
| Disk exhaustion | Bounded temporary filesystem and cleanup |
| Network exfiltration | No network namespace plus host egress deny |
| Reading application secrets | No secret mounts, no host mounts, separate UID |
| Container escape | Rootless runtime, dropped capabilities, seccomp, hardened kernel |
| Cross-job reads | Fresh workspace, unique permissions, sandbox destruction |
| Hidden-test disclosure | Trusted comparison and sanitized result schema |
| Compiler abuse | Apply the same limits to compilation and use pinned toolchains |
| Queue flooding | Authentication, rate limits, quotas, bounded queue |
| Result tampering | Runner-only result signing or authenticated status updates |

## Observability without data leakage

Record job ID, language, image digest, policy version, start/end timestamps,
resource usage, termination reason, and runner host. Do not log source code,
stdin, hidden tests, secrets, or full compiler output by default. Keep
diagnostic output truncated and access-controlled.
