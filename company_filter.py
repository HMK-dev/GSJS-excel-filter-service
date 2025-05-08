import pandas as pd
import os
import sys
import time
import random
import re
import difflib

def extract_province_abbreviation(address):
    """
    전체 주소에서 도/시 이름을 축약형으로 변환합니다.
    예: '경기도' → '경기', '서울특별시' → '서울'
    """
    province_map = {
        '서울특별시': '서울', '서울시': '서울', '서울': '서울',
        '경기도': '경기', '경기': '경기',
        '인천광역시': '인천', '인천': '인천',
        '부산광역시': '부산', '부산': '부산',
        '대구광역시': '대구', '대구': '대구',
        '광주광역시': '광주', '광주': '광주',
        '대전광역시': '대전', '대전': '대전',
        '울산광역시': '울산', '울산': '울산',
        '세종특별자치시': '세종', '세종': '세종',
        '강원도': '강원', '강원': '강원',
        '충청북도': '충북', '충북': '충북',
        '충청남도': '충남', '충남': '충남',
        '전라북도': '전북', '전북': '전북',
        '전라남도': '전남', '전남': '전남',
        '경상북도': '경북', '경북': '경북',
        '경상남도': '경남', '경남': '경남',
        '제주특별자치도': '제주', '제주': '제주'
    }

    if not isinstance(address, str):
        return ""
    for full_name, short in province_map.items():
        if address.startswith(full_name):
            return short
    return ""

# 회사명을 정규화하는 함수
def normalize_company_name(name):
    """
    회사명을 정규화하여 비교가 가능하도록 합니다.
    - 모든 공백 제거
    - 소문자 변환
    - (주), 주식회사 등의 법인 형태 표현 제거
    """
    if not name or not isinstance(name, str):
        return ""

    # 소문자 변환 및 공백 제거
    name = name.lower().replace(" ", "")

    # (주), 주식회사, (유), 유한회사 등 법인 형태 표현 제거
    name = re.sub(r'[\(\［\［\「]?(주|유한|합자|합명|유)[\)\］\］\」]?', '', name)
    name = name.replace('주식회사', '').replace('유한회사', '')
    name = name.replace('합자회사', '').replace('합명회사', '')

    return name


# 컬럼명 자동 감지 함수
def detect_columns(df):
    """
    데이터프레임의 컬럼명을 검사하여 필요한 컬럼의 실제 이름을 찾습니다.
    """
    column_mapping = {
        'company_name': None,  # 회사명/사업장명
        'address': None,  # 주소/사업장지번상세주소
        'zip_code': None  # 우편번호
    }

    # 회사명/사업장명 컬럼 찾기
    for col in df.columns:
        if '사업장명' in col or 'WKPL_NM' in col:
            column_mapping['company_name'] = col
            break

    # 주소 컬럼 찾기
    for col in df.columns:
        if '사업장지번상세주소' in col or 'WKPL_LTNO_DTL_ADDR' in col:
            column_mapping['address'] = col
            break

    # 우편번호 컬럼 찾기
    for col in df.columns:
        if '우편번호' in col or 'ZIP' in col:
            column_mapping['zip_code'] = col
            break

    return column_mapping


# 지역명 추출 함수
def extract_region(address):
    if isinstance(address, str) and address.strip():
        address.split()[0]
    return ""

