
f_in = open('INPUT.TXT', 'r')
n = int(f_in.read().strip())
f_in.close()

total_sum = 0

for i in range(1, n + 1):
    if n % i == 0:
        total_sum += i

f_out = open('OUTPUT.TXT', 'w')
f_out.write(str(total_sum))
f_out.close()
