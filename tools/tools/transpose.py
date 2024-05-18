def transpose(lst: list[list]) -> list:
    try:
        new_lst = []
        for index in range(len(lst[0])):
            new_sublist = []
            for sublist in lst:
                new_sublist.append(sublist[index])
            new_lst.append(new_sublist)
        return new_lst
    except:
        raise ValueError

if __name__ == '__main__':
    l = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    print(transpose(l))