# 영역전개
def gojo_domain_expansion():

    frames = [

        """


           ●      


        """,

        """

          \\●/     
           ●      
          /●\\     

        """,

        """
         \\\\●//    
        \\\\●●●//   
         //●\\\\    

        """,

        """
        \\\\\\●///   
        \\\\●●●//   
        ///●\\\\\\   

        """,

        """
       \\\\\\\\●////  
       \\\\\\●●●/// 
       ////●\\\\\\\\\  

        """,

        """
      \\\\\\\\\\●///// 
      \\\\\\●●●//// 
      /////●\\\\\\\\\\ 

        """,

        """
     * * * * * * * 
     *  무량공처  *
     * * * * * * *

        """,
    ]

    final_text = """
    ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    ★                                                                           ★
    ★                             무 한 영 역 전 개                               ★
    ★                             료 이 키 텐 카 이                               ★
    ★                                                                           ★
    ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    """

    # 애니메이션 실행
    for frame in frames:
        sys.stdout.write('\r' + frame)
        sys.stdout.flush()
        time.sleep(0.3)

    print("\033[H\033[J")
    print(final_text)
    time.sleep(1)

    void_chars = "※☆★○●◎◇◆□■△▲▽▼→←↑↓↔↕◁◀▷▶♤♠♡♥♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☜☞¶†‡↕↗↙↖↘♭♩♪♬㉿㈜№㏇™㏂㏘"
    for _ in range(15):
        line = ""
        for _ in range(60):
            line += random.choice(void_chars)
        sys.stdout.write('\r' + line)
        sys.stdout.flush()
        time.sleep(0.1)


    # print("\033[H\033[J")  # 화면 지우기

    time.sleep(1)


# 경로 설정
ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "data")
COMPANY_DATA_DIR = os.path.join(DATA_DIR, "company_data")  # 강소기업 데이터 폴더
PENSION_DATA_DIR = os.path.join(DATA_DIR, "pension_data")  # 국민연금 데이터 폴더
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")  # 출력 폴더


# 진행 상황 표시 함수
def update_progress(current, total, prefix='처리 중'):
    """
    현재 진행 상황을 콘솔에 한 줄로 표시합니다.
    """
    percent = round(current / total * 100, 1)
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write(f'\r{prefix}: [{bar}] {current}/{total} ({percent}%)')
    sys.stdout.flush()

    if current == total:
        sys.stdout.write('\n')


# 강소기업 명단
def load_company_data(file_name):
    company_file_path = os.path.join(COMPANY_DATA_DIR, file_name)
    df = pd.read_excel(company_file_path, dtype=str)
    return df


# 국민연금 데이터 불러오기
def load_pension_data(file_name):
    pension_file_path = os.path.join(PENSION_DATA_DIR, file_name)
    # 엑셀 파일 읽기
    # df = pd.read_excel(pension_file_path, dtype=str)
    # CSV 파일 읽기
    df = pd.read_csv(pension_file_path, dtype=str, encoding="CP949")
    return df

# 강소기업만 추출하는 함수
def extract_excellent_companies(df_excellent, df_pension):
    print(f"🔍 총 {len(df_pension)}개의 국민연금 데이터 중에서 강소기업 {len(df_excellent)}개를 검색합니다...")

    excellent_company_col = "사업자명"
    excellent_bizno_col = "사업자등록번호"

    pension_bizno_col = df_pension.columns[2] #국민연금 사업자 등록번호 컬럼

    # 회사명 정규화 및 매핑 딕셔너리 생성
    # 회사명 + 사업자등록번호를 기준으로 매핑 딕셔너리 생성
    excellent_companies = {}
    for idx, row in df_excellent.iterrows():
        company_name = normalize_company_name(row[excellent_company_col])
        bizno = str(row[excellent_bizno_col]).replace("-","").zfill(10)
        key = (company_name, bizno[:6])
        excellent_companies[key] = {
            "index": idx,
            "full_bizno": bizno
        }

    # 국민연금 데이터의 회사명 컬럼 확인
    company_name_col = df_pension.columns[1]
    if not company_name_col:
        print("❌ 국민연금 데이터에서 회사명/사업장명 컬럼을 찾을 수 없습니다.")
        return pd.DataFrame()

    # 진행 상황을 표시하면서 필터링
    filtered_rows = []
    total_rows = len(df_pension)

    for i, (idx, row) in enumerate(df_pension.iterrows()):
        if i % 100 == 0 or i == total_rows - 1:  # 100개 단위로 업데이트
            update_progress(i + 1, total_rows, '필터링 중')

        pension_company = normalize_company_name(row[company_name_col])
        pension_bizno = str(row[pension_bizno_col]).replace("-", "")
        key = (pension_company, pension_bizno[:6])

        # 정규화된 회사명으로 비교 및 사업자등록번호 비교
        if key in excellent_companies:
            matched_info = excellent_companies[key]

            # 사업자등록번호 덮어쓰기
            df_pension.at[idx, pension_bizno_col] = matched_info["full_bizno"]

            filtered_rows.append(row)


    df_filtered = pd.DataFrame(filtered_rows)
    print(f"✅ 필터링 완료: 총 {len(df_filtered)}개의 강소기업이 발견되었습니다.")

    return df_filtered


