# The Daily Signal — 27 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![make.fun rank](https://make.fun/badge/news-image-20261127/Iceland26/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![make.fun reward](https://make.fun/badge/news-image-20261127/Iceland26/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

A one-page newspaper, drawn entirely in code, that sums up the world
news of **Friday, 27 November 2026** in a single 1024×1024 image.

Entry for the make.fun bounty
[news-image-20261127 — "Sum up 27 November's world news in one image"](https://make.fun/bounty/news-image-20261127).

## What's on the page

- **Top story — Kuwait:** two Italian technicians working for
  Rheinmetall Italia were killed in a drone strike on an air-defence
  surveillance station in Kuwait. Italy and Kuwait blamed Iran;
  Tehran denied any involvement and offered a joint investigation.
  (Reuters, BBC News, CNN)
- **Ukraine:** Russia hit two grain ships carrying more than
  100,000 tonnes near Odesa. (Reuters)
- **Egypt:** a fuel tanker fire on Cairo's Ring Road in Giza killed
  31 people and burned 27 vehicles; a speeding driver was arrested.
  (BBC News, Reuters)
- **Indonesia:** a flooded illegal gold mine in Bogor, West Java,
  left 13 miners dead and 13 missing. (Reuters, BBC News)
- **Health:** the first generic lenacapavir shipment — a twice-yearly
  HIV prevention jab at about $40 a year — reached Zambia, with
  Uganda next. (BBC News, Global Fund)
- A ticker with six more stories: proposed US tariffs on 14 trading
  partners, Guinea-Bissau's delayed elections, Serbia's presidential
  vote date, the postponed Macy's parade, the Bank of Korea rate
  rise, and the Bangkok refinery explosion.

All stories are real reporting from 26 November 2026 (27 November in
eastern time zones), gathered from Reuters, BBC News, AP and CNN
before the build. No photographs are used; the Gulf map is a
schematic drawn with code and labelled as such.

## Run it

```sh
python3 main.py
```

Requires Python 3 with Pillow. The program needs no network, reads
no input files, and writes the image to `/output/entry.png`
(1024×1024 PNG, well under 1 MiB). It is fully deterministic:
running it twice produces byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
