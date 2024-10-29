# US Election Data

Cleaned and normalized US election data:
- precinct-level
- from all 50 states
- from 2018, 2020, and 2022
- offices:
  - US presidential
  - US Senate
  - US house
  - Governor
  - State House
  - State Senate
  - Ballot Measures
  - Judicial Retentions
  - and others...

This was derived from https://github.com/MEDSL, but I found that
data was messy and in disparate places. This is an attempt
to merge it into one single easy to get place. For example, it's now super easy to get going:

```python
import ibis
ibis.options.interactive = True

t = ibis.read_parquet(
    "https://github.com/NickCrews/election-data/releases/download/v2024-04-25_0/cleaned.parquet"
)
t = t.cache()
print(t.count())
t
```

```
34263636
┏━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ year  ┃ date       ┃ state_po ┃ county_name ┃ county_fips ┃ jurisdiction_name ┃ jurisdiction_fips ┃ district  ┃ office                        ┃ magnitude ┃ special ┃ stage  ┃ precinct               ┃ writein ┃ candidate ┃ party_detailed ┃ mode         ┃ votes  ┃ readme_check ┃
┡━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━┩
│ int16 │ date       │ string   │ string      │ string      │ string            │ string            │ string    │ string                        │ int64     │ boolean │ string │ string                 │ boolean │ string    │ string         │ string       │ string │ boolean      │
├───────┼────────────┼──────────┼─────────────┼─────────────┼───────────────────┼───────────────────┼───────────┼───────────────────────────────┼───────────┼─────────┼────────┼────────────────────────┼─────────┼───────────┼────────────────┼──────────────┼────────┼──────────────┤
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-446 AURORA          │ False   │ NO        │ NULL           │ ELECTION DAY │ 570    │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-446 AURORA          │ False   │ YES       │ NULL           │ ELECTION DAY │ 274    │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-455 FAIRBANKS NO. 1 │ False   │ NO        │ NULL           │ ELECTION DAY │ 99     │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-455 FAIRBANKS NO. 1 │ False   │ YES       │ NULL           │ ELECTION DAY │ 53     │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-465 FAIRBANKS NO. 2 │ False   │ NO        │ NULL           │ ELECTION DAY │ 167    │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-465 FAIRBANKS NO. 2 │ False   │ YES       │ NULL           │ ELECTION DAY │ 100    │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-470 FAIRBANKS NO. 3 │ False   │ NO        │ NULL           │ ELECTION DAY │ 325    │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-470 FAIRBANKS NO. 3 │ False   │ YES       │ NULL           │ ELECTION DAY │ 152    │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-475 FAIRBANKS NO. 4 │ False   │ NO        │ NULL           │ ELECTION DAY │ 145    │ False        │
│  2018 │ 2018-11-06 │ AK       │ NULL        │ NULL        │ DISTRICT 1        │ 02001             │ STATEWIDE │ BALLOT MEASURE NO. 1 - 17FSH2 │         1 │ False   │ GEN    │ 01-475 FAIRBANKS NO. 4 │ False   │ YES       │ NULL           │ ELECTION DAY │ 92     │ False        │
│     … │ …          │ …        │ …           │ …           │ …                 │ …                 │ …         │ …                             │         … │ …       │ …      │ …                      │ …       │ …         │ …              │ …            │ …      │ …            │
└───────┴────────────┴──────────┴─────────────┴─────────────┴───────────────────┴───────────────────┴───────────┴───────────────────────────────┴───────────┴─────────┴────────┴────────────────────────┴─────────┴───────────┴────────────────┴──────────────┴────────┴──────────────┘
```

See https://github.com/NickCrews/election-data/releases for
available versions to download, or the notebooks for methodology.


## Data Notes

- CA doesn't have any US senate elections in 2022: https://github.com/MEDSL/2022-elections-official/issues/23
- Finding the total votes for a candidate seems inconsistent depending on if you
  find it either from where _.mode=="TOTAL" or from _.votes.sum(where=_.mode != "TOTAL").
  See tests/test_mode.py for an example.