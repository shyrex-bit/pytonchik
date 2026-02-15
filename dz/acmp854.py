f_in = open('INPUT.TXT', 'r')
line1 = f_in.readline().split()
t_room = int(line1[0])
t_cond = int(line1[1])
mode = f_in.readline().strip()
f_in.close()

if mode == "freeze":
    res = min(t_room, t_cond)
elif mode == "heat":
    res = max(t_room, t_cond)
elif mode == "auto":
    res = t_cond
else: 
    res = t_room

f_out = open('OUTPUT.TXT', 'w')
f_out.write(str(res))
f_out.close()
