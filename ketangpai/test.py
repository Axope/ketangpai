for ttt in range(int(input())):
    n, m = map(int, input().split())
    v = [input().split() for i in range(n)]
    v.sort(key=lambda t: (int(t[1]), int(t[2]), -len(t[0])), reverse=True)
    ans = [0, 0]
    cnt = {}
    # if n>int(1e3) or m>int(1e3):
    #     test=[([1]*int(1e8)) for i in range(int(1e5))]
    for i in range(n):
        name, atk, level = v[i][0], int(v[i][1]), int(v[i][2])
        # name += "!"+str(atk)+"!"+str(level)
        if name in cnt and cnt[name] >= 3:
            continue
        try:
            cnt[name] += 1
        except:
            cnt[name] = 1
        ans[0], ans[1] = ans[0]+atk, ans[1]+level
        m -= 1
        if m == 0:
            break
    if m>0:
        print("NO")
    else:
        print("YES")
        print("%d %d" % (ans[0], ans[1]))
