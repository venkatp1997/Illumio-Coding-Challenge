'''
Simple utility function to check if two ranges overlap.
'''
def overlap(x1, x2, y1, y2):
    return not((x2 < y1) or (y2 < x1))

