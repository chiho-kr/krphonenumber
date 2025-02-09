# 한국 전화번호 정규화 및 포매팅 도구
이 프로젝트는 전기통신사업법 제48조에 근거한 **전기통신번호관리세칙**[과학기술정보통신부고시 제2021-93호, 2021.12.7.]
을 기반으로 하여, 한국 내 다양한 전화번호 표기(휴대전화, 시내전화, 시외전화, 국제전화 등)를 일관된 표준 형식으로 정규화하고 
포매팅하는 도구입니다. 또한, CSV 및 GeoJSON 파일에 포함된 전화번호 데이터를 자동으로 감지하여 변환하는 기능을 제공합니다.

## 특징
- **전화번호 정규화 및 포매팅**  
  - 다양한 입력 형식(예: "010-1234-5678", "(02) 123-4567", "+82 10 1234 5678" 등)을  
    하나의 표준 형식으로 변환합니다.
  - 옵션에 따라 국가번호 포함 여부와 선행 0 제거 여부를 선택할 수 있습니다.
  - 예를 들어,  
    - `--country True --strip-zero False` → "+82 010-1234-5678"  
    - `--country True --strip-zero True` → "+82 10-1234-5678"  
    - `--country False` → "010-1234-5678" (또는 선행 0 제거 여부에 따라 "10-1234-5678")

- **파일 형식 지원**  
  - **CSV 파일**: 전화번호가 포함된 CSV 파일을 입력받아,  
    전화번호 컬럼을 자동 감지하거나 사용자가 지정한 컬럼을 기준으로 변환합니다.
  - **GeoJSON 파일**: 각 feature의 properties에서 전화번호가 포함된 속성을  
    자동 감지하거나 사용자가 지정한 속성을 기준으로 변환하며,  
    `--split-results` 옵션에 따라 결과를 feature를 복제하여 분리하거나 한 feature 내에  
    세미콜론으로 결합하여 저장할 수 있습니다.
  - 만약 GeoJSON feature에 지정된 전화번호 속성이 없으면, 해당 feature는 그대로 유지합니다.
 
## 사용법
### 설치
- Python 3 이상이 필요합니다.
- 추가적인 외부 라이브러리는 필요하지 않습니다.

### 명령줄 실행
**옵션**  
- `--input` (필수): 입력 파일 경로 (CSV 또는 GeoJSON)
- `--output`: 출력 파일 경로 (생략 시 입력 파일명에 `_processed`가 붙음)
- `--column`: CSV 파일에서 전화번호 컬럼 (자동 감지 가능)
- `--property`: GeoJSON 파일에서 전화번호 속성 (자동 감지 가능)
- `--header`: 파일에 헤더가 있는지 여부 (True/False; 기본: `False`)
- `--delimiter`: 출력 구분자 (`hyphen`, `space`, `dot`, `none`; 기본: `hyphen`)
- `--country`: 국가번호 포함 여부 (True/False; 기본: `False`)  
  - True일 경우, 예: "010-1234-5678" → "+82 010-1234-5678" (strip-zero 옵션에 따라 변동)
- `--strip-zero`: 선행 0 제거 여부 (True/False; 기본: `False`)  
  - True일 경우, "010" → "10", "02" → "2"
- `--deobfuscate`: 대체문자 복원 여부 (True/False; 기본: `True`)
- `--split-results`: 여러 결과를 별도 행으로 출력 (True/False; 기본: `True`)
- `--include-service`: 서비스 분류 열 포함 여부 (True/False; 기본: `False`)

**예시 명령어**
- CSV 파일 처리 (기본 옵션 사용):
`python main.py --input your_input.csv --column PhoneNumber`

- CSV 파일 처리 (국가번호 포함, 선행 0 보존):
`python main.py --input your_input.csv --column PhoneNumber --country True --strip-zero False`

- CSV 파일 처리 (국가번호 포함, 선행 0 제거):
`python main.py --input your_input.csv --column PhoneNumber --country True --strip-zero True`

- GeoJSON 파일 처리:
`python main.py --input your_input.geojson --property PhoneNumber`

## 기능 설명
### 1. 전화번호 정규화 및 포매팅
- **다양한 입력 형식 처리:**  
  한국 내 휴대전화, 시내전화, 시외전화, 국제전화 등 여러 형태의 전화번호 입력을 지원합니다.  
  입력 전화번호에는 하이픈, 공백, 괄호, 점, 물결표 등의 구분자가 포함될 수 있으며, 국가 번호(+82 등)도 처리합니다.

