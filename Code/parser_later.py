import csv

with open(r"C:\Users\GA\Downloads\output_later.csv", mode='r', newline='') as infile:

    reader = csv.reader(infile)

    with open(r"C:\Users\GA\Downloads\current_voltage_later.csv", mode = 'w' , newline = '') as outfile:
        writer = csv.writer(outfile)

         # write header row
        writer.writerow(['Timestamp', 'TimeUS', 'Volt (V)', 'Curr (A)'])

        for row in reader: 
            if row[2] == 'BAT':
                writer.writerow([row[1] , row[3], row[7], row[9]])