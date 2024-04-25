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
to merge it into one single easy to get place. For example, it's now
a oneliner in python:

`ibis.read_parquet("https://github.com/NickCrews/election-data/releases/download/v2024-04-05_0/cleaned.parquet")`

See https://github.com/NickCrews/election-data/releases for
available versions to download, or the notebooks for methodology.