# 강소기업만 추출하는 함수
def extract_excellent_companies_updated(df_excellent, df_pension):
    print(f"🔍 총 {len(df_pension)}개의 국민연금 데이터 중에서 강소기업 {len(df_excellent)}개를 검색합니다...")

    excellent_company_col = "사업자명"
    excellent_bizno_col = "사업자등록번호"
    excellent_address_col = "소재지"  # 강소기업 주소 컬럼명

    pension_bizno_col = df_pension.columns[2]  # 국민연금 사업자 등록번호 컬럼

    # 국민연금 데이터의 회사명 컬럼 확인
    company_name_col = df_pension.columns[1]
    if not company_name_col:
        print("❌ 국민연금 데이터에서 회사명/사업장명 컬럼을 찾을 수 없습니다.")
        return pd.DataFrame()

    # 국민연금 데이터의 주소 컬럼 (일반적으로 3번 컬럼)
    pension_address_col = df_pension.columns[3]  # 국민연금 주소 컬럼

    # 회사명 정규화 및 매핑 딕셔너리 생성
    # 회사명 + 사업자등록번호를 기준으로 매핑 딕셔너리 생성
    excellent_companies = {}
    for idx, row in df_excellent.iterrows():
        company_name = normalize_company_name(row[excellent_company_col])
        bizno = str(row[excellent_bizno_col]).replace("-", "").zfill(10)
        key = (company_name, bizno[:6])
        excellent_companies[key] = {
            "index": idx,
            "full_bizno": bizno,
            "address": row[excellent_address_col]  # 강소기업 주소 저장
        }

    # 진행 상황을 표시하면서 필터링
    filtered_rows = []
    total_rows = len(df_pension)

    # 주소 중복 처리를 위한 딕셔너리 생성
    # 각 key(회사명+사업자번호)에 대한 최적의 행을 저장
    # key: (회사명, 사업자번호 앞6자리), value: (행 데이터, 유사도 점수)
    # 추가된 부분: 중복된 key 처리를 위한 딕셔너리
    best_matches = {}

    for i, (idx, row) in enumerate(df_pension.iterrows()):
        if i % 100 == 0 or i == total_rows - 1:  # 100개 단위로 업데이트
            update_progress(i + 1, total_rows, '필터링 중')

        pension_company = normalize_company_name(row[company_name_col])
        pension_bizno = str(row[pension_bizno_col]).replace("-", "")
        key = (pension_company, pension_bizno[:6])

        # 정규화된 회사명으로 비교 및 사업자등록번호 비교
        if key in excellent_companies:
            matched_info = excellent_companies[key]

            # 추가된 부분: 주소 유사도 계산
            pension_address = str(row[pension_address_col])
            excellent_address = str(matched_info["address"])
            similarity_score = calculate_address_similarity(pension_address, excellent_address)

            # 사업자등록번호 덮어쓰기
            df_pension.at[idx, pension_bizno_col] = matched_info["full_bizno"]

            # 추가된 부분: 중복 처리 - 더 높은 유사도를 가진 행 선택
            if key in best_matches:
                if similarity_score > best_matches[key][1]:
                    # 유사도가 더 높은 경우 교체
                    best_matches[key] = (row, similarity_score)
            else:
                # 첫 등록
                best_matches[key] = (row, similarity_score)

    # 추가된 부분: 중복 제거된 최종 필터링 결과 생성
    filtered_rows = [match[0] for match in best_matches.values()]

    df_filtered = pd.DataFrame(filtered_rows)
    print(f"✅ 필터링 완료: 총 {len(df_filtered)}개의 강소기업이 발견되었습니다.")

    return df_filtered


