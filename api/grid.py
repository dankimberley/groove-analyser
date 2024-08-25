# given a tempo, first beat, and length (in beats), return an array of timing points. e.g. generate_grid(120, 4, 100) returns [100, 400, 700, 1000]
def generate_grid(tempo, length, first=0):
    beat = bpm_to_ms(tempo)
    grid = []
    for i in range(length):
        if (i == 0): grid.append(first)
        else:
            grid.append(round((first + beat * i), 1))
    return grid

def bpm_to_ms(tempo):
    return 60000 / tempo

test1 = generate_grid(138, 8, 100)
print(test1)