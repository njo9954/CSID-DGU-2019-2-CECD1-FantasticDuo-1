
import speech_recognition as sr  # 음성인식과 관련된 유틸을 포함한 라이브러리
import noise_rd

if __name__ == "__main__":
    tmp_filename = 'realtime.wav'  # 버퍼로 사용할 파일이름
    r = sr.Recognizer()       # 음성인식기를 불러옴
    i=1

    while True: # 키보드로 인터럽트가 발생할 때까지 음성을 입력으로 받음!
        try:
            with sr.Microphone() as source:  # 마이크로 음성을 불러옴
                print('Wait for speaking')
                audio_data = r.listen(source)  # 오디오 소스중 의미있는 부분인 오디오 데이터를 기록함
                open(tmp_filename, 'wb').write(audio_data.get_wav_data())  # 오디오 소스를 WAV포맷으로 파일시스템에 전송함             
                freq = noise_rd.reducing(tmp_filename)  # 필터링을 진행함
            with sr.AudioFile(tmp_filename) as source:  # 필터링된 오디오 소스를 불러옴
                audio_data = r.record(source)  # 오디오 소스중 의미있는 부분인 오디오 데이터를 기록함            
                open(f'signal/input_{i}.wav', 'wb').write(audio_data.get_wav_data())
                text = r.recognize_google(audio_data, language='ko-KR')  # 오디오 데이터를 구글음성인식에 전달하여 자연어(평문)으로 바꿈

                if "도와" in text:  # 구조요청이 포함되면 파일시스템에 전송하고 텍스트를 콘솔에 출력함
                    open(f'RT_signal/result_{i}.wav', 'wb').write(audio_data.get_wav_data())
                    print(f'도움호출 !! -> "{text}"')
                elif "구해" in text:                
                    open(f'RT_signal/result_{i}.wav', 'wb').write(audio_data.get_wav_data())
                    print(f'도움호출 !! -> "{text}"')
                    i += 1
                elif "살려" in text:                
                    open(f'RT_signal/result_{i}.wav', 'wb').write(audio_data.get_wav_data())
                    print(f'도움호출 !! -> "{text}"')
                    i += 1
                elif "여기요" in text:                
                    open(f'RT_signal/result_{i}.wav', 'wb').write(audio_data.get_wav_data())
                    print(f'도움호출 !! -> "{text}"')
                    i += 1
                else:  # 구조요청이 아닌 사운드
                    print(f'구조 요청 아님!!"{text}"')
        except sr.UnknownValueError as e:
            print("* 음성을 인식할수없습니다. *", e)  # 음성인식에 실패하면 콘솔에 출력함
            exit(0)
            