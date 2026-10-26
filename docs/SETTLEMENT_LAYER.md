# Settlement and resident layer

## Purpose

This layer records settlement identities, settlement-to-settlement relationships, and narrative or sourced resident assignments. It is separate from the existing five-state absorbing Markov model and from the country-year observation pipeline. Adding a settlement record does not change the Markov chain or establish an empirical economic result.

## Data files

- `data/settlements/settlements.csv`: one row per settlement.
- `data/settlements/resident_assignments.csv`: one row per character/person-to-settlement assignment.
- `data/settlements/settlement_links.csv`: one row per directed relationship between settlements.

The files use explicit headers and preserve provenance. Blank templates are valid starting points; do not populate them with guessed villages, populations, flows, or residents.

## Settlement types and evidence

Use `settlement_type` to distinguish a village from a town, city, capital, or other settlement. Do not call a city a village merely to fit a question or a model. Use `verification_status` to distinguish a narrative fixture, a proposed entry, and a source-verified entry. Narrative fixtures support the epic-world illustration only; they are not historical or geographic verification.

## Draupadi and Indraprastha

The initial narrative fixture associates Draupadi with Indraprastha, the Pandavas' capital in the Mahabharata tradition. It classifies Indraprastha as a `capital_city`, not a village. This is a literary/narrative association, not a claim that the exact historical location or administrative status is established.

Accordingly, the repository does **not** claim that Draupadi resides in one of a set of model villages: no village roster has yet been supplied. To answer a specifically village-level allocation question, first define and version the village roster and the allocation rule, then record a sourced or explicitly hypothetical assignment. Do not silently convert a narrative association into an empirical fact.

## Relationship schema

A link must state its direction and meaning. Examples of possible `link_type` values include `trade`, `road`, `administrative`, and `reciprocal_exchange`. A reciprocal relationship is not evidence of equal flows in both directions. Record units and observation period for any quantitative weight; leave them blank for qualitative narrative links.

## Integration rules

1. Keep settlement identifiers stable across versions.
2. Keep narrative fixtures separate from empirical observations and mark them clearly.
3. Do not infer population, economic state, transition probabilities, or intervention effects from the existence of a settlement or resident assignment.
4. Before estimation, document the settlement sampling frame, inclusion rules, observation frequency, missingness, and source provenance.
5. Extend the existing validators only in a separate change with tests; this initial PR defines the data contract and starter files without altering the validated country-level pipeline.
