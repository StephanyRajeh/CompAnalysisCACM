def orderCommunities(c):
    i = 0
    keys_partition = list()
    for j in c:
        keys_partition.append(i)
        i = i + 1

    partition = dict()
    for i in keys_partition:
        partition[i] = []


    i = 0
    for j in c:
        for k in c[j]:
            partition[i].append(k)
        i = i + 1

    return partition


def communityInfo(c, partition):
    print('Number of partitions: ', len(partition))
    l = list()
    for i in c:
        for j in c[i]:  
            l.append(j)

    print('Number of nodes in the communities detected: ', len(l))

    s = set(l)
    print('Number of repetitions: ', len(l) - len(s))
    print()
    print()


