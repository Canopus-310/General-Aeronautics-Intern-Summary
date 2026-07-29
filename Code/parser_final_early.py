import csv

with open(r"C:\Users\GA\Downloads\Readings_Final_early.csv", mode='r', newline='') as infile:

    reader = csv.reader(infile)

    with open(r"C:\Users\GA\Downloads\final_readings_early.csv", mode = 'w' , newline = '') as outfile:
        writer = csv.writer(outfile)

         # write header row
        writer.writerow(['Timestamp', 'TimeUS', 'Volt (V)', 'Curr (A)'])

        for row in reader: 
            if row[2] == 'BAT':
                writer.writerow([row[1] , row[3], row[5], row[7]])