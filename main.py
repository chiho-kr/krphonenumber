#!/usr/bin/env python3
import argparse
import os
from processors import csv_processor, geojson_processor

def main():
    parser = argparse.ArgumentParser(description="전화번호 CSV/GeoJSON 변환 도구")
    parser.add_argument("--input", required=True, help="입력 파일 경로 (CSV 또는 GeoJSON)")
    parser.add_argument("--output", help="출력 파일 경로 (생략 시 input 파일명에 _processed가 붙음)")
    parser.add_argument("--column", help="CSV 파일에서 전화번호가 포함된 컬럼명 (지정하지 않으면 자동 감지)")
    parser.add_argument("--property", help="GeoJSON 파일에서 전화번호가 포함된 속성 키 (지정하지 않으면 자동 감지)")
    # 기본값: header 기본 False, country 기본 False, strip-zero 기본 False
    parser.add_argument("--header", type=lambda s: s.lower() in ("true", "1", "yes"), default=False,
                        help="파일에 헤더가 있는지 여부 (True/False; 기본: False)")
    parser.add_argument("--delimiter", choices=["hyphen", "space", "dot", "none"], default="hyphen",
                        help="출력 포매팅 구분자 (기본: hyphen)")
    parser.add_argument("--country", type=lambda s: s.lower() in ("true", "1", "yes"), default=False,
                        help="국가번호 포함 여부 (True/False; 기본: False)")
    parser.add_argument("--strip-zero", type=lambda s: s.lower() in ("true", "1", "yes"), default=False,
                        help="지역번호/식별번호 앞의 선행 0 제거 여부 (True/False; 기본: False)")
    parser.add_argument("--deobfuscate", type=lambda s: s.lower() in ("true", "1", "yes"), default=True,
                        help="전화번호 내 대체문자 복원 여부 (True/False; 기본: True)")
    parser.add_argument("--split-results", type=lambda s: s.lower() in ("true", "1", "yes"), default=True,
                        help="한 셀(또는 속성)에 여러 결과가 있으면 각 결과를 별도의 행으로 출력 (True/False; 기본: True)")
    parser.add_argument("--include-service", type=lambda s: s.lower() in ("true", "1", "yes"), default=False,
                        help="출력 파일에 서비스 분류(Service) 컬럼을 포함할지 여부 (True/False; 기본: False)")
    args = parser.parse_args()
    
    if not args.output:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}_processed{ext}"
    
    ext = os.path.splitext(args.input)[1].lower()
    if ext == ".csv":
        csv_processor.process_csv(
            input_file=args.input,
            output_file=args.output,
            column=args.column,
            header_option=args.header,
            delim_option=args.delimiter,
            country_option=args.country,
            strip_zero=args.strip_zero,
            deobfuscate_flag=args.deobfuscate,
            split_results=args.split_results,
            include_service=args.include_service
        )
    elif ext == ".geojson":
        geojson_processor.process_geojson(
            input_file=args.input,
            output_file=args.output,
            property=args.property,
            deobfuscate_flag=args.deobfuscate,
            delim_option=args.delimiter,
            strip_zero=args.strip_zero,
            split_results=args.split_results,
            include_service=args.include_service
        )
    else:
        print("[ERROR] 지원하지 않는 파일 확장자입니다. CSV 또는 GeoJSON 파일만 지원됩니다.")

if __name__ == '__main__':
    main()
