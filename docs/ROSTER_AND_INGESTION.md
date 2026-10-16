# Genuine Nations roster and ingestion contract

## Scope

The roster is a versioned sampling-frame artifact. It is not an empirical
finding and does not, by itself, validate the underlying classification.

The research protocol specifies a conservative 15-entity primary cohort and a
broader sensitivity cohort of approximately 18–20 entities. The roster template
is intentionally unpopulated: membership must be supported by dated evidence,
not inferred from a desired count.

## Roster workflow

1. Copy `data/roster/genuine_nations_roster_template.csv` to a versioned
   release file only when the candidate entries and sources are ready.
2. Use stable `entity_id` values and record membership in the nuclear set and
   AAA-rated set separately. The inclusion rule should express the union rule
   explicitly.
3. Record rating agency, rating scale if relevant, and the reference date for
   every AAA-set determination. A rating is time-specific; do not backdate a
   current rating.
4. Set `membership_status=verified` only when the inclusion rule and source
   provenance are present. Use `proposed` or `disputed` while a decision is
   unresolved. Use `excluded` to preserve a documented exclusion decision.
5. Freeze the primary cohort for the initial analysis. Put alternative
   membership choices in the sensitivity cohort or a new roster version.
   Never overwrite historical membership silently.

The validator checks schema, cohort labels, boolean indicators, duplicate
entity/cohort pairs, optional frozen cohort counts, and minimum provenance for
verified rows. It does not determine geopolitical status or validate the
truthfulness of a cited source.

## Country-year observations

Use the long-form schema in `docs/DATA_DICTIONARY_TEMPLATE.csv`. Each record
must retain the entity, year, variable, value, unit, source, source series code,
frequency, reference period, source release date, download date, transformation,
missingness flag, and notes. Preserve raw values separately from transformed
values; document transformations instead of replacing source observations.

Keep bilateral network records in a separate table with explicit origin,
destination, edge meaning, units, and observation period. Do not infer equal
flows from a reciprocal link.

## Reproducible ingestion

Use `pandavan_economy.roster.load_roster_csv` to validate a roster before
analysis. Use `pandavan_economy.ingestion.load_observations_csv` to validate
country-year observations before panel construction. Validators reject malformed
records; they do not download data, impute missing values, resolve source
conflicts, or claim that the data are analytically sufficient.

Recommended pipeline:

```text
versioned roster + source metadata
            |
            v
immutable raw downloads + retrieval log
            |
            v
schema/type validation
            |
            v
documented transformations and harmonization
            |
            v
country-year panel + missingness report
            |
            v
state classification and transition estimation
```

Do not estimate transition probabilities until state definitions, panel
frequency, missingness treatment, and membership version are recorded.