# 추가된 부분: 주소 유사도 계산 함수
def calculate_address_similarity(address1, address2):
    """
    두 주소 간의 유사도를 계산하는 함수

    주소 전처리 후 토큰 기반 유사도를 계산
    예: "경기 광주시 왕림로 161"와 "경기도 광주시 오포읍 왕림로"의 유사도 계산

    Parameters:
    address1 (str): 첫 번째 주소
    address2 (str): 두 번째 주소

    Returns:
    float: 두 주소 간의 유사도 점수 (0.0 ~ 1.0)
    """
    # 주소 전처리: 공백 제거, 소문자 변환
    address1 = address1.strip().lower()
    address2 = address2.strip().lower()

    # 주소에서 불필요한 단어/문자 제거
    patterns_to_remove = ['(주)', '(유)', '(합)', '주식회사', '유한회사', ',', '(', ')', '.']
    for pattern in patterns_to_remove:
        address1 = address1.replace(pattern, '')
        address2 = address2.replace(pattern, '')

    # 시도 이름 표준화 (예: '경기' -> '경기도')
    sido_mapping = {
        '경기': '경기도', '서울': '서울특별시', '부산': '부산광역시',
        '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시',
        '대전': '대전광역시', '울산': '울산광역시', '세종': '세종특별자치시',
        '강원': '강원도', '충북': '충청북도', '충남': '충청남도',
        '전북': '전라북도', '전남': '전라남도', '경북': '경상북도',
        '경남': '경상남도', '제주': '제주특별자치도'
    }

    for short, full in sido_mapping.items():
        if address1.startswith(short) and not address1.startswith(full):
            address1 = address1.replace(short, full, 1)
        if address2.startswith(short) and not address2.startswith(full):
            address2 = address2.replace(short, full, 1)

    # 토큰화 (공백 기준)
    tokens1 = set(address1.split())
    tokens2 = set(address2.split())

    # 자카드 유사도 계산 (교집합 / 합집합)
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))

    if union == 0:  # 방어 코드
        return 0.0

    similarity = intersection / union
    return similarity

