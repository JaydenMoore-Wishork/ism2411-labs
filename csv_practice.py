#Reflection
#1. In Excel I can open sales.csv and filter a total column by hand which isnt the worst for smaller files. But for a large file or multiple files the python script can do it for me. Excel is definitely easier for people who cant code or if its just a little bit of data but python shines when you need to repeat or do a larger task.
#2. A real world example of append mode use could be a POS system. It would be useful in any retail store or e comerce system. It adds a single line at the very bottom to the file when a cashier cans the iteim and processes the payment instead of rewriting the whole file. Its the right tool because it has high write speed, guaranteed data preservation, and crash resilience.

import csv
import os
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"


# Exercise 1

print("=== Exercise 1: Setup ===")
if os.path.exists(SALES_FILE):
    with open(SALES_FILE, "r") as f:
        line_count = sum(1 for _ in f)
    print(f"Found {SALES_FILE} ({line_count - 1} data rows + 1 header row)")
else:
    raise FileNotFoundError(
        f"{SALES_FILE} not found. Run this script from the ism2411-lab12 folder."
    )
print()


# Exercise 2

print("=== Exercise 2: Raw rows ===")
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
print()


# Exercise 3

print("=== Exercise 3: Header skipped ===")
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)
print()


# Exercise 4

print("=== Exercise 4: Totals ===")
total_revenue = 0.0
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:,.2f}")
print(f"Total revenue: ${total_revenue:,.2f}")
print()


# Exercise 5

print("=== Exercise 5: Filter and write ===")
original_count = 0
written_count = 0
with open(SALES_FILE, "r", newline="") as infile, \
        open(CLEANED_FILE, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)  # skip header
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in reader:
        original_count += 1
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        if line_total > 100:
            writer.writerow([row[0], f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1
print(f"Wrote {written_count} of {original_count} rows to {CLEANED_FILE}")
print()


# Exercise 6

# csv.reader returns each row as data. While the csv.DictReader returns each row as a dictionary. The csv.DictReader is easier to understand when columns might move or there are many of them.

print("=== Exercise 6: DictReader ===")
dict_total = 0.0
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:,.2f}")
print(f"Total revenue: ${dict_total:,.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))
print()


# Exercise 7

print("=== Exercise 7: Summary by product ===")
summary = {}
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["product"]
        line_total = float(row["price"]) * int(row["quantity"])
        summary[name] = summary.get(name, 0) + line_total
for name in sorted(summary):
    print(f"{name}: ${summary[name]:,.2f}")
print()


# Exercise 8

print("=== Exercise 8: Append log ===")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    log.write(f"{timestamp} | total revenue: ${total_revenue:,.2f}\n")
with open(LOG_FILE, "r") as log:
    entries = log.readlines()
print(f"Appended to {LOG_FILE} — it now has {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}")
