---
name: ouroboros-evidence-boundary-engineering
description: Govern repository-native agent execution through explicit lifecycle states, durable journals, exact gate contracts, crash recovery, and signed promotion evidence.
---

# OUROBOROS Evidence Boundary Engineering

## Purpose
Apply OUROBOROS M0's repository-native execution and promotion contracts without allowing generated output, in-memory state or incomplete journal records to create authority.

## Activation
Use when changing OUROBOROS lifecycle states, authorization, mutation journaling, verification evidence, crash recovery, gate contracts, trust anchors, signed checkpoints or promotion.

Do not claim the M0/M1 guarantees from the README alone; inspect the exact implementation and tests for the target revision.

## Inputs
- Exact Agentic-Native-Stack commit and OUROBOROS M0 source revision.
- Repository generation and run identity.
- Canonical gate contract and required command vectors.
- Journal records and integrity chain.
- External trust anchor or signed checkpoint envelope.
- Complete verification result set and verifier contract.

## Procedure
1. Pin the M0 implementation and the exact repository generation under review.
2. Preserve the lifecycle: INTAKE → PLANNED → AUTHORIZED → EXECUTING → OBSERVED → VERIFYING → VERIFIED → PROMOTABLE → PROMOTED.
3. Treat policy denial and failure as terminal for the current run unless an explicit recovery transition creates a new plan.
4. Require every mutation to pass through the kernel, receive policy evaluation, produce an observation, be journaled, and invalidate prior verification by advancing generation.
5. Bind verification evidence simultaneously to run identity, repository generation, verification epoch, required-gate results and complete verifier gate contract.
6. Canonicalize gate contracts exactly as specified: versioned identity, canonical UTF-8 JSON, exact fields, preserved command argument vectors, unique gate names and deterministic ordering.
7. Treat journal replay as an authority reconstruction boundary. No durable event means no recovered authority.
8. Require durable authorization before execution; an ACTION_EXECUTED record alone cannot imply authorization.
9. Require complete digest-valid verification evidence before VERIFIED. GATE_RESULT records alone never imply VERIFIED.
10. Serialize journal appends under the specified inter-process lock, validate the existing chain, append one canonical record, flush and fsync before releasing the lock.
11. Validate an external trust anchor or signed checkpoint against sequence, digest, generation, schema, algorithm and key lifecycle. Do not create/rotate trust anchors during recovery.
12. Fail closed on malformed, tampered, incomplete, stale, cross-run, wrongly ordered or mismatched privileged records.
13. Test crash points, replay, journal corruption, concurrent append, generation change, gate-contract drift, key rotation/revocation and promotion replay.
14. Bind each verification result to the exact implementation and test run; distinguish design requirements from tested behavior.

## Outputs
- Lifecycle/state transition contract.
- Gate-contract canonicalization and digest evidence.
- Durable journal and recovery test matrix.
- External trust-anchor/key-lifecycle record.
- Promotion evidence bundle and release decision.

## Failure handling
Fail closed on journal corruption, missing durable authorization, incomplete evidence, gate-contract mismatch, stale generation, unknown/revoked key, or trust-anchor mismatch. Do not reconstruct privileged state from an in-memory object or inferred event sequence.

## Acceptance criteria
- Every mutation passes through policy and kernel.
- Every mutation has observation and durable journal record.
- Generation changes invalidate prior verification.
- Evidence binds run, generation, epoch, gate results and verifier contract.
- Recovery derives authority only from valid durable events.
- Journal appends are serialized and fsynced.
- External trust anchors and signing keys remain outside mutable repository state.
- Promotion is impossible without exact, complete, current evidence.

## Source references
- `ouroboros/M0/README.md`
- `ouroboros/M0/ourob/kernel.py`
- `ouroboros/M0/ourob/journal.py`
- `ouroboros/M0/ourob/recovery.py`
- `ouroboros/M0/ourob/verify.py`
- `ouroboros/M0/ourob/promotion.py`
- `ouroboros/M0/ourob/signed_trust.py`
- `ouroboros/M0/tests/`

## Validation status
The M0 README describes required evidence contracts. Verify exact implementation and tests before marking any lifecycle or trust property VERIFIED.
