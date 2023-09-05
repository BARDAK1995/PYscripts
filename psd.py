import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
# Read the file into a DataFrame, assuming space-separated values and no header
file_path = "6Lightestjet.dat"
df = pd.read_csv(file_path, delim_whitespace=True, header=None)
# Extract the first column (time step) and the 10th column (data of interest)

tau = 5.0e-9   
time_step = np.array(df[0]) * tau
data_of_interest = np.array(df[11])
cutoff = len(data_of_interest)//2
cutoffTime = cutoff * tau
actual_data = data_of_interest[cutoff:]
cutoff_timesteps = time_step[cutoff:]
# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(cutoff_timesteps, actual_data, marker='o', linestyle='-')
plt.xlabel('Time Step')
plt.ylabel('Data of Interest')
plt.title('Plot of Data of Interest against Time Step')
# plt.grid(True)
plt.show()


# # # Detrend the data to make it stationary
detrended_data = signal.detrend(actual_data)
plt.figure(figsize=(12, 6))
plt.plot(cutoff_timesteps, detrended_data, marker='o', linestyle='-')
plt.xlabel('Time Step')
plt.ylabel('Detrended DATA')
plt.title('Plot of Data of Interest against Time Step')
# plt.grid(True)
plt.show()
detrended_data_array = np.array(detrended_data)
# Calculate the Power Spectral Density using Fast Fourier Transform
samplingFreq = 1/tau
frequencies, psd_values = signal.welch(detrended_data_array, fs=samplingFreq, nperseg=30030)
# Plotting the Power Spectral Density
plt.figure(figsize=(12, 6))
plt.semilogy(frequencies/1000, psd_values)
plt.title('Power Spectral Density')
plt.xlabel('Frequency [kHz]')
plt.ylabel('PSD [V**2/Hz]')
plt.grid(True)
plt.show()
filtered_indices = (frequencies >= 0) & (frequencies <= 900000)
plt.title('Power Spectral Density')
plt.xlabel('Frequency [kHz]')
plt.ylabel('PSD [V**2/Hz]')
plt.semilogy(frequencies[filtered_indices]/1000, psd_values[filtered_indices])
plt.show()

