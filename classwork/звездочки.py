def solve():
    n = int(input())
    ans = float('inf')
    for m in range(1, n + 1):
        # k_min возможное
        k_min = (n + m - 1) // m  # ceil(n/m)
        # перебираем k от k_min до n (k не может быть больше n)
        # но достаточно до n, т.к. дальше разность растет
        for k in range(k_min, n + 1):
            # n = a*k + (m-a)*(k-1) = m*(k-1) + a
            a = n - m * (k - 1)
            b = m - a
            if 0 <= a <= m:
                if a == 0 or a == m:
                    ans = min(ans, abs(m - k))
                    break
                if abs(2 * a - m) <= 1:
                    ans = min(ans, abs(m - k))
                    break
    print(ans)

if __name__ == "__main__":
    solve()