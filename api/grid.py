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

def get_beats_of_peaks(peaks, grid):
    peaks_with_beats = []
    beat_length = grid[1]['time'] - grid[0]['time']
    print(beat_length)
    for peak in peaks:
        print(f'On {peak}')
        peak_time = peak['time']
        for position in grid:
            grid_time = position['time']
            if (abs(peak_time - grid_time) < beat_length):
                index = grid.index(position)
                if ((abs(peak_time - grid[index+1]['time']) < beat_length) & ((abs(peak_time - grid[index+1]['time'])) < (peak_time - grid_time))):
                    print(f'special case: {(peak_time - grid[index+1]["time"])} is less than {(peak_time - grid_time)}')
                    peaks_with_beats.append({'time': peak['time'], 'amplitude': peak['amplitude'], 'bar': grid[index+1]['bar'], 'position': grid[index+1]['position']})
                    break
                peaks_with_beats.append({'time': peak['time'], 'amplitude': peak['amplitude'], 'bar': position['bar'], 'position': position['position']})
                break
            else:
                print(f'not appending {peak} because {abs(peak_time - grid_time)}')
            
    return peaks_with_beats

    

# test1 = generate_grid(138, 8, 100)
# print(test1)

peaks = [{'time': 2430, 'amplitude': -8.1}, {'time': 3025, 'amplitude': -10.0}, {'time': 3602, 'amplitude': -9.5}, {'time': 9334, 'amplitude': -9.5}]
positions = [{'position': 0, 'time': 2430, 'bar': 1}, {'position': 0.25, 'time': 3030.0, 'bar': 1}, {'position': 0.5, 'time': 3630.0, 'bar': 1}, {'position': 0.75, 'time': 4230.0, 'bar': 1}, {'position': 0, 'time': 4830.0, 'bar': 2}, {'position': 0.25, 'time': 5430.0, 'bar': 2}, {'position': 0.5, 'time': 6030.0, 'bar': 2}, {'position': 0.75, 'time': 6630.0, 'bar': 2}, {'position': 0, 'time': 7230.0, 'bar': 3}, {'position': 0.25, 'time': 7830.0, 'bar': 3}, {'position': 0.5, 'time': 8430.0, 'bar': 3}, {'position': 0.75, 'time': 9030.0, 'bar': 3}, {'position': 0, 'time': 9630.0, 'bar': 4}, {'position': 0.25, 'time': 10230.0, 'bar': 4}, {'position': 0.5, 'time': 10830.0, 'bar': 4}, {'position': 0.75, 'time': 11430.0, 'bar': 4}]

print(get_beats_of_peaks(peaks, positions ))