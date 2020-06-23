def size_format(b):
    unit = ['B','KB','MB','GB','TB']
    i = 0
    while b/1024 >= 1:
        b /= 1024
        i = i+1
    return f"{b:.3f} {unit[i]}"