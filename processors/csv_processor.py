import csv
import os
from phone_utils import extract_phone_numbers
from alt_map import deobfuscate

def detect_phone_column(rows, fieldnames):
    best_col = None
    best_count = 0
    total = len(rows)
    for col in fieldnames:
        count = 0
        for row in rows:
            cell = row.get(col, "")
            if cell:
                results = extract_phone_numbers(cell)
                if results:
                    count += 1
        if count > best_count:
            best_count = count
            best_col = col
    if total > 0 and best_count / total >= 0.3:
        return best_col
    return None

def process_csv(input_file, output_file, column, header_option, delim_option, country_option, strip_zero, deobfuscate_flag, split_results, include_service):
    with open(input_file, newline='', encoding='utf-8') as csv_in:
        if header_option:
            reader = csv.DictReader(csv_in)
            rows = list(reader)
            fieldnames = reader.fieldnames
        else:
            reader = csv.reader(csv_in)
            rows_list = list(reader)
            if not rows_list:
                print("[ERROR] CSV 파일이 비어 있습니다.")
                return
            fieldnames = [f"Column{i+1}" for i in range(len(rows_list[0]))]
            rows = [dict(zip(fieldnames, row)) for row in rows_list]

    if not column:
        detected_col = detect_phone_column(rows, fieldnames)
        if detected_col:
            print(f"[INFO] 자동 감지된 전화번호 컬럼: '{detected_col}'")
            column = detected_col
        else:
            print("[ERROR] 전화번호 컬럼을 자동 감지할 수 없습니다.")
            return

    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_processed{ext}"

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_out:
        output_fields = fieldnames.copy()
        output_fields += ["Normalized", "Formatted"]
        if include_service:
            output_fields.insert(-1, "Service")
        writer = csv.DictWriter(csv_out, fieldnames=output_fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in rows:
            orig = row.get(column, "")
            if deobfuscate_flag:
                orig = deobfuscate(orig)
            entries = extract_phone_numbers(orig, delim_option, country_option, strip_zero)
            if entries:
                if split_results:
                    for entry in entries:
                        new_row = row.copy()
                        new_row["Normalized"] = entry["normalized"]
                        if include_service:
                            new_row["Service"] = entry["service_by_law"]
                        new_row["Formatted"] = entry["formatted"]
                        writer.writerow(new_row)
                else:
                    normalized_list = [entry["normalized"] for entry in entries]
                    formatted_list = [entry["formatted"] for entry in entries]
                    row["Normalized"] = ";".join(normalized_list)
                    if include_service:
                        service_list = [entry["service_by_law"] for entry in entries]
                        row["Service"] = ";".join(service_list)
                    row["Formatted"] = ";".join(formatted_list)
                    writer.writerow(row)
            else:
                row["Normalized"] = ""
                if include_service:
                    row["Service"] = ""
                row["Formatted"] = ""
                writer.writerow(row)
    print(f"[INFO] 처리 완료. 결과는 '{output_file}'에 저장되었습니다.")
