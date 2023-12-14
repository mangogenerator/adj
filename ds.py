#!/usr/bin/env python3

max_days_difference = 8

from datetime import datetime
import random
import csv

def read_days(filename):
    days = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            date, day_of_week, weight = row
            days.append((date, day_of_week, float(weight)))
    return days

def read_people(filename):
    with open(filename, 'r') as file:
        people = [line.strip() for line in file]
    return people

def assign_duties(people, days, max_days_difference):
    assignments = {person: [] for person in people}
    sorted_days = sorted(days, key=lambda x: (x[2], x[0]), reverse=True)
    
    def is_within_max_days(duty1, duty2):
        date1 = datetime.strptime(duty1[0], '%d%b')
        date2 = datetime.strptime(duty2[0], '%d%b')
        return abs((date2 - date1).days) <= max_days_difference
    
    def calculate_total_weight(duties):
        return sum(weight for _, _, weight in duties)
    
    weekends = ['Saturday', 'Sunday']
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    for day, day_of_week, weight in sorted_days:
        if day_of_week in weekends: #prioritize saturday and sunday filling first
            available_people = [person for person in assignments if all(not is_within_max_days(duty, (day, day_of_week, weight)) for duty in assignments[person])]
            if not available_people:
                chosen_person = min(assignments, key=lambda p: calculate_total_weight(assignments[p]))
                assignments[chosen_person].append((day, day_of_week, weight))
            else:
                available_people.sort(key=lambda p: calculate_total_weight(assignments[p]))
                chosen_person = available_people[0]
                assignments[chosen_person].append((day, day_of_week, weight))
    
    for day, day_of_week, weight in sorted_days:
        if day_of_week == 'Friday': #fill fridays after saturdays and sundays
            available_people = [person for person in assignments if all(not is_within_max_days(duty, (day, day_of_week, weight)) for duty in assignments[person])]
            if not available_people:
                chosen_person = min(assignments, key=lambda p: calculate_total_weight(assignments[p]))
                assignments[chosen_person].append((day, day_of_week, weight))
            else:
                available_people.sort(key=lambda p: calculate_total_weight(assignments[p]))
                chosen_person = available_people[0]
                assignments[chosen_person].append((day, day_of_week, weight))
    
    for day, day_of_week, weight in sorted_days:
        if day_of_week in weekdays and day_of_week != 'Friday':
            available_people = [person for person in assignments if all(not is_within_max_days(duty, (day, day_of_week, weight)) for duty in assignments[person])]
            if not available_people: #fill weekdays last
                chosen_person = min(assignments, key=lambda p: calculate_total_weight(assignments[p]))
                assignments[chosen_person].append((day, day_of_week, weight))
            else:
                available_people.sort(key=lambda p: calculate_total_weight(assignments[p]))
                chosen_person = available_people[0]
                assignments[chosen_person].append((day, day_of_week, weight))
    return assignments

def write_watchbill(filename, assignments):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "DayOfWeek", "Weight"] + [f"Person {i}" for i in range(1, len(assignments) + 1)])
        
        all_duties = [(day, day_of_week, weight, person) for person, duties in assignments.items() for day, day_of_week, weight in duties]
        sorted_duties = sorted(all_duties, key=lambda x: (datetime.strptime(x[0], '%d%b'), x[2]))
        
        current_date = None
        person_list = []
        
        for day, day_of_week, weight, person in sorted_duties:
            if day != current_date:
                if person_list:
                    writer.writerow(person_list)
                person_list = [day, day_of_week, weight, person]
                current_date = day
            else:
                person_list.append(person)
        
        if person_list:
            writer.writerow(person_list)
            
def write_duty_section_files(assignments):
    with open("DUTYSECTION_ASSIGNED_DAYS.txt", "w") as file:
        for person, duties in assignments.items():
            file.write(f"{person}:\n")
            
            saturday_count = 0
            sunday_count = 0
            friday_count = 0
            
            for day, day_of_week, weight in duties:
                file.write(f"{day}, {day_of_week}, {weight:.2f}\n")
                
                if day_of_week == "Saturday":
                    saturday_count += 1
                elif day_of_week == "Sunday":
                    sunday_count += 1
                elif day_of_week == "Friday":
                    friday_count += 1
            
            file.write(f"\nTotal Saturdays: {saturday_count}\n")
            file.write(f"Total Sundays: {sunday_count}\n")
            file.write(f"Total Fridays: {friday_count}\n")
            file.write(f"Total Weekend Days: {saturday_count+sunday_count+friday_count}\n\n")

def write_total_points(filename, assignments):
    with open(filename, 'w') as file:
        for person, duties in assignments.items():
            total_weight = sum(weight for _, _, weight in duties)
            file.write(f"{person}:\t{total_weight:.2f}\n")

def main():
    people = read_people("duty_sections.txt")
    days = read_days("days_static.csv")
    assignments = assign_duties(people, days, max_days_difference)
    write_watchbill("DUTYSECTION_WATCHBILL.csv", assignments)
    write_duty_section_files(assignments)
    write_total_points("DUTYSECTION_TOTAL_POINTS.txt", assignments)
    
if __name__ == "__main__":
    main()
