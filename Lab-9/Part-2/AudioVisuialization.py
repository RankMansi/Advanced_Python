import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

# 1. Audio Loading and Visualization
def load_and_visualize_audio(file_path):
    # Load the audio file
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    
    # Visualize the waveform
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(audio_data, sr=sample_rate)
    plt.title("Waveform of Audio")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()
    
    return audio_data, sample_rate

# 2. Audio Manipulation

# 2.1 Change Playback Speed (Fixed)
def change_playback_speed(audio_data, sample_rate, rate=1.5):
    # Compute the Short-Time Fourier Transform (STFT)
    stft_data = librosa.stft(audio_data)
    
    # Time-stretch the STFT
    stft_stretched = librosa.phase_vocoder(stft_data, rate=rate)
    
    # Convert back to audio signal
    manipulated_audio = librosa.istft(stft_stretched)
    
    # Visualize the manipulated audio
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(manipulated_audio, sr=sample_rate)
    plt.title(f"Waveform after Speed Change (Rate={rate})")
    plt.show()
    
    return manipulated_audio

# 2.2 Apply Echo Effect
def apply_echo(audio_data, sample_rate, delay=0.2, decay=0.4):
    # Create an echo effect by delaying the audio and decaying the amplitude
    delay_samples = int(delay * sample_rate)
    echo_audio = np.zeros(len(audio_data) + delay_samples)
    echo_audio[:len(audio_data)] = audio_data
    echo_audio[delay_samples:] += decay * audio_data
    return echo_audio

# 3. Spectral Analysis (Spectrogram)
def display_spectrogram(audio_data, sample_rate):
    # Compute the Short-Time Fourier Transform (STFT)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)
    
    # Display the spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D, sr=sample_rate, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.show()

# 4. Clipping Audio Segment
def clip_audio(audio_data, start_time, end_time, sample_rate):
    # Clip a segment of the audio
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)
    clipped_audio = audio_data[start_sample:end_sample]
    
    # Visualize the clipped audio
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(clipped_audio, sr=sample_rate)
    plt.title(f"Clipped Audio from {start_time}s to {end_time}s")
    plt.show()
    
    return clipped_audio

# Full Example Usage
if __name__ == "__main__":
    print("Rank Mansi")
    print("22BCP284")

    file_path = 'Lab-9/Part-2/seventeen_rington.mp3'  # Replace with your actual file path
    
    # Step 1: Load and visualize audio
    audio_data, sample_rate = load_and_visualize_audio(file_path)
    
    # Step 2: Manipulate audio (change speed, apply echo)
    manipulated_audio = change_playback_speed(audio_data, sample_rate, rate=1.2)
    
    # Step 3: Apply echo (optional, no visual update)
    echo_audio = apply_echo(audio_data, sample_rate, delay=0.3, decay=0.5)
    
    # Step 4: Display spectrogram
    display_spectrogram(audio_data, sample_rate)
    
    # Step 5: Clip a segment of the audio (e.g., from 5 to 10 seconds)
    clipped_audio = clip_audio(audio_data, start_time=5, end_time=10, sample_rate=sample_rate)
    
    # Step 6: Save the manipulated, echo, and clipped audio in the same directory as the input file
    output_dir = os.path.dirname(file_path)  # Get the directory of the input file
    
    manipulated_output_path = os.path.join(output_dir, 'manipulated_audio.wav')
    clipped_output_path = os.path.join(output_dir, 'clipped_audio.wav')
    echo_output_path = os.path.join(output_dir, 'echo_audio.wav')  # Path for echo audio
    
    # Save the manipulated, clipped, and echo audio
    sf.write(manipulated_output_path, manipulated_audio, sample_rate)
    sf.write(clipped_output_path, clipped_audio, sample_rate)
    sf.write(echo_output_path, echo_audio, sample_rate)  # Save echo-applied audio
    
    print(f"Manipulated audio saved at: {manipulated_output_path}")
    print(f"Clipped audio saved at: {clipped_output_path}")
    print(f"Echo-applied audio saved at: {echo_output_path}")
