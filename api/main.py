import librosa
import numpy as np
from datetime import datetime
import json
import os

import grid
import logic

AUDIO_PATH = "api/inputs/120bass.mp3"
SECOND_AUTO_PATH = "api/inputs/120drums.mp3"
AMPLITUDE_THRESHOLD = -40
os.makedirs('api/outputs', exist_ok=True)
# file_name = os.path.join('api/outputs', datetime.now().strftime("%Y%m%d_%H%M%S") + '.json')
file_name = os.path.join('api/outputs', 'output' + '.json')

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

def detect_transients(data, threshold=-25):
    transients = []
    i = 1
    while i < len(data):
        current_amplitude = data[i]['amplitude']
        current_time = data[i]['time']
        if current_amplitude > threshold:
            if current_amplitude - data[i-10]['amplitude'] > 5: # check transient is significant
                if data[i+1]['amplitude'] - current_amplitude < 5: # check transient does not rise significantly more
                    transients.append({'time': current_time, 'amplitude': current_amplitude})
                    i += 250
                    continue
                    
        i += 1
    
    return transients

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
    
def every_x(data, x):
    filtered = []
    total = 0
    i = 0  # Initialize i to 0 to correctly count elements

    for datum in data:
        total += datum['amplitude']  # Accumulate the amplitude
        i += 1  # Increment the counter

        if i == x:  # If we've accumulated x elements
            average_amplitude = total / x  # Calculate the average
            filtered.append({'time': datum['time'], 'amplitude': average_amplitude})
            total = 0  # Reset the total for the next group
            i = 0  # Reset the counter for the next group

    return filtered
            
    
amplitudes = audio_to_millisecond_amplitude(AUDIO_PATH)
peaks = detect_transients(amplitudes)
print('Peaks ')
print(peaks)


input_times = get_times_from_points(peaks)
test_grid = grid.generate_grid(120, 20, input_times[0])


peaks_and_beats = grid.get_beats_of_peaks(peaks, test_grid)
print('peaks and beats:')
print(peaks_and_beats)

drum_amplitudes = audio_to_millisecond_amplitude(SECOND_AUTO_PATH)
drum_peaks = detect_transients(drum_amplitudes)
drum_times = get_times_from_points(drum_peaks)
drum_beats = grid.get_beats_of_peaks(drum_peaks, grid.generate_grid(120, 20, drum_times[0]))

json_data = {"points": peaks_and_beats, "grid": drum_beats, 'amplitudes': every_x(amplitudes, 5)}
write_to_json(json_data)


test = logic.compare_timing(input_times, test_grid)
print('Comparison returns: ')
print(test)
print('Relative')
print(logic.convert_abs_to_rel(test, 100))
print(f'Average timing difference is {logic.get_average(test)}ms')
print(test_grid)