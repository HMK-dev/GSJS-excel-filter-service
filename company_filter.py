import pandas as pd
import os
import sys
import time
import random
import re


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
    return address.split()[0]

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
     *  무한공간  *
     * * * * * * *

        """,
    ]

    final_text = """
    ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    ★                                                  ★
    ★             무 한 영 역 전 개                     ★
    ★              INFINITE VOID                       ★
    ★                                                  ★
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

    # 컬럼 자동 감지
    excellent_cols = detect_columns(df_excellent)

    pension_cols = detect_columns(df_pension)

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
        excellent_companies[key] = idx


    # 국민연금 데이터의 회사명 컬럼 확인
    company_name_col = df_pension.columns[1]
    if not company_name_col:
        print("❌ 국민연금 데이터에서 회사명/사업장명 컬럼을 찾을 수 없습니다.")
        return pd.DataFrame()

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
        pension_bizno = str(row[pension_bizno_col]).replace("-", "").zfill(10)
        key = (pension_company, pension_bizno[:6])

        # 정규화된 회사명으로 비교 및 사업자등록번호 비교
        if key in excellent_companies:
            filtered_rows.append(row)

    df_filtered = pd.DataFrame(filtered_rows)
    print(f"✅ 필터링 완료: 총 {len(df_filtered)}개의 강소기업이 발견되었습니다.")

    return df_filtered


def update_company_location(df_excellent, df_pension):
    """
    국민연금 데이터에서 주소를 추출하여 강소기업 엑셀에 소재지 컬럼을 업데이트합니다.
    """
    print(f"🔄 강소기업 {len(df_excellent)}개와 국민연금 데이터 {len(df_pension)}개를 비교합니다...")
    print("\n    [ 고죠 사토루: 무한의 가능성 속에서 답을 찾겠어... ]\n")
    time.sleep(1)

    gojo_domain_expansion()

    # 컬럼 자동 감지
    excellent_cols = detect_columns(df_excellent)
    pension_cols = detect_columns(df_pension)

    excellent_company_col = "사업자명"

    # 국민연금 데이터의 필요한 컬럼 확인
    company_name_col = df_pension.columns[1]
    address_col = df_pension.columns[5]
    zip_code_col = df_pension.columns[4]


    if not company_name_col:
        print("❌ 국민연금 데이터에서 회사명/사업장명 컬럼을 찾을 수 없습니다.")
        return df_excellent


    # 새 컬럼 추가
    if '지역' not in df_excellent.columns:
        df_excellent['지역'] = ""
    if '우편번호' not in df_excellent.columns:
        df_excellent['우편번호'] = ""

    # 회사명 매핑 생성 (정규화된 이름 기준)
    company_mapping = {}
    for idx, row in df_pension.iterrows():
        if company_name_col in row and row[company_name_col]:
            normalized_name = normalize_company_name(row[company_name_col])

            # 주소 정보 저장
            company_info = {}

            if address_col and address_col in row and row[address_col]:
                company_info['region'] = extract_region(row[address_col])

            if zip_code_col and zip_code_col in row and row[zip_code_col]:
                company_info['zip_code'] = row[zip_code_col]

            company_mapping[normalized_name] = company_info

    # 진행 상황을 표시하면서 업데이트
    total_rows = len(df_excellent)
    updated_count = 0

    for i, (idx, row) in enumerate(df_excellent.iterrows()):
        if i % 10 == 0 or i == total_rows - 1:  # 10개 단위로 업데이트
            update_progress(i + 1, total_rows, '데이터 업데이트 중')

        company_name = row[excellent_company_col]
        normalized_name = normalize_company_name(company_name)

        if normalized_name in company_mapping:
            company_info = company_mapping[normalized_name]
            # 지역 컬럼 업데이트
            if 'region' in company_info:
                df_excellent.at[idx, '지역'] = company_info['region']

            # 우편번호 업데이트
            if 'zip_code' in company_info:
                df_excellent.at[idx, '우편번호'] = company_info['zip_code']

            updated_count += 1

    print(f"✅ 업데이트 완료: 총 {updated_count}개 기업의 정보가 업데이트되었습니다.")
    return df_excellent