- **정규화:**  
  입력된 전화번호에서 숫자만 추출하여 “01012345678”과 같은 정규화된 형태로 변환합니다.

- **포매팅:**  
  정규화된 번호를 사용자 옵션에 따라 원하는 포맷(예: “010-1234-5678” 또는 “+82 010-1234-5678”)으로 변환합니다.
  `--country`, `--strip-zero` 옵션에 따라 다르게 출력됩니다.
  - **ITU-T E.123 / DIN 5008**: 국가 코드, 지역 번호, 로컬 번호를 공백으로 구분하는 패턴입니다.
    - `python main.py --input input.csv --country True --delimiter space --strip-zero False`: 지역번호의 선행 0이 보존됩니다.
      - 예: `+82 010 1234 5678`
    - `python main.py --input input.csv --country True --delimiter space --strip-zero True`: 지역번호의 선행 0이 제거됩니다.
      - 예: `+82 10 1234 5678`

  - **RFC 3966 / NANP**: 국가 코드, 지역 번호, 로컬 번호를 하이픈으로 구분하는 패턴입니다.
    - `python main.py --input input.csv --country True --delimiter hyphen --strip-zero False`: 지역번호의 선행 0이 보존됩니다.
      - 예: `+82 010-1234-5678`
    - `python main.py --input input.csv --country True --delimiter hyphen --strip-zero True`: 지역번호의 선행 0이 제거됩니다.
      - 예: `+82 10-1234-5678`
  
  - **국내 전화망 번호**: 국가 코드 없이 지역 번호, 로컬 번호를 하이픈 또는 공백으로 구분하는 패턴입니다. `--country` 매개변수를 명시하지 않습니다.
    - `python main.py --input input.csv --delimiter space --strip-zero False`: 번호를 공백으로 구분하며, 지역번호의 선행 0이 보존됩니다.
      - 예: `010 1234 5678`
    - `python main.py --input input.csv --delimiter space --strip-zero True`: 번호를 공백으로 구분하며, 지역번호의 선행 0이 제거됩니다.
      - 예: `10 1234 5678`
    - `python main.py --input input.csv --delimiter hyphen --strip-zero False`: 번호를 하이픈으로 구분하며, 지역번호의 선행 0이 보존됩니다.
      - 예: `010-1234-5678`
    - `python main.py --input input.csv --delimiter hyphen --strip-zero True`: 번호를 하이픈으로 구분하며, 지역번호의 선행 0이 제거됩니다.
      - 예: `10-1234-5678`

### 2. 파일 처리 기능 (CSV 및 GeoJSON)
- **CSV 파일 처리:**  
  - CSV 파일에서 전화번호가 포함된 컬럼을 자동 감지하거나 사용자가 직접 지정할 수 있습니다.  
  - 각 행에 대해 전화번호 정규화 및 포매팅을 수행한 후, 결과를 “Normalized”, “Formatted” (및 옵션에 따라 “Service”) 열에 추가합니다.
  - `--split-results` 옵션에 따라 한 셀에 여러 전화번호가 있는 경우 각 결과를 별도의 행으로 출력하거나, 하나의 셀에 세미콜론으로 결합하여 저장할 수 있습니다.

- **GeoJSON 파일 처리:**  
  - GeoJSON 파일의 각 feature의 properties에서 전화번호가 포함된 속성을 자동 감지하거나 사용자가 지정할 수 있습니다.  
  - 지정된 속성 값이 있는 경우에만 전화번호 정규화 및 포매팅을 수행하여,  
    결과를 해당 속성 이름 뒤에 “_Normalized”와 “_Formatted” (및 옵션에 따라 “_Service”) 항목으로 추가합니다.  
  - `--split-results` 옵션에 따라, 여러 전화번호 결과가 있을 경우 feature를 복제하여 각 결과를 별도 feature로 출력하거나  
    한 feature 내에서 결과를 결합하여 저장할 수 있습니다.

### 3. 대체 문자 복원 (Deobfuscation)
- 입력 전화번호에 숫자나 하이픈 대신 사용된 대체 문자(예: “O”, “영”, “공” 등)를  
  내장된 대체 문자 매핑을 통해 정상 숫자 및 하이픈으로 복원합니다.  
  이 기능은 기본적으로 활성화되어 있어, 표기 오류를 줄이는 데 도움을 줍니다.