def update_company_location(df_excellent, df_pension):
    """
    국민연금 데이터에서 주소를 추출하여 강소기업 엑셀에 소재지 컬럼을 업데이트합니다.
    """
    print(f"🔄 강소기업 {len(df_excellent)}개와 국민연금 데이터 {len(df_pension)}개를 비교합니다...")
    print("\n    [ 고죠 사토루: 무한의 가능성 속에서 답을 찾겠어... ]\n")
    time.sleep(1)

    gojo_domain_expansion()

    excellent_company_col = "사업자명"
    excellent_bizno_col = "사업자등록번호"

    # 국민연금 데이터의 필요한 컬럼 확인
    zip_code_col = df_pension.columns[4]
    company_name_col = df_pension.columns[1]
    address_col = df_pension.columns[5]
    pension_bizno_col = df_pension.columns[2]  # 국민연금 사업자 등록번호 컬럼
    biz_detail_col = df_pension.columns[14]  # 사업장업종상세정보 컬럼 (엑셀 기준 알파벳 O)


    if not company_name_col:
        print("❌ 국민연금 데이터에서 회사명/사업장명 컬럼을 찾을 수 없습니다.")
        return df_excellent

    # 새 컬럼 추가
    if '지역' not in df_excellent.columns:
        df_excellent['지역'] = ""
    if '우편번호' not in df_excellent.columns:
        df_excellent['우편번호'] = ""
    if '사업장업종상세정보' not in df_excellent.columns:
        df_excellent['사업장업종상세정보'] = ""

    # 회사명 매핑 생성 (정규화된 이름 기준)
    print("회사명 매핑을 생성합니다.")
    company_mapping = {}
    for idx, row in df_pension.iterrows():

        pension_bizno = str(row[pension_bizno_col]).replace("-", "")
        address = str(row[address_col]).replace("-", "")
        biz_detail = str(row[biz_detail_col]).replace("-", "")

        if not pension_bizno:
            print(f"❌ {row[company_name_col]} 사업자 등록번호가 누락되었습니다.")
            continue  # 사업자등록번호가 없는 경우 건너뛰기
        if not address:
            print(f"❌ {row[company_name_col]} 주소가 누락되었습니다.")
            continue  # 주소가 없는 경우 건너뛰기
        if not biz_detail:
            print(f"❌ {row[company_name_col]} 사업장업종상세정보가 누락되었습니다.")
            continue # 사업장업종상세정보가 없는 경우 건너뛰기

        if company_name_col in row and row[company_name_col]:
            normalized_name = normalize_company_name(row[company_name_col])

            mapping_key = (normalized_name, pension_bizno)

            # 주소 정보 저장
            company_info = {}

            if zip_code_col and zip_code_col in row and row[zip_code_col]:
                company_info['zip_code'] = row[zip_code_col]
            company_info['biz_detail'] = row[biz_detail_col]

            company_mapping[mapping_key] = company_info

    print("------------")
    # 진행 상황을 표시하면서 업데이트
    total_rows = len(df_excellent)
    updated_count = 0

    for i, (idx, row) in enumerate(df_excellent.iterrows()):
        if i % 10 == 0 or i == total_rows - 1:  # 10개 단위로 업데이트
            update_progress(i + 1, total_rows, '데이터 업데이트 중')

        company_name = normalize_company_name(row[excellent_company_col])
        excellent_bizno = str(row[excellent_bizno_col]).replace("-", "")
        mapping_key = (company_name, excellent_bizno[:6])

        # df_pension에 해당 회사명이 있는지 확인하고, 없으면 건너뛴다.
        if mapping_key not in company_mapping:
            continue  # 해당 회사명이 없으면 건너뛰기


        if mapping_key in company_mapping:
            company_info = company_mapping[mapping_key]
            # 지역 컬럼 업데이트
            df_excellent.at[idx, '지역'] = extract_province_abbreviation(str(row['소재지']))

            # 우편번호 업데이트
            if 'zip_code' in company_info:
                df_excellent.at[idx, '우편번호'] = company_info['zip_code']

            df_excellent.at[idx, '사업장업종상세정보'] = company_info['biz_detail']
            updated_count += 1

    print(f"✅ 업데이트 완료: 총 {updated_count}개 기업의 정보가 업데이트되었습니다.")
    return df_excellent


