#!/usr/bin/env python3

import curses
import time

class Resource:
    def __init__(self, rate, count):
        self.rate = rate
        self.count = count

    def update(self, delta_time):
        self.count += self.rate * delta_time

class Mine:
    def __init__(self, cost, cost_multiplier):
        self.cost = cost
        self.cost_multiplier = cost_multiplier
        self.quantity = 0

    def purchase(self):
        self.quantity += 1
        self.cost = int(self.cost * self.cost_multiplier)

class NIDLE:
    def __init__(self):
        self.bronze = Resource(rate=1, count=0)
        self.silver = Resource(rate=0, count=0)
        self.gold = Resource(rate=0, count=0)
        self.computronium = 0.0

        self.bronze_mine = Mine(cost=100, cost_multiplier=1.5)
        self.silver_mine = Mine(cost=1000, cost_multiplier=1.5)
        self.gold_mine = Mine(cost=1000, cost_multiplier=1.5)

        self.ascension_target = 1
        self.ascended = 0

    def main(self, stdscr):
        stdscr.nodelay(1)
        stdscr.timeout(250)

        self.bronze_mine.quantity = 1

        while True:
            key = stdscr.getch()

            if key == ord('q'):
                break

            self.input_handler(key)
            self.update_resources()
            self.check_ascension()
            self.draw_interface(stdscr)

    def draw_interface(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Bronze: {int(self.bronze.count)}")
        stdscr.addstr(1, 0, f"Silver: {int(self.silver.count)}")
        stdscr.addstr(2, 0, f"Gold: {int(self.gold.count)}")
        stdscr.addstr(3, 0, f"Computronium: {self.computronium:.2f}")

        stdscr.addstr(5, 0, f"Bronze Mines: {self.bronze_mine.quantity} (Buy: {self.bronze_mine.cost} Bronze)")
        stdscr.addstr(6, 0, f"Silver Mines: {self.silver_mine.quantity} (Buy: {self.silver_mine.cost} Bronze, 10 Silver)")
        stdscr.addstr(7, 0, f"Gold Mines: {self.gold_mine.quantity} (Buy: {self.gold_mine.cost} Silver, 10 Gold)")

        stdscr.addstr(9, 0, f"Ascension Target: {self.ascension_target} Gold")
        stdscr.addstr(10, 0, f"Ascended: {self.ascended}")

        stdscr.addstr(12, 0, "Press 'q' to quit")
        stdscr.addstr(13, 0, "Press 'b' to buy a Bronze Mine")
        stdscr.addstr(14, 0, "Press 's' to buy a Silver Mine")
        stdscr.addstr(15, 0, "Press 'g' to buy a Gold Mine")

        stdscr.refresh()

    def update_resources(self):
        delta_time = 2.0
        self.bronze.update(delta_time)

        if self.silver_mine.quantity > 0:
            self.silver.rate = self.bronze_mine.quantity * 0.1
            self.silver.update(delta_time)
        else:
            self.silver.rate = 0

        if self.gold_mine.quantity > 0:
            self.gold.rate = self.silver_mine.quantity * 0.01
            self.gold.update(delta_time)
        else:
            self.gold.rate = 0

    def input_handler(self, key):
        if key == ord('b'):
            self.purchase_bronze_mine()
        elif key == ord('s'):
            self.purchase_silver_mine()
        elif key == ord('g'):
            self.purchase_gold_mine()

    def purchase_bronze_mine(self):
        if self.bronze.count >= self.bronze_mine.cost:
            self.bronze.count -= self.bronze_mine.cost
            self.bronze_mine.purchase()

def purchase_silver_mine(self):
    if self.silver_mine.quantity == 0:
        if self.bronze.count >= self.silver_mine.cost:
            self.bronze.count -= self.silver_mine.cost
            self.silver_mine.purchase()
    else:
        if self.silver.count >= self.silver_mine.cost:
            self.silver.count -= self.silver_mine.cost
            self.silver_mine.purchase()

def purchase_gold_mine(self):
    if self.gold_mine.quantity == 0:
        if self.silver.count >= self.gold_mine.cost:
            self.silver.count -= self.gold_mine.cost
            self.gold_mine.purchase()
    else:
        if self.gold.count >= self.gold_mine.cost:
            self.gold.count -= self.gold_mine.cost
            self.gold_mine.purchase()

    def check_ascension(self):
        if self.gold.count >= self.ascension_target:
            self.ascend()

    def ascend(self):
        self.computronium += 1
        self.gold.count -= self.ascension_target
        self.ascension_target *= 2
        self.ascended += 1

        self.bronze.rate *= (2 * self.computronium)
        self.silver.rate *= (2 * self.computronium)
        self.gold.rate *= (2 * self.computronium)

if __name__ == '__main__':
    curses.wrapper(NIDLE().main)
