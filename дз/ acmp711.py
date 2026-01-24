f_in = open('INPUT.TXT', 'r')

line1 = f_in.readline().split()
n = int(line1[0])
m = int(line1[1])

best_time = float('inf') 
winner_name = ""

for _ in range(n):
    name = f_in.readline().strip()  
    current_total_time = 0
    
   
    for _ in range(m):
        lap_time = int(f_in.readline().strip())
        current_total_time += lap_time
    

    if current_total_time < best_time:
        best_time = current_total_time
        winner_name = name

f_in.close()


f_out = open('OUTPUT.TXT', 'w')
f_out.write(winner_name)
f_out.close()
