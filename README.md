# nov23-in-one-picture

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/hesperastryn/nov23-in-one-picture/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/hesperastryn/nov23-in-one-picture/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

The world news of **Monday 23 November 2026** in one picture: a newspaper-style front page drawn entirely in code. A huge date header tops six illustrated panels — the COP31 climate talks in Antalya collapsing with no deal after the EU rejected a final text that never mentions fossil fuels, Ukraine's sea drones sinking a Russian warship at its Benghazi base in Libya and destroying a Ka-27 helicopter, Russian strikes killing at least 15 people in the Kyiv region, US Democrats clinching their biggest House majority in decades, Trump warning he may resume strikes on Iran after the New Year if talks fail, and Washington probing Nvidia's chip sales to China as Trump backs ousted CEO Jensen Huang — with an "also today" ticker (the Manchester concert evacuation, Medvedev's nuclear remarks, France's tear-gas complaints, Bangladesh's vow to arrest Sheikh Hasina, NATO's nuclear-satellite fears) along the bottom.

`generate.py` (Python + PIL) draws the image procedurally — flat vector-style panels: a rejected final text stamped NO DEAL, sea drones closing on a warship in Benghazi harbour, missile arcs over a night skyline, the Capitol dome under a House majority banner, a New Year calendar page with its first day circled in red, and a giant AI chip under a magnifying glass — and writes `entry.png` (1024×1024). The entry program `main.py` is standard-library only: it copies the committed `entry.png` to the output directory, byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 generate.py   # redraws entry.png from scratch
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=9sbzt2n6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
