import os
import speech_recognition as sr  # 음성인식 관련 라이브러리
import noise_rd

if __name__ == "__main__":
    # raw 데이터(드론 노이즈 + 보이스), 음성인식기
    path = "input/"
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        file_list[i] = path+file_list[i]
    r = sr.Recognizer()

    for i in range(len(file_list)):
        try:
            with sr.AudioFile(file_list[i]) as source:  # 오디오 소스를 불러옴
                audio_data = r.record(source)  # 오디오 소스중 의미있는 부분인 오디오 데이터를 기록
                open(file_list[i], 'wb').write(
                    audio_data.get_wav_data())  # 오디오 소스를 wav포맷으로 파일시스템에 전송
                rate, filename = noise_rd.reducing(file_list[i])  # 필터링
                
            with sr.AudioFile(file_list[i]) as source:  # 필터링된 오디오 소스를 불러옴
                audio_data = r.record(source)
                # 오디오 데이터를 구글음성인식에 전달하여 평문으로 바꿈
                text = r.recognize_google(audio_data, language='ko-KR')

                # if "도와" or "구해" or "살려" or "여기" in text:  # 해당 글자가 포함되면 파일시스템에 전송
                if "도와" in text:  # 구조요청이 포함되면 파일시스템에 전송
                    # print(text)
                    i += 1
                    open(f'signal/'+filename, 'wb').write(audio_data.get_wav_data())

                elif "구해" in text:
                    # print(text)
                    i += 1
                    open(f'signal/'+filename, 'wb').write(audio_data.get_wav_data())

                elif "살려" in text:
                    # print(text)
                    i += 1
                    open(f'signal/'+filename, 'wb').write(audio_data.get_wav_data())

                elif "여기요" in text:
                    # print(text)
                    i += 1
                    open(f'signal/'+filename, 'wb').write(audio_data.get_wav_data())

                else:  # 구조요청이 아닌 보이스
                    print(text + "\t-> 구조요청 아님")          
        except sr.UnknownValueError as e:
            print("* 음성을 인식할수없습니다. *", e)  # 음성인식에 실패하면 콘솔에 출력함
            exit(0)
