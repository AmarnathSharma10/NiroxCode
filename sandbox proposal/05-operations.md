# Operations and incident response

## Deployment separation

Deploy the web/API and runner as separate services on separate least-privilege
runtime identities. The web service should be able to enqueue jobs and read
sanitized results, but not launch containers, access the runner host, read
hidden tests, or use a container socket. The runner should be able to read
approved job inputs and write result records, but should not have Django admin,
user-session, or unrestricted database permissions.

The deployment documentation should explicitly define:

- private network routes between web, queue, result store, and runner;
- firewall rules denying sandbox egress and runner-host ingress;
- runner host patching and kernel hardening;
- image provenance, digest pinning, and vulnerability scanning;
- log retention and access control;
- backup and restoration for job metadata without retaining unnecessary source.

## Metrics and alerts

Track queue depth and age, jobs by terminal status, execution duration,
compile duration, CPU/memory usage, output truncations, timeout counts,
sandbox-start failures, cleanup failures, runner restarts, and per-user quota
violations. Alert on queue growth, repeated sandbox failures, unexpected network
attempts, privileged-operation denials, and any cleanup failure.

## Incident response

If escape or cross-job access is suspected:

1. Disable new execution jobs with the kill switch.
2. Isolate or stop affected runner hosts; do not continue reusing them.
3. Preserve runner, kernel, queue, and audit logs without logging new source.
4. Rotate runner credentials and invalidate affected job leases.
5. Rebuild runner images from trusted sources and patch the runtime/kernel.
6. Review database, object-store, queue, and host access logs.
7. Re-enable execution only after adversarial verification and approval.

## Safe failure behavior

If the queue, runner, or result store is unavailable, the web application
should report that execution is temporarily unavailable rather than executing
locally or returning a success-shaped fallback. A repeated runner failure
should trip a circuit breaker and preserve normal browsing, authentication, and
submission-history functionality.
