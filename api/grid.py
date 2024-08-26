# given a tempo, first beat, and length (in beats), return an array of timing points. e.g. generate_grid(120, 4, 100) returns [100, 400, 700, 1000]
def generate_grid(tempo, length, first=0):
    beat = bpm_to_ms(tempo)
    grid = []
    position = 0
    bar = 1
    for i in range(length):
        if (i == 0): grid.append({'position': 0, 'time':(first), 'bar': bar})
        else:
            grid.append({'position': position, 'time':(first + beat * i), 'bar': bar})
        if (position == 0.75):
            position = 0
            bar += 1
        else:
            position += 0.25
    return grid

def bpm_to_ms(tempo):
    return 60000 / tempo

def get_times_from_grid(grid):
    grid_times = []
    for time in grid:
        grid_times.append(time['time'])
    return grid_times

# test1 = generate_grid(138, 8, 100)
# print(test1)