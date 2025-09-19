#!/usr/bin/env python3
"""
Weekly Shift Scheduler (Python)
Supports: morning, afternoon, evening
Employees provide preference ranking per day (list of shifts in priority order).
Implements constraints:
 - max 1 shift per day per employee
 - max 5 working days per week per employee
 - at least 2 employees per shift per day (randomly fill from eligible)
 - conflict resolution: try alternate same-day preference, then next days
"""

import random
from collections import defaultdict
import csv

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SHIFTS = ["morning", "afternoon", "evening"]
MIN_PER_SHIFT = 2
MAX_DAYS_PER_EMP = 5

random.seed(42)

# ---------- Utility functions ----------
def init_schedule():
    return {day: {shift: [] for shift in SHIFTS} for day in DAYS}

def eligible_pool(employees, assignments, day, exclude_set):
    """Return employees eligible to be assigned on a given day"""
    pool = []
    for name in employees:
        if name in exclude_set:
            continue
        worked_days = len(assignments.get(name, set()))
        if worked_days >= MAX_DAYS_PER_EMP:
            continue
        pool.append(name)
    return pool

# ---------- Scheduling algorithm ----------
def schedule_week(employees):
    """
    employees: dict
      name -> {day: [pref1, pref2, pref3]}
    """
    schedule = init_schedule()
    assignments = defaultdict(set)  # name -> set(days worked)

    for day in DAYS:
        assigned_today = set()

        # Try to give each employee their top preference first
        for name, prefs in employees.items():
            if len(assignments[name]) >= MAX_DAYS_PER_EMP:
                continue
            top_pref = prefs.get(day, SHIFTS)[0]
            if name not in assigned_today and len(schedule[day][top_pref]) < MIN_PER_SHIFT:
                schedule[day][top_pref].append(name)
                assignments[name].add(day)
                assigned_today.add(name)

        # Fill shortages per shift
        for shift in SHIFTS:
            while len(schedule[day][shift]) < MIN_PER_SHIFT:
                pool = eligible_pool(employees, assignments, day, assigned_today)
                if not pool:
                    break
                # Prefer employees with this shift as 2nd/3rd preference
                ranked = []
                for emp in pool:
                    prefs = employees[emp].get(day, SHIFTS)
                    if shift in prefs:
                        ranked.append((prefs.index(shift), emp))
                    else:
                        ranked.append((99, emp))  # low priority if not in prefs
                ranked.sort()
                chosen = ranked[0][1]
                schedule[day][shift].append(chosen)
                assignments[chosen].add(day)
                assigned_today.add(chosen)

        # Conflict resolution: employees unassigned today
        for name, prefs in employees.items():
            if name in assigned_today:
                continue
            if len(assignments[name]) >= MAX_DAYS_PER_EMP:
                continue
            for alt_shift in prefs.get(day, SHIFTS):
                if name not in schedule[day][alt_shift]:
                    schedule[day][alt_shift].append(name)
                    assignments[name].add(day)
                    assigned_today.add(name)
                    break

    return schedule

# ---------- Output ----------
def pretty_print(schedule):
    print("\nFinal weekly schedule:\n" + "=" * 30)
    for day in DAYS:
        print(f"{day}:")
        for shift in SHIFTS:
            workers = schedule[day][shift]
            print(f"  {shift.title():<9}: {', '.join(workers) if workers else '(none)'}")
        print("-" * 30)

# ---------- Load Employees ----------
def load_employees_from_csv(filename):
    employees = {}
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["Name"]
            prefs = {}
            for i, day in enumerate(DAYS, start=1):
                prefs[day] = row[day].split(">")
            employees[name] = prefs
    return employees

# ---------- Main ----------
if __name__ == "__main__":
    employees = load_employees_from_csv(r"/workspaces/Assignment4-control-structure/python-language/employee.csv")
    schedule = schedule_week(employees)
    pretty_print(schedule)
