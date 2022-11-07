import csv
# Define the structure of the data
student_header = ['name', 'age', 'major', 'minor']
# Define the actual data
student_data = ['Jack', 23, 'Physics', 'Chemistry']
# 1. Open a new CSV file
with open('students.csv', 'w') as file:
    # 2. Create a CSV writer
    writer = csv.writer(file)
    # 3. Write data to the file
    writer.writerow(student_header)
    writer.writerow(student_data)