# 옵션 1: 국민연금 데이터에서 강소기업만 추출
def run_filter_companies():
    print("강소기업 데이터가 경로 data/company_data/에 있는지 확인하세요.")
    print("📄 강소기업 엑셀 파일명을 입력하세요 (예: 강소기업_명단):")
    company_file = input().strip() + ".xlsx"

    try:
        print(f"📝 강소기업 데이터를 불러오는 중...")
        df_excellent = load_company_data(company_file)
        print(f"✅ 강소기업 데이터 불러오기 완료: {len(df_excellent)}개 기업")

        print("📌 하나의 파일만 처리하려면 1, 여러 개를 처리하려면 2를 입력하세요:")
        mode = input().strip()

        if mode == "1":
            print("📄 처리할 국민연금 csv 파일명을 입력하세요 (예: pension_202401):")
            pension_file = input().strip() + ".csv"

            print(f"📝 국민연금 데이터를 불러오는 중...")
            df_pension = load_pension_data(pension_file)
            print(f"✅ 국민연금 데이터 불러오기 완료: {len(df_pension)}개 항목")

            df_filtered = extract_excellent_companies_updated(df_excellent, df_pension)

            print("💾 저장할 파일명을 입력하세요 (예: filtered_202401):")
            output_file = input().strip() + ".xlsx"


            print(f"💾 결과를 저장하는 중...")
            df_filtered.to_excel(os.path.join(OUTPUT_DIR, output_file), index=False)
            print(f"✅ 저장 완료: {output_file} ({len(df_filtered)}개 기업)")

        elif mode == "2":
            # 영역전개 실행
            gojo_domain_expansion()

            print("📁 국민연금 데이터가 저장된 디렉토리에서 모든 파일을 처리합니다.")
            pension_files = [f for f in os.listdir(PENSION_DATA_DIR) if f.endswith(".csv")]

            for i, file in enumerate(pension_files):
                print(f"\n[{i + 1}/{len(pension_files)}] 📂 {file} 처리 중...")

                df_pension = load_pension_data(file)
                print(f"✅ 국민연금 데이터 불러오기 완료: {len(df_pension)}개 항목")

                df_filtered = extract_excellent_companies(df_excellent, df_pension)

                output_name = f"filtered_{file}"
                print(f"💾 결과를 저장하는 중: {output_name}")
                df_filtered.to_excel(os.path.join(OUTPUT_DIR, output_name.split(".")[0] + ".xlsx"), index=False)
                print(f"✅ 저장 완료: {output_name} ({len(df_filtered)}개 기업)")
        else:
            print("❌ 잘못된 입력입니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")


# 옵션 2: 소재지를 강소기업 파일로 덮어쓰기
def run_update_location():
    print("강소기업 데이터가 경로 data/company_data/에 있는지 확인하세요.")
    print("📄 강소기업 엑셀 파일명을 입력하세요 (예: 강소기업_명단):")
    company_file = input().strip() + ".xlsx"

    try:
        print(f"📝 강소기업 데이터를 불러오는 중...")

        df_excellent = load_company_data(company_file)
        print(f"✅ 강소기업 데이터 불러오기 완료: {len(df_excellent)}개 기업")

        print("국민연금 데이터가 경로 data/pension_data/에 있는지 확인하세요.")
        print("📄 국민연금 csv 파일명을 입력하세요 (예: pension_202401):")
        pension_file = input().strip() + ".csv"

        print(f"📝 국민연금 데이터를 불러오는 중...")
        df_pension = load_pension_data(pension_file)
        print(f"✅ 국민연금 데이터 불러오기 완료: {len(df_pension)}개 항목")

        updated_df = update_company_location(df_excellent, df_pension)

        print("💾 저장할 파일명을 입력하세요 (예: updated_gangso):")
        output_file = input().strip() + ".xlsx"

        print(f"💾 결과를 저장하는 중...")
        updated_df.to_excel(os.path.join(OUTPUT_DIR, output_file), index=False)
        print(f"✅ 저장 완료: {output_file} ({len(updated_df)}개 기업)")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")


# 메인 콘솔 인터페이스
def main():
    # 필요한 디렉토리 생성 확인
    for dir_path in [DATA_DIR, COMPANY_DATA_DIR, PENSION_DATA_DIR, OUTPUT_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"📁 디렉토리 생성: {dir_path}")

    while True:
        print("\n 고졸 사토루가 당신의 엿같은 데이터 정리를 도와준다고 합니다!")
        print("\n📊 실행할 작업을 선택하세요:")
        print("1: 국민연금 데이터에서 강소기업만 추출")
        print("2: 국민연금 데이터의 소재지를 강소기업 엑셀로 복사")
        print("q: 종료")

        choice = input("👉 입력: ").strip().lower()

        if choice == "1":
            run_filter_companies()
        elif choice == "2":
            run_update_location()
        elif choice == "q":
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다. 다시 입력해주세요.")


if __name__ == "__main__":
    main()