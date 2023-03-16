#!/usr/bin/env python3
import curses,time, argparse

class Resource:
    def __init__(self, rate, count):
        self.rate = rate
        self.count = count

    def update(self, delta_time):
        self.count += self.rate * delta_time

class Mine:
    def __init__(self, cost, cost_multiplier):
        self.base_cost = cost  # Add this line to store the initial cost
        self.cost = cost
        self.cost_multiplier = cost_multiplier
        self.quantity = 0

    def purchase(self):
        self.quantity += 1
        self.cost = int(self.cost * self.cost_multiplier)

    def reset_cost(self):  # Add this method to reset the cost to the initial value
        self.cost = self.base_cost

class NIDLE:
    def __init__(self, delta_multiplier=1.0):
        self.delta_multiplier = delta_multiplier
        self.bronze = Resource(rate=1, count=0)
        self.silver = Resource(rate=0, count=0)
        self.gold = Resource(rate=0, count=0)
        self.computronium = 0.0
        self.potential_computronium = 0.0

        self.bronze_mine = Mine(cost=10, cost_multiplier=1.5)
        self.silver_mine = Mine(cost=1000, cost_multiplier=1.5)
        self.gold_mine = Mine(cost=1000, cost_multiplier=1.5)

        self.ascension_target = 10
        self.ascended = 0

    def main(self, stdscr):
        stdscr.nodelay(1)
        stdscr.timeout(50)

        self.bronze_mine.quantity = 1

        while True:
            key = stdscr.getch()

            if key == ord('q'):
                break

            self.input_handler(key)
            self.update_resources()
            self.check_ascension()
            self.draw_interface(stdscr)

    def format_large_number(self, number, decimal_places=0):
        if number == float('inf'):
            return "Infinity"
        if number >= 1e12:
            return f"{number:.4e}"
        else:
            return f"{number:.{decimal_places}f}"
        
    def draw_interface(self, stdscr):
        screen_height, screen_width = stdscr.getmaxyx()

        # Ensure a minimum size for the screen
        if screen_height < 25 or screen_width < 80:
            stdscr.clear()
            stdscr.addstr(0, 0, "Please increase the terminal size.")
            stdscr.refresh()
            return

        buffer = curses.newpad(screen_height, screen_width)

        # Initialize variables
        line_number = 0
        blank_lines = 0

        def add_line(line_content):
            nonlocal line_number, blank_lines
            if not line_content.strip():
                blank_lines += 1
            else:
                blank_lines = 0

            if blank_lines <= 2:
                buffer.addstr(line_number, 0, line_content)
                line_number += 1

        add_line(f"Bronze: {self.format_large_number(self.bronze.count)}")
        if self.silver_mine.quantity > 0:
            add_line(f"Silver: {self.format_large_number(self.silver.count)}")
        if self.gold_mine.quantity > 0:
            add_line(f"Gold: {self.format_large_number(self.gold.count)}")
        add_line("")

        ascension_multiplier = 1.5 ** (1 + self.computronium) if self.computronium > 0 else 1        
        if self.computronium >= 1:
            add_line(f"Computronium: {self.computronium:.2f} ({ascension_multiplier:.2f}x bonus to mines)")
        add_line("")

        if self.potential_computronium >= 1:
            add_line(f"Potential Computronium: {self.potential_computronium:.2f} (Ascend to claim)")
        add_line("")

        bronze_rate = self.bronze.rate
        add_line(f"Bronze Mines: {self.format_large_number(self.bronze_mine.quantity)} ({self.format_large_number(bronze_rate, 4)} Bronze/s)")

        silver_rate = 0
        if self.silver_mine.quantity >= 1:
            silver_cost = 10 * self.silver_mine.quantity
            silver_rate = self.silver.rate
        add_line(f"Silver Mines: {self.format_large_number(self.silver_mine.quantity)} ({self.format_large_number(silver_rate, 4)} Silver/s)")

        gold_rate = 0
        if self.gold_mine.quantity >= 1:
            gold_cost = 10 * self.gold_mine.quantity
            gold_rate = self.gold.rate
            add_line(f"Gold Mines: {self.format_large_number(self.gold_mine.quantity)} ({self.format_large_number(gold_rate, 4)} Gold/s)")
        add_line("")

        if self.ascended > 0 or self.gold_mine.quantity > 0:
            add_line(f"Ascension Target: {self.format_large_number(self.ascension_target)} Gold")
            add_line(f"Ascended: {self.format_large_number(self.ascended)}")
        add_line("")

        buy_bronze_mine_attr = curses.A_BOLD if self.bronze.count >= self.bronze_mine.cost else curses.A_NORMAL
        add_line(f"Press 'b' to buy a Bronze Mine for {self.format_large_number(self.bronze_mine.cost)} Bronze")

        buy_silver_mine_attr = curses.A_BOLD if (self.silver_mine.quantity == 0 and self.bronze.count >= self.silver_mine.cost) or (self.silver_mine.quantity > 0 and self.silver.count >= silver_cost) else curses.A_NORMAL

        if self.silver_mine.quantity == 0:
            add_line(f"Press 's' to buy a Silver Mine for {self.format_large_number(self.silver_mine.cost)} Bronze")
        else:
            add_line(f"Press 's' to buy a Silver Mine for {self.format_large_number(silver_cost)} Silver")

        buy_gold_mine_attr = curses.A_BOLD if (self.gold_mine.quantity == 0 and self.silver.count >= self.gold_mine.cost) or (self.gold_mine.quantity > 0 and self.gold.count >= gold_cost) else curses.A_NORMAL

        if self.silver_mine.quantity > 0:
            if self.gold_mine.quantity == 0:
                add_line(f"Press 'g' to buy a Gold Mine for {self.format_large_number(self.gold_mine.cost)} Silver")
            else:
                add_line(f"Press 'g' to buy a Gold Mine for {self.format_large_number(gold_cost)} Gold")


        add_line("")

        perform_ascension_attr = curses.A_BOLD if self.potential_computronium > 0 else curses.A_NORMAL
        add_line(f"Press 'a' to perform Ascension")

        add_line("")

        add_line("Press 'q' to quit")

        buffer.refresh(0, 0, 0, 0, screen_height - 1, screen_width - 1)  # Copy the buffer to the main screen
        stdscr.refresh()  # Refresh the main screen

    def update_resources(self):
        delta_time = 0.05 * self.delta_multiplier
        ascension_multiplier = 1.5 ** (1 + self.computronium) if self.computronium > 0 else 1
        bronze_boost = (1.02 ** int(self.silver.count) if self.silver_mine.quantity > 0 else 1) * ascension_multiplier
        self.bronze.rate = self.bronze_mine.quantity * bronze_boost
        self.bronze.update(delta_time)

        silver_boost = (1.02 ** int(self.gold.count) if self.gold_mine.quantity > 0 else 1) * ascension_multiplier
        if self.silver_mine.quantity > 0:
            self.silver.rate = self.silver_mine.quantity * 0.1 * silver_boost
            self.silver.update(delta_time)
        else:
            self.silver.rate = 0

        if self.gold_mine.quantity > 0:
            self.gold.rate = self.gold_mine.quantity * 0.01 * ascension_multiplier
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
        elif key == ord('a'):
            self.perform_ascension()

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
            self.add_potential_computronium()

    def add_potential_computronium(self):
        self.potential_computronium += 1
        self.ascension_target **= 2

    def perform_ascension(self):
        if self.potential_computronium > 0:
            self.computronium += self.potential_computronium
            self.potential_computronium = 0
            self.ascended += 1

            self.reset_resources_and_mines()

    def reset_resources_and_mines(self):
        self.bronze.count = 0
        self.silver.count = 0
        self.gold.count = 0

        self.bronze_mine.quantity = 1
        self.silver_mine.quantity = 0
        self.gold_mine.quantity = 0

        self.bronze_mine.reset_cost()  # Call the reset_cost method for each mine
        self.silver_mine.reset_cost()
        self.gold_mine.reset_cost()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', type=float, default=1.0, help='Specify a multiplier for delta_time')
    args = parser.parse_args()

    delta_multiplier = args.debug
    curses.wrapper(NIDLE(delta_multiplier).main)
