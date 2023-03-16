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
        stdscr.timeout(100)

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
        buffer = curses.newpad(20, 80)  # Create an off-screen buffer with enough size to fit all elements

        buffer.addstr(0, 0, f"Bronze: {int(self.bronze.count)}")
        buffer.addstr(1, 0, f"Silver: {int(self.silver.count)}")
        buffer.addstr(2, 0, f"Gold: {int(self.gold.count)}")
        buffer.addstr(3, 0, f"Computronium: {self.computronium:.2f}")

        bronze_rate = self.bronze.rate * 1000 / 100
        buffer.addstr(5, 0, f"Bronze Mines: {self.bronze_mine.quantity} ({bronze_rate:.2f} Bronze/s)")

        silver_cost = 10 * self.silver_mine.quantity
        silver_rate = self.silver.rate * 1000 / 100
        buffer.addstr(6, 0, f"Silver Mines: {self.silver_mine.quantity} ({silver_rate:.2f} Silver/s)")

        gold_cost = 10 * self.gold_mine.quantity
        gold_rate = self.gold.rate * 1000 / 100
        buffer.addstr(7, 0, f"Gold Mines: {self.gold_mine.quantity} ({gold_rate:.2f} Gold/s)")

        buffer.addstr(9, 0, f"Ascension Target: {self.ascension_target} Gold")
        buffer.addstr(10, 0, f"Ascended: {self.ascended}")

        buffer.addstr(16, 0, "Press 'q' to quit")

        buy_bronze_mine_attr = curses.A_BOLD if self.bronze.count >= self.bronze_mine.cost else curses.A_NORMAL
        buffer.addstr(12, 0, f"Press 'b' to buy a Bronze Mine for {self.bronze_mine.cost} Bronze", buy_bronze_mine_attr)

        buy_silver_mine_attr = curses.A_BOLD if (self.silver_mine.quantity == 0 and self.bronze.count >= self.silver_mine.cost) or (self.silver_mine.quantity > 0 and self.silver.count >= silver_cost) else curses.A_NORMAL

        if self.silver_mine.quantity == 0:
            buffer.addstr(13, 0, f"Press 's' to buy a Silver Mine for {self.silver_mine.cost} Bronze", buy_silver_mine_attr)
        else:
            buffer.addstr(13, 0, f"Press 's' to buy a Silver Mine for {silver_cost} Silver", buy_silver_mine_attr)

        buy_gold_mine_attr = curses.A_BOLD if (self.gold_mine.quantity == 0 and self.silver.count >= self.gold_mine.cost) or (self.gold_mine.quantity > 0 and self.gold.count >= gold_cost) else curses.A_NORMAL

        if self.gold_mine.quantity == 0:
            buffer.addstr(14, 0, f"Press 's' to buy a Gold Mine for {self.gold_mine.cost} Silver", buy_gold_mine_attr)
        else:
            buffer.addstr(14, 0, f"Press 's' to buy a Gold Mine for {gold_cost} Gold", buy_gold_mine_attr)

        buffer.refresh(0, 0, 0, 0, 20, 80)  # Copy the buffer to the main screen
        stdscr.refresh()  # Refresh the main screen

    def update_resources(self):
        delta_time = 1.0
        bronze_boost = 2 ** self.silver_mine.quantity if self.silver_mine.quantity > 0 else 1
        self.bronze.rate = self.bronze_mine.quantity * bronze_boost
        self.bronze.update(delta_time)

        silver_boost = 2 ** self.gold_mine.quantity if self.gold_mine.quantity > 0 else 1
        if self.silver_mine.quantity > 0:
            self.silver.rate = self.silver_mine.quantity * 0.1 * silver_boost
            self.silver.update(delta_time)
        else:
            self.silver.rate = 0

        if self.gold_mine.quantity > 0:
            self.gold.rate = self.gold_mine.quantity * 0.01
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
            silver_cost = 10 * self.silver_mine.quantity
            if self.silver.count >= silver_cost:
                self.silver.count -= silver_cost
                self.silver_mine.purchase()

    def purchase_gold_mine(self):
        if self.gold_mine.quantity == 0:
            if self.silver.count >= self.gold_mine.cost:
                self.silver.count -= self.gold_mine.cost
                self.gold_mine.purchase()
        else:
            gold_cost = 10 * self.gold_mine.quantity
            if self.gold.count >= gold_cost:
                self.gold.count -= gold_cost
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
