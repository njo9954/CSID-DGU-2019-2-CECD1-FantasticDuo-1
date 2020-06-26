import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wave  # wav 포맷으로 입출력을 할 수 있게 해주는 라이브러리
from scipy import signal        # 신호처리 관련 라이브러리 // 소음 제거 수행
from scipy.fftpack import fft
import math

# path : wav파일의 위치
# show_plot : 비교 그래프
def reducing(path, show_plot=True):
    filename = path[path.rfind('/') + 1:]  # 파일 이름
    rate, raw = wave.read(path)       # wav 데이터

    # 1~N개의 채널 중 첫번째 것만 추출함
    raw_data = []
    if type(raw[0]) != np.int16:
        for stereo in raw:
            raw_data.append(int(stereo[0]))
    else:
        raw_data = raw

    # 750Hz 보다 위의 대역을 소거(highpass)
    b, a = signal.butter(5, 750 / (rate / 2), btype='highpass',
                         analog=False, output='ba', fs=None)
    filtered = signal.lfilter(b, a, raw_data)
    filtered = signal.lfilter(b, a, filtered)

    # 450Hz 보다 아래의 대역을 소거(lowpass)
    d, c = signal.butter(5, 450 / (rate / 2), btype='lowpass',
                         analog=False, output='ba', fs=None)
    filtered=signal.lfilter(d, c, filtered)

    # 소리의 크기를 듣기 적절하게 조정
    filtered = np.int16(filtered / np.max(np.abs(filtered)) * 32767)
    r_time = np.arange(len(raw_data))/float(rate)
    f_time = np.arange(len(filtered))/float(rate)

    # raw_noise_1=list()  #1초부터 2.5초까지 노이즈 제거 전
    # fil_noise_1=list()  #1초부터 2.5초까지 노이즈 제거 후    

    # raw_noise_2=list()  #3.5초부터 5초까지 노이즈 제거 전
    # fil_noise_2=list()  #3.5초부터 5초까지 노이즈 제거 후    

    # 비교 그래프 설정

    if show_plot:
        x_labels=["0.0s","0.5s","1.0s","1.5s","2.0s","2.5s","3.0s","3.5s",
        "4.0s","4.5s","5.0s","5.5s","6.0s","6.5s","7.0s","7.5s","8.0s"]
        y_ticks=[-40000,-35000,-30000,-25000,-20000,-15000,-10000,-5000,
        0,5000,10000,15000,20000,25000,30000,35000,40000]
        fig, axs = plt.subplots(2, 1)
        fig.subplots_adjust(hspace=0.5)
        axs[0].fill_between(r_time, raw_data)
        axs[0].plot(raw_data)  # before
        axs[0].set_xlabel("Raw Sound")
        axs[0].set_ylabel("Magnitude")
        axs[0].grid(True)
        axs[0].set_xticks(np.arange(0, len(raw_data)+1, 22050))
        axs[0].set_xticklabels(x_labels)
        axs[0].set_yticks(y_ticks)

        axs[1].fill_between(f_time, filtered)
        axs[1].plot(filtered)  # after
        axs[1].set_xlabel('Filtered Sound')
        axs[1].set_ylabel("Magnitude")
        axs[1].grid(True)
        axs[1].set_xticks(np.arange(0, len(filtered)+1, 22050))
        axs[1].set_xticklabels(x_labels)
        axs[1].set_yticks(y_ticks)

        plt.show()
        pass

    # freq = np.fft.fftfreq(filtered.shape[-1], 0.1)
    # plt.plot(np.fft.fftshift(freq), np.fft.fftshift(np.abs(filtered)) / len(filtered))

    # r_spec = np.fft.fft(raw_data)
    # r_freq = np.fft.fftfreq(raw_data.size, 1/rate)
    # r_mask = r_freq > 0

    # f_spec = np.fft.fft(filtered)
    # f_freq = np.fft.fftfreq(filtered.size, 1/rate)
    # f_mask = f_freq > 0

    # fig, axs = plt.subplots(2, 1)
    # fig.subplots_adjust(hspace=0.5)
    # axs[0].plot(r_freq[r_mask], np.abs(r_spec[r_mask]))
    # axs[0].set_xlim(0, 1500)
    # axs[0].set_xlabel("Frequency(HZ)")
    # axs[0].set_ylabel("Magnitude")

    # axs[1].plot(f_freq[f_mask], np.abs(f_spec[f_mask]))
    # axs[1].set_xlim(0, 1500)
    # axs[1].set_xlabel("Frequency(Hz)")
    # axs[1].set_ylabel("Magnitude")
    # plt.show()

    wave.write(f'output/{"filtered_"+filename}',
               rate, filtered)  # output 파일 생성
    return rate, filename
