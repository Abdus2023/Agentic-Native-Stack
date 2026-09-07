# OUROBOROS M0 — Repository-Native Autonomous Engineering Runtime

This directory defines the M0 implementation contract for a Python runtime whose source, skills, policies, state, verification machinery, and bootstrap mechanism live inside the repository it can engineer.

## Core invariant

Every repository mutation passes through the kernel, is policy-evaluated, produces an observation, is journaled, and invalidates prior verification by advancing the repository generation.

## M0 lifecycle

`INTAKE → PLANNED → AUTHORIZED → EXECUTING → OBSERVED → VERIFYING → VERIFIED → PROMOTABLE → PROMOTED`

Failure and policy denial are terminal for the current run unless an explicit recovery transition creates a new plan.

## Trust boundary

Bootstrap establishes trust from repository state. The runtime never treats generated output as authoritative merely because it generated it. Kernel, policy, verifier, and bootstrap changes require elevated authorization and independent verification.

## Verification evidence

Promotion requires immutable evidence bound simultaneously to:

1. the run identity;
2. the repository generation;
3. the verification epoch;
4. the complete required-gate result set; and
5. the complete verifier gate contract.

### Canonical gate contract

M0.23 defines `Gate` identity as `ouroboros.gate-contract.v1` followed by canonical UTF-8 JSON objects containing exactly `name`, `required`, and the ordered `command` argument vector. JSON uses sorted keys, compact separators, and UTF-8 encoding. Gates are sorted by unique name before hashing.

Therefore:

- gate declaration order does not affect identity;
- command argument boundaries are preserved;
- changing `required` changes identity;
- changing any command argument changes identity; and
- the contract schema itself is versioned.

Promotion compares the evidence's gate-set digest with the current kernel verifier's digest and fails closed on mismatch.

## M1.3 — Crash recovery authority boundary

The journal is an integrity-checked, hash-chained JSONL history. Recovery is a **reconstruction authority boundary**, not a state inference engine.

The normative invariant is:

> **No durable event → no recovered authority.**

In particular:

- `AUTHORIZED` requires a durable `AUTHORIZATION_GRANTED` event following durable `PLANNED` state;
- `VERIFIED` requires a durable `VERIFICATION_EVIDENCE_CAPTURED` event containing complete, digest-valid evidence;
- `GATE_RESULT` records alone never imply `VERIFIED`;
- `PROMOTABLE` requires durable `PROMOTION_AUTHORIZED` bound to the recovered evidence digest and gate-contract digest; and
- `PROMOTED` requires durable `PROMOTED` following that promotion authorization.

Verification evidence is serialized completely in the capture event so a crashed process can reconstruct the same immutable evidence rather than trusting an in-memory object that disappeared with the process. Any malformed, tampered, incomplete, stale, cross-run, or incorrectly ordered privileged record causes recovery to fail closed.

Repeated mutation after `OBSERVED` also emits a new durable `AUTHORIZATION_GRANTED` event before execution. Recovery therefore never interprets `ACTION_EXECUTED` as implicit authorization.

## M1.4 — Journal durability contract

The journal append operation is serialized with an inter-process exclusive lock on POSIX platforms. Each append:

1. acquires the append lock;
2. validates the complete existing chain before choosing its sequence and predecessor digest;
3. appends exactly one canonical JSON record;
4. flushes the file buffer; and
5. calls `fsync` before releasing the lock.

A blank or malformed record is corruption, not an ignorable tail. Recovery and subsequent appends therefore fail closed rather than silently skipping damaged history.

On platforms without the required inter-process locking primitive, append fails closed rather than pretending that concurrent append serialization exists.

## M1.5 — External journal trust anchor

M1.4 proves crash durability and hash-chain consistency, but a hash chain beginning at a public all-zero genesis does not establish authenticity: an attacker who can rewrite the complete journal can recompute every digest.

M1.5 introduces `JournalTrustAnchor`, a pre-provisioned checkpoint held outside the mutable journal. A trusted read requires both ordinary journal validation and an exact match against the external checkpoint.

The anchor binds:

1. the checkpoint sequence;
2. the checkpoint digest; and
3. optionally, the repository generation at that checkpoint.

A whole-history rewrite, truncation before the checkpoint, or generation mismatch is rejected. The runtime does **not** create, rotate, or replace an anchor during recovery. Anchor provisioning and storage are therefore part of the deployment trust boundary, not repository-derived authority.

This is a checkpoint authenticity boundary, not a complete key-management system. If an attacker can also replace the external anchor, the anchor provides no protection; M1.6 can add signed checkpoints/key lifecycle as the next trust layer.

## Required M0 proof

1. Cold bootstrap from repository state.
2. Runtime discovers a repository-declared skill.
3. Runtime adds a new skill through the kernel.
4. Candidate generation is verified.
5. Verification is bound to that exact generation.
6. A cold bootstrap of the promoted generation discovers and executes the new skill.

## Planned package

`ourob/` contains the kernel, state machine, action model, policy engine, skill registry, filesystem/process/git adapters, verifier, manifest/generation machinery, bootstrap, deterministic planner, and CLI.

## M1 direction

M1 extends the in-process lifecycle with durable journal replay and crash recovery. M1.3 establishes the authority boundary, M1.4 establishes append durability, and M1.5 establishes an external checkpoint trust boundary.

This M0 artifact is intentionally placed under the existing Agentic-Native-Stack repository as an architecture/implementation seed; it is not yet the executable package until the implementation slice is committed.