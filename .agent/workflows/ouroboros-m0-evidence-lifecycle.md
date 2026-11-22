# OUROBOROS M0 Evidence Lifecycle

**Status:** operator-run workflow  
**Source:** `ouroboros/M0/README.md` and `ouroboros/M0/ourob/`

## Lifecycle
`INTAKE → PLANNED → AUTHORIZED → EXECUTING → OBSERVED → VERIFYING → VERIFIED → PROMOTABLE → PROMOTED`

## Procedure
1. Bootstrap trust from repository state and identify the exact repository generation.
2. Create a bounded plan with action manifest and required gates.
3. Persist authorization before any mutation.
4. Route every mutation through kernel and policy evaluation.
5. Observe the actual effect and append a durable journal event.
6. Advance repository generation and invalidate prior verification.
7. Run the complete required verifier gate set.
8. Capture immutable evidence bound to run, generation, verification epoch, gate results and gate-contract digest.
9. Verify journal chain, external trust anchor or signed checkpoint and key lifecycle.
10. Promote only after current verifier contract and complete evidence match.
11. On crash, reconstruct authority only from valid durable events; malformed/tampered/stale/incomplete records fail closed.
12. Record CI run, commit, test output and remaining limitations.

## Required invariants
- No durable event → no recovered authority.
- A gate result alone never implies VERIFIED.
- ACTION_EXECUTED alone never implies authorization.
- Gate-contract drift invalidates prior promotion evidence.
- Trust anchors and signing private keys remain outside mutable repository state.

## Stop conditions
Fail closed on journal corruption, missing durable authorization, incomplete evidence, gate-contract mismatch, stale generation, unknown/revoked key or trust-anchor mismatch.
