import numpy as np
import scipy.signal as signal
import scipy.stats as stats

def extract_ppg_features(ppg_signal, fs=2175.0):
    """
    Extracts time-domain, morphological, frequency-domain, and statistical features from a PPG signal segment.
    
    Parameters:
        ppg_signal (list or np.ndarray): Raw PPG signal values.
        fs (float): Sampling rate in Hz.
        
    Returns:
        dict: A dictionary of extracted features.
    """
    ppg = np.array(ppg_signal).astype(float)
    t = np.arange(len(ppg)) / fs

    # 1. Detrend and Bandpass Filter (0.5 - 8 Hz)
    sos = signal.butter(2, [0.5, 8], btype='bandpass', fs=fs, output='sos')
    filtered = signal.sosfiltfilt(sos, ppg)

    # 2. Peak Detection
    distance = int(0.3 * fs)  # assuming minimum 0.3s between peaks (~200 BPM max)
    peaks, _ = signal.find_peaks(filtered, distance=distance)

    ibi = np.diff(peaks) / fs if len(peaks) > 1 else np.array([0])
    hr = 60 / ibi if len(ibi) > 0 else np.array([0])

    # 3. Frequency-Domain Features using Welch
    f, psd = signal.welch(filtered, fs, nperseg=len(filtered))
    lf_band = (0.04, 0.15)
    hf_band = (0.15, 0.4)

    lf_power = np.trapz(psd[(f >= lf_band[0]) & (f <= lf_band[1])], f[(f >= lf_band[0]) & (f <= lf_band[1])])
    hf_power = np.trapz(psd[(f >= hf_band[0]) & (f <= hf_band[1])], f[(f >= hf_band[0]) & (f <= hf_band[1])])

    # 4. Statistical Features
    features = {
        'mean_ppg': np.mean(filtered),
        'std_ppg': np.std(filtered),
        'skew_ppg': stats.skew(filtered),
        'kurtosis_ppg': stats.kurtosis(filtered),
        'mean_hr': np.mean(hr) if len(hr) else 0,
        'std_hr': np.std(hr) if len(hr) else 0,
        'lf_power': lf_power,
        'hf_power': hf_power,
        'lf_hf_ratio': lf_power / hf_power if hf_power > 0 else 0,
        'pulse_rate': len(peaks) / (len(ppg) / fs) * 60
    }

    return features
