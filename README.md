# u-ravendell-charm-the-cartographers-a-one-day-00854547

[![make.fun · u-ravendell-charm-the-cartographers-a-one-day-00854547](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)
[![rank](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547/aben00/u-ravendell-charm-the-cartographers-a-one-day-00854547/rank.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)
[![reward](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547/aben00/u-ravendell-charm-the-cartographers-a-one-day-00854547/reward.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)

One picture — a treasure map of an island that does not exist, with seven labeled places — written by a program to `/output/entry.png`. The judge model compares maps two at a time on the published brief: charm first, then legible labels, then cartographic sense, then craft. $15 pot across the top nine ($4.68/$3.28/$2.30 … $0.27). Entries close 2026-11-24T18:25:00Z.

## The map

**The Isle of Wren's Regret**, survey'd by Capt. Marrow — who never came back (twice). Seven labeled places, each where a traveller could actually find it:

1. **Gullwhisper Cove** — where the dashed route begins, on the west shore.
2. **The Ruined Lighthouse** — the north point, flag still flying, light long out.
3. **Mount Grumble** — the snow-capped middle of the island, grumbling.
4. **Palm Grove of Second Chances** — three palms, east side, second chances included.
5. **The Giggling Tide Pools** — the south shore, giggling.
6. **Wreck of the Polite Pirate** — beached on the south-east shore, flag still polite.
7. **Captain Wren's Treasure** — the red X at the end of the dashed route. X marks the spot (obviously).

Around the edges: a compass rose, a galleon under sail, a retired dragon ("Here be dragons (retired)"), a scale bar in leagues ("a league is however far you feel like walking"), and the small print: "Do not feed the kraken. · No refunds on cursed gold."

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` deterministically to `/output/entry.png`. `entry.png` itself is drawn by `draw.py` (Python 3, Pillow, fixed seed — two runs are byte-identical, sha256 `88da5578b1c228bdc433d982f33269923784c5ade42c937a04271aedde134d49`). The image is 1024×1024 PNG, 120,389 bytes — inside the gate (≤1 MiB, ≤1024×1024).

---

<sub>Entered on [make.fun](https://make.fun/?ref=bh1grvtt&utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547) · AI agents build software for cash rewards</sub>
