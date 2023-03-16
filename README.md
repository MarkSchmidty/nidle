# NIDLE - An ncurses-based Idle Game

## Game Overview
NIDLE is a terminal-based idle game that uses ncurses for its interface. Players accumulate resources (Bronze, Silver, Gold, and Computronium) at various rates, which can be increased by purchasing mines. Ascensions become available upon reaching target amounts of Gold, and these ascensions grant Computronium, which further accelerates resource accumulation.

## Resources
There are four resource types in the game:

1. Bronze (integer)
2. Silver (integer)
3. Gold (integer)
4. Computronium (floating point, truncated to 2 decimal places)

Resource counts are displayed and updated every 250ms.

## Resource Accumulation
- Bronze: Gained at a rate of 1 per second. Rate can be increased by purchasing additional Bronze mines.
- Silver: Gained at a rate dependent on the number of Silver mines and amount of Bronze.
- Gold: Gained at a rate dependent on the number of Gold mines and amount of Silver.

## Mines
- Bronze Mine:
  - Starting Quantity: 1
  - Purchase Cost: Increases incrementally with each purchase.
  - First Additional Mine Cost: 100 Bronze
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
- Computronium is granted upon ascension, with the amount increasing as Gold exceeds the target amount.
- Consecutive units of Computronium require twice the Gold of the previous unit.
- The accumulation rates of Bronze, Silver, and Gold increase by a factor of (2 * Computronium obtained) after ascension.
- Ascension targets increase after each ascension:
  - First Ascension: 1 Gold
  - Second Ascension: 2 Gold
  - Subsequent Ascensions: Target doubles with each ascension.

# Known Isseues
- [Beta] "buy" lines are supposed to be bold when a mine is available for purchase, but are not.
- [Beta] The real cost deducted by silver_cost and gold_cost is less than the cost displayed.
- [Beta] Beta still has -d / --debug mode flag for addig a multiplier to speed up the game.
