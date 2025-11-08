import sounddevice as sd
import numpy as np
def play_async(frequencies, duration=1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate*duration), endpoint=False)
    decay_rate=5/duration
    chord_waveform=np.zeros_like(t)
    for freq in frequencies:
        waveform=sum((1/(i+1))*np.sin(2*np.pi*freq*(i+1)*t) for i in range(5))
        waveform*=np.exp(-decay_rate*t)
        chord_waveform+=waveform
    if np.max(np.abs(chord_waveform))!=0:
        chord_waveform=0.5*chord_waveform/np.max(np.abs(chord_waveform))
    sd.play(chord_waveform, sample_rate)