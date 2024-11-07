import csv

averages = []
with open('student_grades.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row['Name']
        maths = int(row['Maths'])
        science = int(row['Science'])
        english = int(row['English'])
        avg = (maths + science + english) / 3
        averages.append([name, avg])

with open('student_grades_average.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Average'])
    writer.writerows(averages)

print("student_grades_average.csv created successfully.")