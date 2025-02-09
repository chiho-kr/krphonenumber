import re
from alt_map import deobfuscate

def classify_by_law(normalized):
    if len(normalized) in (3, 4) and normalized.startswith('1'):
        if normalized in ["110", "112", "119"]:
            return "긴급전화 (110/112/119)"
        if normalized.startswith(("10", "11", "12")):
            return "특수번호 (긴급민원 및 공공서비스)"
        if normalized.startswith("13"):
            return "특수번호 (생활정보 안내 및 긴급민원)"
        if normalized in ["1541", "1633", "1655", "1677", "1782"]:
            return "특수번호 (수신자 부담)"
        if normalized.startswith("18") and len(normalized)==3:
            return "특수번호 (기타 서비스)"
        if normalized.startswith("15") and len(normalized)==4:
            return "특수번호 (기타 서비스)"
        return "특수번호 (미분류)"
    
    if normalized.startswith("00"):
        if normalized.startswith("003") or normalized.startswith("007"):
            return "국제전화사업자 (설비보유재판매)"
        return "국제전화사업자 (회선설비 보유)"
    
    if normalized.startswith("08"):
        if normalized.startswith("085"):
            return "시외전화사업자 (재판매)"
        m = re.match(r"08(\d)", normalized)
        if m and m.group(1) not in ['5','9']:
            return "시외전화사업자 (회선설비 보유)"
        return "시외전화사업자 (비정상)"
    
    if normalized.startswith("0100"):
        return "위성휴대통신사업자"
    
    if normalized.startswith("015"):
        return "무선호출사업자"
    
    if normalized.startswith("013"):
        if normalized.startswith("0135"):
            return "특정 가입자 대상 서비스 (공공기관)"
        return "특정 가입자 대상 서비스"
    
    if normalized.startswith("014"):
        return "부가통신역무 제공사업자"
    
    if normalized.startswith("070"):
        return "인터넷전화사업자"
    
    if normalized.startswith("012"):
        return "사물지능통신사업자"
    
    if normalized.startswith("050"):
        return "개인번호 서비스"
    
    if normalized.startswith("01"):
        return "이동전화사업자 (모바일)"
    
    if normalized.startswith("0"):
        region = classify_region(normalized)
        if region == "예비":
            return "일반 전화망 번호 (알 수 없음)"
        return f"일반 전화망 번호 ({region})"
    
    return "알 수 없음"

def classify_region(normalized):
    s_val = normalized[1:]
    AREA_MAPPING = {
        "2": "서울",
        "31": "경기",
        "32": "인천",
        "33": "강원",
        "41": "충남",
        "42": "대전",
        "43": "충북",
        "44": "세종",
        "51": "부산",
        "52": "울산",
        "53": "대구",
        "54": "경북",
        "55": "경남",
        "61": "전남",
        "62": "광주",
        "63": "전북",
        "64": "제주"
    }
    if len(s_val) >= 2 and s_val[:2] in AREA_MAPPING:
        return AREA_MAPPING[s_val[:2]]
    if len(s_val) >= 1 and s_val[0] in AREA_MAPPING:
        return AREA_MAPPING[s_val[0]]
    if len(s_val) >= 2 and s_val[:2] in [str(i) for i in range(34,40)]:
        return "예비"
    if len(s_val) >= 2 and s_val[:2] in [str(i) for i in range(45,50)]:
        return "예비"
    if len(s_val) >= 2 and s_val[:2] in [str(i) for i in range(56,60)]:
        return "예비"
    if len(s_val) >= 2 and s_val[:2] in [str(i) for i in range(65,70)]:
        return "예비"
    return "알 수 없음"

def normalize_number_without_ext(number):
    num = re.sub(r'[\s\-\(\)\.\~]+', '', number.strip())
    if num.startswith('+82'):
        num = num[3:]
        if not num.startswith('0'):
            num = '0' + num
    elif num.startswith('0082'):
        pass
    if num and not num.startswith('0') and num[0] in '23456' and len(num) in (9,10):
        num = '0' + num
    return num

def parse_extension(raw):
    if "~" in raw:
        parts = re.split(r'~+', raw)
        if len(parts) < 2:
            return [normalize_number_without_ext(raw)]
        ext_candidates = parts[1:]
        if any(len(c.strip()) > 2 for c in ext_candidates):
            return [normalize_number_without_ext(raw)]
        base = normalize_number_without_ext(parts[0])
        results = [base]
        for candidate in ext_candidates:
            candidate = candidate.strip()
            if candidate.isdigit():
                new_number = base[:-1] + candidate
                if new_number not in results:
                    results.append(new_number)
        return results
    elif "." in raw:
        parts = re.split(r'\.+', raw)
        if len(parts) == 2 and 1 <= len(parts[1].strip()) <= 2:
            base = normalize_number_without_ext(parts[0])
            ext = parts[1].strip()
            replaced = base[:-len(ext)] + ext
            return [base, replaced]
        else:
            return [normalize_number_without_ext(raw)]
    else:
        return [normalize_number_without_ext(raw)]

