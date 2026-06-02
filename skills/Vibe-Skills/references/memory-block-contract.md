# Memory Block Contract Mapping

This reference maps Letta-style memory blocks into VCO Runtime v2 semantics.

| Letta Concept | VCO Equivalent | Canonical Owner |
|---|---|---|
| Core runtime context | active session state | `state_store` |
| Persistent project memory | explicit project decision memory | `Serena` |
| Short semantic recall | short-term retrieval cache | `ruflo` |
| Archival memory | graph / relationship retrieval | `Cognee` |
| Preference note | optional external preference store | `mem0` |
| Tool rule | governance contract | `Letta` contract only |

## Rules

1. A memory block describes organization, not ownership transfer.
2. VCO owners stay canonical even when Letta terms are used.
3. If one memory block maps to multiple VCO owners, split the block rather than broadening ownership.
