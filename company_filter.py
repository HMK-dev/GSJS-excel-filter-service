import pandas as pd
import os

# 경로 설정
ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "data")
COMPANY_DATA_DIR = os.path.join(DATA_DIR, "company_data")  # 강소기업 데이터 폴더
PENSION_DATA_DIR = os.path.join(DATA_DIR, "pension_data")  # 국민연금 데이터 폴더
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")  # 출력 폴더

# 강소기업 명단 불러오기
def load_company_data(file_name):
    company_file_path = os.path.join(COMPANY_DATA_DIR, file_name)
    df = pd.read_excel(company_file_path, dtype=str)
    return df

# 국민연금 데이터 불러오기
def load_pension_data(file_name):
    pension_file_path = os.path.join(PENSION_DATA_DIR, file_name)
    df = pd.read_excel(pension_file_path, dtype=str)
    return df


# 강소기업만 추출하는 함수
def extract_excellent_companies(df_excellent, df_pension):
    excellent_ids = set(df_excellent["사업자등록번호"].str.replace("-", "").str.strip())
    df_pension["BZOWR_RGST_NO"] = df_pension["BZOWR_RGST_NO"].str.replace("-", "").str.strip()
    df_filtered = df_pension[df_pension["BZOWR_RGST_NO"].isin(excellent_ids)]
    return df_filtered

def update_company_location(df_excellent, df_pension,
                            company_key_col="사업자등록번호",
                            pension_key_col="BZOWR_RGST_NO",
                            company_address_col="소재지",
                            pension_address_col="WKPL_LTNO_DTL_ADDR"):
    """
    국민연금 데이터에서 주소를 추출하여 강소기업 엑셀에 소재지 컬럼을 업데이트합니다.
    각 컬럼명은 함수 매개변수로 지정할 수 있습니다.
    """
    # 빈값 처리
    df_excellent[company_address_col] = df_excellent[company_address_col].fillna("")
    df_pension[company_address_col] = df_pension[pension_address_col].fillna("")

    # 인덱스 설정
    df_excellent.set_index(company_key_col, inplace=True)
    df_pension.set_index(pension_key_col, inplace=True)

    # 업데이트 수행
    df_excellent.update(df_pension[[company_address_col]])

    # 인덱스 복원
    df_excellent.reset_index(inplace=True)
    df_pension.reset_index(inplace=True)

    return df_excellent

# 옵션 1: 국민연금 데이터에서 강소기업만 추출
def run_filter_companies():
    print("📄 강소기업 엑셀 파일명을 입력하세요 (예: 강소기업_명단.xlsx):")
    company_file = input().strip()
    df_excellent = load_company_data(company_file)

    print("📌 하나의 파일만 처리하려면 1, 여러 개를 처리하려면 2를 입력하세요:")
    mode = input().strip()

    if mode == "1":
        print("📄 처리할 국민연금 엑셀 파일명을 입력하세요 (예: 국민연금_202401.xlsx):")
        pension_file = input().strip()
        df_pension = load_pension_data(pension_file)

        df_filtered = extract_excellent_companies(df_excellent, df_pension)

        print("💾 저장할 파일명을 입력하세요 (예: filtered_202401.xlsx):")
        output_file = input().strip()
        df_filtered.to_excel(os.path.join(OUTPUT_DIR, output_file), index=False)
        print(f"✅ 저장 완료: {output_file}")

    elif mode == "2":
        print("📁 국민연금 데이터가 저장된 디렉토리에서 모든 파일을 처리합니다.")
        pension_files = os.listdir(PENSION_DATA_DIR)
        for file in pension_files:
            if file.endswith(".xlsx"):
                df_pension = load_pension_data(file)
                df_filtered = extract_excellent_companies(df_excellent, df_pension)

                output_name = f"filtered_{file}"
                df_filtered.to_excel(os.path.join(OUTPUT_DIR, output_name), index=False)
                print(f"✅ 저장 완료: {output_name}")
    else:
        print("❌ 잘못된 입력입니다.")

# 옵션 2: 소재지를 강소기업 파일로 덮어쓰기
def run_update_location():
    print("📄 강소기업 엑셀 파일명을 입력하세요 (예: 강소기업_명단.xlsx):")
    company_file = input().strip()
    df_excellent = load_company_data(company_file)

    print("📄 국민연금 엑셀 파일명을 입력하세요 (예: 국민연금_202401.xlsx):")
    pension_file = input().strip()
    df_pension = load_pension_data(pension_file)

    updated_df = update_company_location(df_excellent, df_pension)

    print("💾 저장할 파일명을 입력하세요 (예: updated_location.xlsx):")
    output_file = input().strip()
    updated_df.to_excel(os.path.join(OUTPUT_DIR, output_file), index=False)
    print(f"✅ 저장 완료: {output_file}")

# 메인 콘솔 인터페이스
def main():
    while True:
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