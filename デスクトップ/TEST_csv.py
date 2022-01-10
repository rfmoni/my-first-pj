import csv

print("input file name")

name = input()

f = open(str(name) + '.csv', 'w', newline='')

writer = csv.writer(f)

ini_data = [['Time' , 'RF-A' , ' RF-B']]
writer.writerows(ini_data)
    
while True:
    print("enter number")
    number = input()
    
    if number == 'end':
        f.close()
        break
        
    data = [[str(number) ,'番'],['次は','678910']]
    writer.writerows(data)
    continue