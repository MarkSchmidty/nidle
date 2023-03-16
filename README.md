# NIDLE - An ncurses-based Idle Game

## Requiremnts
nidle has only been tested inside a `linux` terminal environment.
It may or may not work on Mac or Windows if you have ncurses and python installed.

## How to play
clone the repo or dowload just `nidle.py`
Then either run:
`python nidle.py`
or
```
chmod +x nidle.py
./nidle.py
```

You will be greeted by a screen which tells you what to do.

## Game Overview
NIDLE is a terminal-based idle game that uses ncurses for its interface. Players accumulate resources (Bronze, Silver, Gold, and Computronium) at various rates, which can be increased by purchasing mines. Ascensions become available upon reaching target amounts of Gold, and these ascensions grant Computronium, which further accelerates resource accumulation.

## Resources
There are four resource types in the game:

1. Bronze
2. Silver
3. Gold 
4. Computronium

## Resource Accumulation
- Bronze: Gained at a rate dependent on the number ofBronze mines and accumulated Silver.
- Silver: Gained at a rate dependent on the number of Silver mines and accumulated gold.
- Gold: Gained at a rate dependent on the number of Gold mines, plus any modifiers.

## Mines
- Bronze Mine:
  - Starting Quantity: 1
  - Purchase Cost: Increases incrementally with each purchase.
  - First Additional Mine Cost: 10 Bronze
- Silver Mine:
  - Purchase Cost: Increases incrementally with each purchase.
  - First Mine Cost: 1000 Bronze
  - Second Mine Cost: 10 Silver
- Gold Mine:
  - Purchase Cost: Increases incrementally with each purchase.
  - First Mine Cost: 1000 Silver
  - Second Mine Cost: 10 Gold

## Ascension
Available when a target amount of Gold is reached.
- Computronium is granted upon ascension.
- Consecutive units of Computronium require logarithmically more Gold than the previous unit.
- The accumulation rates of Bronze, Silver, and Gold are multiplied by 1.5^Computronium after ascension.

# Known Isseues
- Scaling of target gold for ascension is more than logarithmic.
- "buy" lines are supposed to be bold when a mine is available for purchase, but are not.
- The real cost deducted by silver_cost and gold_cost is less than the cost displayed.
- [Beta] Beta still has -d / --debug mode flag for addig a multiplier to speed up the game.
