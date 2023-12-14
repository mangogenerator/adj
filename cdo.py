#!/usr/bin/env python3

days_between_watch_should_be = 8 #fine-tune this variable if need-be to constrain how many days people should have at minimum, between their duty days. If the program is generating an unfair watchbill, you may need to decrease this number.

from datetime import datetime
import random
import csv


def read_days(filename):
    days = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            date, day_of_week, weight = row
            days.append((date, day_of_week, float(weight)))
    return days

def read_cdos(filename):
    with open(filename, 'r') as file:
        cdos = [line.strip() for line in file]
    random.shuffle(cdos)
    return cdos

def assign_duties(cdos, days):
    cdo_assignments = {cdo: [] for cdo in cdos}
    sorted_days = sorted(days, key=lambda x: (x[2], x[0]), reverse=True)
    
    def is_within_x_days(duty1, duty2):
        date1 = datetime.strptime(duty1[0], '%d%b')
        date2 = datetime.strptime(duty2[0], '%d%b')
        return abs((date2 - date1).days) <= days_between_watch_should_be
    
    def calculate_total_weight(duties):
        return sum(weight for _, _, weight in duties)
    
    for day, day_of_week, weight in sorted_days:
        available_cdos = [cdo for cdo in cdo_assignments if all(not is_within_x_days(duty, (day, day_of_week, weight)) for duty in cdo_assignments[cdo])]
        
        if not available_cdos: # choose with least total weight
            chosen_cdo = min(cdo_assignments, key=lambda c: calculate_total_weight(cdo_assignments[c]))
            cdo_assignments[chosen_cdo].append((day, day_of_week, weight))
        else: # prioritize total weight being less for remaining cdos
            available_cdos.sort(key=lambda c: calculate_total_weight(cdo_assignments[c]))
            chosen_cdo = available_cdos[0]
            cdo_assignments[chosen_cdo].append((day, day_of_week, weight))
    
    return cdo_assignments


def write_assignments(filename, assignments):
    with open(filename, 'w') as file:
        for cdo, duties in assignments.items():
            total_weight = sum(weight for _, _, weight in duties)
            file.write(f"{cdo}:\t{total_weight:.2f}\n")

def write_watchbill(filename, assignments):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "DayOfWeek", "Weight", "CDO"])
        all_duties = [(day, day_of_week, weight, cdo) for cdo, duties in assignments.items() for day, day_of_week, weight in duties]
        sorted_duties = sorted(all_duties, key=lambda x: (datetime.strptime(x[0], '%d%b'), x[2]))
        for day, day_of_week, weight, cdo in sorted_duties:
            writer.writerow([day, day_of_week, weight, cdo])

def write_assignments_by_lastname(filename, assignments):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["CDO", "Assigned Days"])
        for cdo, duties in assignments.items():
            writer.writerow([cdo + ":"])
            sorted_duties = sorted(duties, key=lambda x: (x[0], x[1]))
            for day, day_of_week, weight in sorted_duties:
                writer.writerow(["\t", f"{day}, {day_of_week}, {weight}"])

def main():
    cdos = read_cdos("cdo.txt")
    days = read_days("days_static.csv")

    sorted_days = sorted(days, key=lambda x: (x[2], x[0]), reverse=True)
    cdo_assignments = assign_duties(cdos, sorted_days)

    write_assignments("CDO_ASSIGNMENTS.txt", cdo_assignments)
    write_assignments_by_lastname("CDO_ASSIGNMENTS_BY_LASTNAME.csv", cdo_assignments)
    write_watchbill("CDO_WATCHBILL.csv", cdo_assignments)
    
if __name__ == "__main__":
    main()