# 옵션 1: 국민연금 데이터에서 강소기업만 추출
def run_filter_companies():
    print("📄 강소기업 엑셀 파일명을 입력하세요 (예: 강소기업_명단.xlsx):")
    company_file = input().strip()

    try:
        print(f"📝 강소기업 데이터를 불러오는 중...")
        df_excellent = load_company_data(company_file)
        print(f"✅ 강소기업 데이터 불러오기 완료: {len(df_excellent)}개 기업")

        print("📌 하나의 파일만 처리하려면 1, 여러 개를 처리하려면 2를 입력하세요:")
        mode = input().strip()

        if mode == "1":
            print("📄 처리할 국민연금 csv 파일명을 입력하세요 (예: pension_202401.csv):")
            pension_file = input().strip()

            # 영역전개 실행
            gojo_domain_expansion()
            print(f"📝 국민연금 데이터를 불러오는 중...")
            df_pension = load_pension_data(pension_file)
            print(f"✅ 국민연금 데이터 불러오기 완료: {len(df_pension)}개 항목")

            df_filtered = extract_excellent_companies(df_excellent, df_pension)

            print("💾 저장할 파일명을 입력하세요 (예: filtered_202401.xlsx):")
            output_file = input().strip()


            print(f"💾 결과를 저장하는 중...")
            df_filtered.to_excel(os.path.join(OUTPUT_DIR, output_file), index=False)
            print(f"✅ 저장 완료: {output_file} ({len(df_filtered)}개 기업)")

        elif mode == "2":
            # 영역전개 실행
            gojo_domain_expansion()

            print("📁 국민연금 데이터가 저장된 디렉토리에서 모든 파일을 처리합니다.")
            pension_files = [f for f in os.listdir(PENSION_DATA_DIR) if f.endswith(".xlsx")]

            for i, file in enumerate(pension_files):
                print(f"\n[{i + 1}/{len(pension_files)}] 📂 {file} 처리 중...")

                df_pension = load_pension_data(file)
                print(f"✅ 국민연금 데이터 불러오기 완료: {len(df_pension)}개 항목")

                df_filtered = extract_excellent_companies(df_excellent, df_pension)

                output_name = f"filtered_{file}"
                print(f"💾 결과를 저장하는 중: {output_name}")
                df_filtered.to_excel(os.path.join(OUTPUT_DIR, output_name), index=False)
                print(f"✅ 저장 완료: {output_name} ({len(df_filtered)}개 기업)")
        else:
            print("❌ 잘못된 입력입니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")


# 옵션 2: 소재지를 강소기업 파일로 덮어쓰기
def run_update_location():
    print("📄 강소기업 엑셀 파일명을 입력하세요 (예: 강소기업_명단.xlsx):")
    company_file = input().strip()

    try:
        # 영역전개 실행
        gojo_domain_expansion()
        print(f"📝 강소기업 데이터를 불러오는 중...")

        df_excellent = load_company_data(company_file)
        print(f"✅ 강소기업 데이터 불러오기 완료: {len(df_excellent)}개 기업")

        print("📄 국민연금 엑셀 파일명을 입력하세요 (예: 국민연금_202401.xlsx):")
        pension_file = input().strip()

        print(f"📝 국민연금 데이터를 불러오는 중...")
        df_pension = load_pension_data(pension_file)
        print(f"✅ 국민연금 데이터 불러오기 완료: {len(df_pension)}개 항목")

        updated_df = update_company_location(df_excellent, df_pension)

        print("💾 저장할 파일명을 입력하세요 (예: updated_location.xlsx):")
        output_file = input().strip()

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