### 4. 서비스 분류
- 전화번호의 시작 부분(식별번호, 국번호 등)을 분석하여,  
  - 긴급전화, 특수번호, 국제전화사업자, 시외전화사업자, 위성휴대전화사업자, 무선호출사업자,  
    특정 가입자 대상 서비스, 부가통신역무 제공사업자, 인터넷전화사업자, 사물지능통신사업자,  
    개인번호 서비스, 이동전화사업자, 고정전화(일반 전화망) 등으로 분류합니다.
- 이를 통해, 전화번호 데이터가 어떤 유형의 서비스에 속하는지 추가 정보를 제공합니다.

### 5. 유연한 옵션 설정
- **사용자 지정 옵션:**  
  파일에 헤더가 있는지 여부, 전화번호 컬럼(또는 속성) 지정, 출력 구분자, 국가번호 포함 여부,  
  선행 0 제거 여부, 대체 문자 복원 여부, 결과 분할 방식, 서비스 열 포함 여부 등을 명령줄 옵션으로  
  자유롭게 설정할 수 있습니다.
- **옵션 기본값:**  
  기본값은 상황에 맞게 설정되며, 사용자가 별도의 옵션을 지정하지 않으면 자동 감지 및 기본 설정이 적용됩니다.

## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE.md](LICENSE.md)를 참조하세요.

----

# Korean Phone Number Normalization and Formatting Tool
This project is a tool for normalizing and formatting various phone number representations in Korea—including mobile phones, landlines, long-distance, international calls, etc.—into a consistent standard format. It is based on the Telecommunications Number Management Regulations pursuant to Article 48 of the Telecommunications Business Act (Ministry of Science and ICT Notice No. 2021-93, December 7, 2021). Additionally, the tool automatically detects and converts phone number data contained in CSV and GeoJSON files.

## Features
- **Phone Number Normalization and Formatting**
  - Standardization: Converts various input formats (e.g., "010-1234-5678", "(02) 123-4567", "+82 10 1234 5678", etc.) into a single standardized format.
  - Customization Options: You can choose whether to include the country code and whether to remove the leading zero. For example:
    - `--country True --strip-zero False` → "+82 010-1234-5678"
    - `--country True --strip-zero True` → "+82 10-1234-5678"
    - `--country False` → "010-1234-5678" (or "10-1234-5678" if the leading zero is removed)

- **File Format Support**
  - **CSV Files**: Accepts CSV files containing phone numbers by automatically detecting the phone number column or using a user-specified column for conversion.
  - **GeoJSON Files**: Automatically detects the property containing phone numbers within each feature’s properties or uses a user-specified property for conversion. Depending on the --split-results option, the tool can either duplicate the feature to separate multiple results or combine them with semicolons within a single feature. If a GeoJSON feature does not contain the specified phone number property, that feature remains unchanged.

## Usage
### Installation
- Requirements
  - Python 3 or higher is required.
  - No additional external libraries are needed.

### Command Line Execution
**Options**
- `--input` (Required): Input file path (CSV or GeoJSON).
- `--output`: Output file path (if omitted, `_processed` is appended to the input file name).
- `--column`: Phone number column in CSV files (automatically detected if not specified).
- `--property`: Phone number property in GeoJSON files (automatically detected if not specified).
- `--header`: Specifies whether the file has a header (True/False; default: `False`).
- `--delimiter`: Output delimiter (options: `hyphen`, `space`, `dot`, `none`; default: `hyphen`).
- `--country`: Whether to include the country code (True/False; default: False). 
  - If `True`, for example, "010-1234-5678" becomes "+82 010-1234-5678" (subject to the strip-zero option).
- `--strip-zero`: Whether to remove the leading zero (True/False; default: `False`).
  - If `True`, "010" becomes "10" and "02" becomes "2".
- `--deobfuscate`: Whether to restore obfuscated characters (True/False; default: `True`).
- `--split-results`: Whether to output multiple results as separate rows (True/False; default: `True`).
- `--include-service`: Whether to include a service classification column (True/False; default: `False`).

**Example Commands**
- Processing a CSV file (default options):
`python main.py --input your_input.csv --column PhoneNumber`

- Processing a CSV file (including country code, preserving leading zero):
`python main.py --input your_input.csv --column PhoneNumber --country True --strip-zero False`

- Processing a CSV file (including country code, removing leading zero):
`python main.py --input your_input.csv --column PhoneNumber --country True --strip-zero True`

- Processing a GeoJSON file:
`python main.py --input your_input.geojson --property PhoneNumber`

## Feature Description
### 1. Phone Number Normalization and Formatting
- **Handling Various Input Formats:**  
  Supports various forms of phone number inputs, including Korean mobile phones, local phones, long-distance calls, and international calls.  
  Input phone numbers may include separators such as hyphens, spaces, parentheses, dots, tildes, etc., and also handle country code (e.g., +82).

