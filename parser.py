

# import csv

# with open( r"C:\Users\GA\Downloads\output_early.csv", mode='r', newline='') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         print(row)


import csv


# the early lines establish - they first define the what each row consists of - for example, on one line, the BATT format was given, its 5th row was
# voltage and 7th was current - i manually deduced it from the reading the data. 1,3 rows are printing time stamps.
with open(r"C:\Users\GA\Downloads\output_early.csv", mode='r', newline='') as infile:

    reader = csv.reader(infile)

    with open(r"C:\Users\GA\Downloads\current_voltage_early.csv", mode = 'w' , newline = '') as outfile:
        writer = csv.writer(outfile)

         # write header row
        writer.writerow(['Timestamp', 'TimeUS', 'Volt (V)', 'Curr (A)'])
        #print the specifics when the data row is of BAT. 
        for row in reader:
             if row[2] == 'BAT' :
                writer.writerow([row[1], row[3], row[5], row[7]])


# import csv

# results = []

# with open(r"C:\Users\GA\Downloads\output_early.csv", mode='r', newline='') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         if row[2] == 'BAT':
#             timestamp = row[1]
#             time_us   = row[3]
#             volt      = row[5]
#             curr      = row[7]
#             results.append([timestamp, time_us, volt, curr])

# # write output
# with open(r"C:\Users\GA\Downloads\battery_cleaned.csv", mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Timestamp', 'TimeUS', 'Volt (V)', 'Curr (A)'])
#     writer.writerows(results)

# print(f"Done. {len(results)} rows written.")