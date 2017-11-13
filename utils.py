# -*- coding: utf-8 -*-

'''
By Yunchao He. yunchaohe@gmail.com
'''

from __future__ import print_function

import numpy as np
import librosa
import copy
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt

from hyperparams import Hyperparams as hp


def spectrogram2wav(spectrogram):
    '''Convert spectrogram into a waveform using Griffin-lim's raw.
    '''
    spectrogram = spectrogram.T  # [f, t]
    X_best = copy.deepcopy(spectrogram)  # [f, t]
    for i in range(hp.n_iter):
        X_t = invert_spectrogram(X_best)
        est = librosa.stft(X_t, hp.n_fft, hp.hop_length, win_length=hp.win_length)  # [f, t]
        phase = est / np.maximum(1e-8, np.abs(est))  # [f, t]
        X_best = spectrogram * phase  # [f, t]
    X_t = invert_spectrogram(X_best)
    y = np.real(X_t)

    return y


def invert_spectrogram(spectrogram):
    '''
    spectrogram: [f, t]
    '''
    return librosa.istft(spectrogram, hp.hop_length, win_length=hp.win_length, window="hann")


def plot_alignment(alignment, gs, elapsed_time):
    """
    Plots the alignment

    alignment: (numpy) matrix of shape (encoder_steps,decoder_steps)

    gs : (int) global step
    """
    a = alignment[:, 10]

    fig, ax = plt.subplots()
    im = ax.imshow(alignment, interpolation='none')
    fig.colorbar(im, ax=ax)
    plt.xlabel('Decoder timestep')
    plt.ylabel('Encoder timestep')
    hours = elapsed_time // 3600
    minutes = (elapsed_time - 3600 * hours) // 60
    plt.title('{} Steps After {} hours {} minutes'.format(gs, hours, minutes))
    plt.tight_layout()
    plt.axis('off')
    plt.savefig('{}/alignment_{}.png'.format(hp.logdir, gs), format='png')
