def flattenList(l):
    l_flattened = []
    for item in l:
        if type(item) is list:
            l_flattened.extend(flattenList(item))
        else:
            l_flattened.append(item)
    return l_flattened
