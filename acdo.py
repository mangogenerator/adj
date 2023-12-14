#!/usr/bin/env python3

from datetime import datetime
import random
import csv
import statistics
import math

def read_days(filename):
    days = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            date, day_of_week, weight = row
            days.append((date, day_of_week, float(weight)))
    return days

def read_persons(filename):
    with open(filename, 'r') as file:
        persons = [line.strip() for line in file]
    random.shuffle(persons)
    return persons

def calculate_standard_deviation(assignments):
    weights = [weight for duties in assignments.values() for _, _, weight in duties]
    return statistics.stdev(weights)

def assign_duties(persons, days):
    person_assignments = {person: [] for person in persons}
    sorted_days = sorted(days, key=lambda x: (x[2], x[0]), reverse=True)
    
    acdos_per_day = 2
    
    for day, day_of_week, weight in sorted_days:
        available_persons = [person for person in person_assignments if all(not is_within_8_days(duty, (day, day_of_week, weight)) for duty in person_assignments[person])]
        
        chosen_persons = []
        for _ in range(acdos_per_day):
            if available_persons:
                available_persons.sort(key=lambda p: calculate_total_weight(person_assignments[p]))
                chosen_person = available_persons.pop(0)
                chosen_persons.append(chosen_person)
        
        for chosen_person in chosen_persons:
            person_assignments[chosen_person].append((day, day_of_week, weight))
    
    return person_assignments


def calculate_total_weight(duties):
    return sum(weight for _, _, weight in duties)

def is_within_8_days(duty1, duty2):
    date1 = datetime.strptime(duty1[0], '%d%b')
    date2 = datetime.strptime(duty2[0], '%d%b')
    return abs((date2 - date1).days) <= 5


def calculate_range(assignments):
    total_points = [sum(weight for _, _, weight in duties) for duties in assignments.values()]
    return max(total_points) - min(total_points)

def write_assignments(filename, assignments):
    with open(filename, 'w') as file:
        for person, duties in assignments.items():
            total_weight = sum(weight for _, _, weight in duties)
            file.write(f"{person}:\t{total_weight:.2f}\n")
            
def write_watchbill(filename, assignments):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "DayOfWeek", "Weight", "ACDO 1", "ACDO 2"])
        
        all_duties = [(day, day_of_week, weight, person) for person, duties in assignments.items() for day, day_of_week, weight in duties]
        sorted_duties = sorted(all_duties, key=lambda x: (datetime.strptime(x[0], '%d%b'), x[2]))
        
        current_date = None
        acdo_list = []
        
        for day, day_of_week, weight, person in sorted_duties:
            if day != current_date:
                if acdo_list:
                    writer.writerow(acdo_list)
                acdo_list = [day, day_of_week, weight, person]
                current_date = day
            else:
                acdo_list.extend([person, ""])
        
        if acdo_list:
            writer.writerow(acdo_list)
            
def write_assignments_by_lastname_csv(filename, assignments):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Person", "Assigned Days"])
        for person, duties in assignments.items():
            writer.writerow([person + ":"])
            sorted_duties = sorted(duties, key=lambda x: (x[0], x[1]))
            for day, day_of_week, weight in sorted_duties:
                writer.writerow(["\t", f"{day}, {day_of_week}, {weight}"])

def main():
    persons = read_persons("acdo.txt")
    days = read_days("days_static.csv")

    sorted_days = sorted(days, key=lambda x: (x[2], x[0]), reverse=True)
    initial_assignments = assign_duties(persons, sorted_days)
    
    write_assignments("ACDO_ASSIGNMENTS.txt", initial_assignments)
    write_assignments_by_lastname_csv("ACDO_ASSIGNMENTS_BY_LASTNAME.txt", initial_assignments)
    write_watchbill("ACDO_WATCHBILL.csv", initial_assignments)
    print(calculate_range(initial_assignments))
    print(calculate_standard_deviation(initial_assignments))
    
if __name__ == "__main__":
    main()