- **Normalization:**  
  Extracts only the digits from the input phone number and converts it into a normalized form (e.g., "01012345678").

- **Formatting:**  
  Transforms the normalized number into the desired format based on user options (e.g., "010-1234-5678" or "+82 010-1234-5678").  
  The output varies according to the `--country` and `--strip-zero` options.
  - **ITU-T E.123 / DIN 5008**: A pattern that separates the country code, area code, and local number with spaces.
    - `python main.py --input input.csv --country True --delimiter space --strip-zero False`: The leading zero in the area code is preserved.
      - Example: `+82 010 1234 5678`
    - `python main.py --input input.csv --country True --delimiter space --strip-zero True`: The leading zero in the area code is removed.
      - Example: `+82 10 1234 5678`
  
  - **RFC 3966 / NANP**: A pattern that separates the country code, area code, and local number with hyphens.
    - `python main.py --input input.csv --country True --delimiter hyphen --strip-zero False`: The leading zero in the area code is preserved.
      - Example: `+82 010-1234-5678`
    - `python main.py --input input.csv --country True --delimiter hyphen --strip-zero True`: The leading zero in the area code is removed.
      - Example: `+82 10-1234-5678`
  
  - **Domestic Phone Network Numbers**: A pattern that separates the area code and local number with either hyphens or spaces without including the country code. The `--country` parameter is not specified.
    - `python main.py --input input.csv --delimiter space --strip-zero False`: Numbers are separated by spaces, and the leading zero in the area code is preserved.
      - Example: `010 1234 5678`
    - `python main.py --input input.csv --delimiter space --strip-zero True`: Numbers are separated by spaces, and the leading zero in the area code is removed.
      - Example: `10 1234 5678`
    - `python main.py --input input.csv --delimiter hyphen --strip-zero False`: Numbers are separated by hyphens, and the leading zero in the area code is preserved.
      - Example: `010-1234-5678`
    - `python main.py --input input.csv --delimiter hyphen --strip-zero True`: Numbers are separated by hyphens, and the leading zero in the area code is removed.
      - Example: `10-1234-5678`

### 2. File Processing Functionality (CSV and GeoJSON)
- **CSV File Processing**:
  - Automatically detects the column containing phone numbers or allows the user to specify it.
  - For each row, performs phone number normalization and formatting, then adds the results into new columns: "Normalized", "Formatted" (and "_Service" if the option is enabled).
  - When the `--split-results` option is `True`, if a cell contains multiple phone numbers, each result can be output in a separate row or combined in one cell with semicolons.

- **GeoJSON File Processing**:
  - Automatically detects the property containing phone numbers within each feature’s properties or allows the user to specify it.
  - If the specified property exists, performs phone number normalization and formatting, then appends new properties with names suffixed by "_Normalized" and "_Formatted" (and "_Service" if the option is enabled).
  - Depending on the `--split-results` option, if there are multiple phone numbers, the feature can be duplicated so that each result appears as a separate feature, or the results can be combined within a single feature.

### 3. Deobfuscation
- Restores obfuscated characters used in place of digits or hyphens in the input phone numbers (for example, characters like "O", "영", "공", etc.) back to their correct numeric form and hyphen using an internal mapping. This feature is enabled by default and helps reduce notation errors.

### 4. Service Classification
- Analyzes the beginning part of the phone number (such as identification numbers or area codes) to classify it into various categories such as:
  - Emergency numbers
  - Special numbers
  - International telephone operators
  - Long-distance telephone operators
  - Satellite mobile phone operators
  - Wireless call service operators
  - Specific subscriber services
  - Additional telecommunication service providers
  - Internet telephony operators
  - IoT communication operators
  - Personal number services
  - Mobile phone operators
  - Landline (public switched telephone network) operators
- This classification provides additional information about the type of service associated with the phone number data.

### 5. Flexible Option Settings
- **User-Defined Options**:
- You can freely configure various options via command line, including:
  - Whether the file has a header
  - Specifying the phone number column (or property)
  - Output delimiter
  - Country code inclusion
  - Removal of the leading zero
  - Deobfuscation of characters
  - Method for splitting results
  - Inclusion of a service classification column

- **Default Settings**:
Default values are chosen to suit typical scenarios. If no additional options are specified, the tool automatically detects the required fields and applies these default settings.

## License
This project is distributed under the MIT License. For more details, please refer to [LICENSE.md](LICENSE.md).
