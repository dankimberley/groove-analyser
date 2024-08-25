import librosa
import numpy as np
from datetime import datetime
import json
import os

import grid
import logic

AUDIO_PATH = "api/snare.mp3"
AMPLITUDE_THRESHOLD = -25
os.makedirs('api/outputs', exist_ok=True)
file_name = os.path.join('api/outputs', datetime.now().strftime("%Y%m%d_%H%M%S") + '.json')

# convert a given amplitude to decibels
def amplitude_to_db(amplitude):
    epsilon = 1e-10
    return round(20 * np.log10(np.maximum(amplitude, epsilon)), 1)

# convert an audio file into an array of time objects, x: time (ms), y: amplitude (db)
def audio_to_millisecond_amplitude(audio_path):
    
    y, sr = librosa.load(audio_path, sr=None)
    samples_per_ms = sr // 1000
    amplitudes = []
    
    # Calculate amplitude for each millisecond
    for ms in range(0, len(y) // samples_per_ms):
        start = ms * samples_per_ms
        end = start + samples_per_ms
        amplitude = np.abs(y[start:end]).mean()
        if (amplitude > 0):
            amplitudes.append({"time": ms, "amplitude": amplitude_to_db(amplitude)})

    
    return amplitudes

# extract peaks from a set of amplitudes, peak defined as the greatest amplitude out of the +/- 10 milliseconds
def find_peaks(data, window_size=20, min_distance=10):
    peaks = []
    n = len(data)
    last_peak_index = -min_distance  # Initialize to allow first peak to be detected

    for i in range(n):
        if i - last_peak_index < min_distance:
            continue  # Skip if we're too close to the last detected peak

        start = max(0, i - window_size)
        end = min(n, i + window_size + 1)
        value = data[i]['amplitude']
        surrounding_values = [data[j]['amplitude'] for j in range(start, end) if j != i]
        
        if all(value >= surrounding_value for surrounding_value in surrounding_values):
            if value > AMPLITUDE_THRESHOLD:
                peaks.append(data[i])
                last_peak_index = i  # Update the last peak index

    return peaks

def get_times_from_points(peaks):
    times = []
    for point in peaks:
        times.append(point['time'])
    return times

def get_amplitudes_from_points(peaks):
    amplitudes = []
    for point in peaks:
        amplitudes.append(point['amplitude'])
    return amplitudes

def write_to_json(data):
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print('File has been saved as ' + file_name)
    

peaks = find_peaks(audio_to_millisecond_amplitude(AUDIO_PATH))
# print(peaks)

# print('Input times')
input_times = get_times_from_points(peaks)
# print(input_times)

# print('Grid times')
test_grid = grid.generate_grid(100, 16, input_times[0])
# print(test_grid)

test = logic.compare_timing(input_times, test_grid)
print('Comparison returns: ')
print(test)
print('Relative')
print(logic.convert_abs_to_rel(test, 100))
print(f'Average timing difference is {logic.get_average(test)}ms')