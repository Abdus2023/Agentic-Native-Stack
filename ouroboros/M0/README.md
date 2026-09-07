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

M1 extends the in-process lifecycle with durable journal replay and crash recovery. Recovery may reconstruct only state that is supported by durable events; it may never manufacture authorization, verification, or promotion that was not durably recorded.

This M0 artifact is intentionally placed under the existing Agentic-Native-Stack repository as an architecture/implementation seed; it is not yet the executable package until the implementation slice is committed.