def normalize_number(raw):
    raw = re.sub(r'[/]+', '~', raw)
    if raw.count('-') == 3:
        parts = raw.rsplit('-', 1)
        raw = parts[0] + "~" + parts[1]
        return parse_extension(raw)
    if "~" in raw or (("." in raw) and re.search(r'[\.]+(\d{1,2})\s*$', raw)):
        return parse_extension(raw)
    else:
        return [normalize_number_without_ext(raw)]

def format_phone_number(num, delim_option="hyphen", country=True, s=False, user_format=None):
    """
    num: 숫자만 포함된 전화번호 문자열
    delim_option: 출력 구분자 ("hyphen", "space", "dot", "none")
    country: 국가번호 포함 여부.
       True이면, 국내번호 앞의 0을 (s 옵션에 따라) 처리한 후 "+82 " 접두어를 붙임.
    s: True이면 각 부분에서 선행 0을 제거, False이면 그대로 유지.
    user_format: 선택적 사용자 지정 형식 (예: "{area}-{central}-{line}")
    
    예)
      - country True, s False: "010-1234-5678" → "+82 010-1234-5678"
      - country True, s True:  "010-1234-5678" → "+82 10-1234-5678"
      - country False, s False: "010-1234-5678" → "010-1234-5678"
      - country False, s True:  "010-1234-5678" → "10-1234-5678"
    """
    if not num.isdigit():
        return num

    if delim_option == "hyphen":
        delim = "-"
    elif delim_option == "space":
        delim = " "
    elif delim_option == "dot":
        delim = "."
    else:
        delim = ""

    area = central = line = None
    if len(num) in (3, 4) and num[0] == '1':
        formatted = num
    elif (num.startswith("010") or num.startswith("011") or num.startswith("016") or
          num.startswith("017") or num.startswith("018") or num.startswith("019") or
          num.startswith("070")) and len(num) == 11:
        area = num[:3]
        central = num[3:7]
        line = num[7:]
        formatted = delim.join([area, central, line])
    elif num.startswith("050") and len(num) == 12:
        area = num[:4]
        central = num[4:8]
        line = num[8:]
        formatted = delim.join([area, central, line])
    elif num.startswith("02"):
        if len(num) == 9:
            area = num[:2]
            central = num[2:5]
            line = num[5:]
        elif len(num) == 10:
            area = num[:2]
            central = num[2:6]
            line = num[6:]
        else:
            area = num[:2]
            central = num[2:-4]
            line = num[-4:]
        formatted = delim.join([area, central, line])
    elif num.startswith("0"):
        if len(num) == 10:
            area = num[:3]
            central = num[3:6]
            line = num[6:]
        elif len(num) == 11:
            area = num[:3]
            central = num[3:7]
            line = num[7:]
        else:
            a_len = 3
            l_len = 4
            area = num[:a_len]
            central = num[a_len:-l_len]
            line = num[-l_len:]
        formatted = delim.join([area, central, line])
    else:
        formatted = num

    # s 옵션 처리
    if s:
        parts = formatted.split(delim) if delim else [formatted]
        parts = [p.lstrip("0") or "0" for p in parts]
        formatted = delim.join(parts)

    # country 옵션 처리
    if country and num.startswith("0") and area is not None:
        # 만약 s 옵션이 False: area를 그대로 사용; True이면 lstrip("0")
        if s:
            area_part = area.lstrip("0") or "0"
        else:
            area_part = area
        formatted = "+82 " + delim.join([area_part, central, line])
    elif not country and num.startswith("0") and area is not None:
        if s:
            area_part = area.lstrip("0") or "0"
        else:
            area_part = area
        formatted = delim.join([area_part, central, line])
    
    if user_format:
        try:
            return user_format.format(area=area, central=central, line=line)
        except Exception:
            return formatted
    return formatted

def validate_number_by_law(raw):
    norm_list = normalize_number(raw)
    if not norm_list:
        return "정규화 실패"
    norm = norm_list[0]
    service = classify_by_law(norm)
    return service

def extract_phone_numbers(text, delim_option="hyphen", country=True, s=True, user_format=None):
    tokens = re.split(r'[,;\n]+', text)
    results = []
    for token in tokens:
        token = token.strip()
        if not token or len(token) < 3:
            continue
        matches = re.findall(r'[\+0-9\(\)][\d\.\-\~\s\(\)/]+', token)
        for m in matches:
            original = m.strip()
            norm_list = normalize_number(original)
            for norm in norm_list:
                if len(norm) < 3:
                    continue
                service = validate_number_by_law(original)
                formatted = format_phone_number(norm, delim_option, country, s, user_format)
                results.append({
                    'original': original,
                    'normalized': norm,
                    'service_by_law': service,
                    'formatted': formatted
                })
    return results
