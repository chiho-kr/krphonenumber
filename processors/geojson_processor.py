import json
from phone_utils import extract_phone_numbers
from alt_map import deobfuscate

def detect_property(features):
    prop_counts = {}
    total = len(features)
    for feature in features:
        props = feature.get("properties", {})
        for key, value in props.items():
            if not isinstance(value, str):
                continue
            results = extract_phone_numbers(value)
            if results:
                prop_counts[key] = prop_counts.get(key, 0) + 1
    if not prop_counts:
        return None
    best_key, best_count = max(prop_counts.items(), key=lambda item: item[1])
    if best_count / total >= 0.3:
        return best_key
    return None

def process_geojson(input_file, output_file, property, deobfuscate_flag=True, delim_option="hyphen", strip_zero=True, split_results=True, include_service=False):
    with open(input_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    features = geojson_data.get("features", [])
    # 자동 감지: property가 지정되지 않은 경우
    if not property:
        property = detect_property(features)
        if property:
            print(f"[INFO] 자동 감지된 전화번호 속성: '{property}'")
        else:
            print("[ERROR] 전화번호 속성을 자동 감지할 수 없습니다.")
            return

    new_features = []
    for feature in features:
        props = feature.get("properties", {})
        phone_text = props.get(property, "")
        # 전화번호 값이 없으면 원래 feature 그대로 추가
        if not isinstance(phone_text, str) or phone_text.strip() == "":
            new_features.append(feature)
            continue

        if deobfuscate_flag:
            phone_text = deobfuscate(phone_text)
        entries = extract_phone_numbers(phone_text, delim_option, True, strip_zero)
        if entries:
            if split_results:
                # 각 전화번호 결과마다 feature를 복제하여 추가
                for entry in entries:
                    # 딥카피 대신, 기존 properties를 복제한 후 업데이트
                    new_props = props.copy()
                    new_props[property + "_Normalized"] = entry["normalized"]
                    new_props[property + "_Formatted"] = entry["formatted"]
                    if include_service:
                        new_props[property + "_Service"] = entry["service_by_law"]
                    # 복제된 feature 생성 (geometry는 동일)
                    new_feature = {
                        "type": feature.get("type", "Feature"),
                        "geometry": feature.get("geometry"),
                        "properties": new_props
                    }
                    new_features.append(new_feature)
            else:
                # 한 feature 내에 여러 결과를 저장 (세미콜론으로 결합)
                normalized_list = [entry["normalized"] for entry in entries]
                formatted_list = [entry["formatted"] for entry in entries]
                props[property + "_Normalized"] = ";".join(normalized_list)
                props[property + "_Formatted"] = ";".join(formatted_list)
                if include_service:
                    service_list = [entry["service_by_law"] for entry in entries]
                    props[property + "_Service"] = ";".join(service_list)
                new_features.append(feature)
        else:
            # 전화번호 결과가 없으면, 원래 feature를 추가
            new_features.append(feature)
    
    # 업데이트된 feature 목록으로 대체
    geojson_data["features"] = new_features
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 처리 완료. 결과는 '{output_file}'에 저장되었습니다.")
