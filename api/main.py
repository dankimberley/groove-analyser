import librosa
import numpy as np

AUDIO_PATH = "api/metronome.mp3"

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
def find_peaks(data):
    peaks = []
    n = len(data)
    
    for i in range(n):
        start = max(0, i - 10)
        end = min(n, i + 11)
        
        value = data[i]['amplitude']
        
        surrounding_values = [data[j]['amplitude'] for j in range(start, end) if j != i]
        
        if all(value > surrounding_value for surrounding_value in surrounding_values):
            peaks.append(data[i])
    
    return peaks

amplitudes = audio_to_millisecond_amplitude(AUDIO_PATH)
print(find_peaks(amplitudes))