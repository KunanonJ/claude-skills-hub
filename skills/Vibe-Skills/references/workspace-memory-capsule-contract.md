# Workspace Memory Capsule Contract

## Purpose

Define the bounded disclosure capsule returned by the workspace-shared memory broker so runtime stages can consume memory continuity without raw storage coupling.

## Capsule Shape

Each capsule in `capsules[]` must include:

- `capsule_id`: stable record id (`record_id`)
- `owner`: canonical owner label (`Serena`, `ruflo`, `Cognee`)
- `lane`: broker lane id (`serena`, `ruflo`, `cognee`)
- `kind`: lane record kind (`decision`, `handoff_card`, `relation`)
- `disclosure_level`: currently `bounded`
- `summary`: short disclosure payload for stage prompts
- `updated_at`: UTC timestamp

## Broker Response Fields

The broker response must expose:

- `capsule_count`: number of capsules in this response
- `capsules`: bounded capsule list
- `suppressed_count`: writes filtered by noise admission
- `workspace_memory_plane`: workspace identity metadata

## Disclosure Rules

1. Capsules expose summary-level continuity only; they do not expose raw row internals.
2. Stage consumers should use `items[]` for prompt injection and `capsules[]` for metadata/accounting.
3. Host adapters must not infer physical storage topology from capsule contents.

## Compatibility Rule

Legacy callers can continue using `status`, `item_count`, and `items` while newer callers consume capsule metadata in parallel.
