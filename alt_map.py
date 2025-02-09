# alt_map.py
# 전화번호에 사용된 대체 문자(Obfuscation)를 표준 문자(숫자 및 하이픈)로 복원하는 모듈입니다.

ALT_MAP = {}

# 하이픈 대체 문자
for ch in ["‐", "‑", "‒", "—", "–", "―", "－", "ー", "ｰ", "➖", "−", "一", "ㅡ"]:
    ALT_MAP[ch] = "-"

# 0번 대체 문자
for ch in ["o", "ο", "о", "ㅇ", "٥", "ہ", "०", "৹", "ଠ", "ഠ", "O", "○", "〇", "◯", "ⓞ", "⒪", "영", "공", "빵"]:
    ALT_MAP[ch] = "0"

# 1번 대체 문자
for ch in ["|", "I", "ı", "l", "ㅣ", "│", "ا", "৷", "丨", "①", "⒧", "⑴", "하나", "일"]:
    ALT_MAP[ch] = "1"

# 2번 대체 문자
for ch in ["②", "⑵", "둘", "이"]:
    ALT_MAP[ch] = "2"

# 3번 대체 문자
for ch in ["③", "⑶", "삼", "셋"]:
    ALT_MAP[ch] = "3"

# 4번 대체 문자
for ch in ["④", "⑷", "사", "넷"]:
    ALT_MAP[ch] = "4"

# 5번 대체 문자
for ch in ["⑤", "⑸", "오", "다섯"]:
    ALT_MAP[ch] = "5"

# 6번 대체 문자
for ch in ["⑥", "⑹", "육", "여섯"]:
    ALT_MAP[ch] = "6"

# 7번 대체 문자
for ch in ["⑦", "⑺", "칠", "일곱"]:
    ALT_MAP[ch] = "7"

# 8번 대체 문자
for ch in ["⑧", "⑻", "팔", "여덟"]:
    ALT_MAP[ch] = "8"

# 9번 대체 문자
for ch in ["⑨", "⑼", "구", "아홉"]:
    ALT_MAP[ch] = "9"


def deobfuscate(text):
    """
    입력 text 내의 각 문자를 ALT_MAP에 따라 표준 문자(숫자 및 하이픈)로 치환합니다.
    """
    return "".join(ALT_MAP.get(ch, ch) for ch in text)
