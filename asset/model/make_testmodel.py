for i in range(50):
    for j in range(50):
        for k in range(50):
            if (20 < i < 30) and (20 < j < 30) and (20 < k < 30):
                print('{} {} {} {}'.format(i, j, k, 1))
            else:            
                print('{} {} {} {}'.format(i, j, k, 0))