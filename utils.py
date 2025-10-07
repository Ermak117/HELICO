
import random

def randbool(r, mxr):
    return random.randint(1, mxr) <= r

def randcell(w, h):
    return random.randrange(w), random.randrange(h)

def randcell2(x, y):
    return random.choice([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])