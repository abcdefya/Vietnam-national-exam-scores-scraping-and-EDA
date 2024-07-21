import time
import pandas as pd
import requests
import concurrent.futures
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import locale
# Import the dictionary from province_codes.py
from province_codes import province_codes


# Set locale for proper encoding
locale.setlocale(locale.LC_ALL, '')


# Function to sending GET method to request result from api
def test_api_response(sbd):
    url = f"https://vtvapi3.vtv.vn/handlers/timdiemthi.ashx?keywords={sbd}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check HTTP status code
        data = response.json()
        if isinstance(data, dict) and data.get("result") != "Không tìm thấy thông tin thí sinh":
            return data
        elif isinstance(data, list) and data:
            # Assume the first element contains the required information
            return data[0]
    except requests.RequestException:
        pass
    return None


# Function to find maximum SBD using binary search
def find_max_sbd_for_province(province_code, province_name):
    print(f"Getting maximum candidates for {province_name}...Please wait!!!")
    sbd = province_code + '000000'
    max_sbd = ""
    sbd_len = len(sbd)
    sbd_int = int(sbd)
    high = sbd_int + int('9' * (sbd_len - len(province_code)))
    low = sbd_int

    while low <= high:
        mid = (low + high) // 2
        mid_sbd = f"0{str(mid)}" if sbd[0] == '0' else str(mid)
        result = test_api_response(mid_sbd)

        if result:
            max_sbd = mid_sbd
            low = mid + 1
        else:
            high = mid - 1

    return province_code, province_name, max_sbd

# Function to find maximum SBD which is the largest number of candidates of a province (Multithread) and binary seach


def find_parsbd_max(province_codes, num_workers=4):
    result_dict = {}
    total_tasks = len(province_codes)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(find_max_sbd_for_province,
                            province_code, province_name)
            for province_code, province_name in province_codes.items()
        ]

        for future in tqdm(as_completed(futures), total=total_tasks, desc="Processing provinces"):
            province_code, province_name, max_sbd = future.result()
            result_dict[province_code] = {
                "province_name": province_name, "max_sbd": max_sbd}

    return result_dict


# Function to get data from one API calling
def fetch_data(base_url, keyword):
    url = f"{base_url}?keywords={keyword}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        if response.status_code == 200:
            return response.json(), keyword
        else:
            return None, keyword
    except requests.exceptions.RequestException:
        return None, keyword


# Function to get data from single province using multithread
def fetch_multiple(base_url, start_sbd, end_sbd, max_workers=16):
    results = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_data, base_url, f"{i:08d}")
            for i in range(start_sbd, end_sbd + 1)
        ]

        with tqdm(total=end_sbd - start_sbd + 1) as pbar:
            for future in concurrent.futures.as_completed(futures):
                result, keyword = future.result()
                if result:
                    results.extend(result)
                else:
                    errors.append(keyword)
                pbar.update(1)
    return results, errors


# Function to convert fields to Vietnamese
def convert_keys(data_list):
    key_map = {
        'SINH': 'Sinh học',
        'TOAN': 'Toán',
        'NGOAI_NGU': 'Ngoại ngữ',
        'HOA': 'Hóa học',
        'VAN': 'Ngữ Văn',
        'DIA': 'Địa Lí',
        'MA_MON_NGOAI_NGU': 'Mã môn ngoại ngữ',
        'id': 'ID',
        'SU': 'Lịch Sử',
        'GIAO_DUC_CONG_DAN': 'GDCD',
        'SOBAODANH': 'Số báo danh',
        'LY': 'Vật Lý'
    }

    # Function to handle fields name in raw data
    def convert_single_dict(data):
        converted_data = {key_map.get(
            key, key): value for key, value in data.items()}
        ordered_data = {}
        if 'Số báo danh' in converted_data:
            ordered_data['Số báo danh'] = converted_data.pop('Số báo danh')
        if 'ID' in converted_data:
            ordered_data['ID'] = converted_data.pop('ID')
        ordered_data.update(converted_data)
        return ordered_data

    return [convert_single_dict(data) for data in data_list]


# Function to get all data from province using multithread
def get_data_of_all_provinces(province_codes, max_sbd_province, max_workers=10):
    for province_code, province_data in max_sbd_province.items():
        print(f"Getting data for {
              province_data['province_name']}...Please wait!!!")
        province_name = province_data['province_name']
        max_sbd = province_data['max_sbd']

        start_sbd = int(province_code + '000000')
        end_sbd = int(max_sbd)
        base_url = "https://vtvapi3.vtv.vn/handlers/timdiemthi.ashx"

        province_data, errors_sbd = fetch_multiple(
            base_url, start_sbd, end_sbd, max_workers=max_workers)
        province_data = convert_keys(province_data)

        df_score_exam = pd.DataFrame(province_data)
        df_error_sbd = pd.DataFrame(errors_sbd, columns=['SBD'])

        # Write result to csv
        df_score_exam.to_csv(f'{province_code}_{
                             province_name}.csv', encoding='utf-8-sig', index=False)
        df_error_sbd.to_csv(f'{province_code}_error_sbd.csv',
                            encoding='utf-8-sig', index=False)


def main():
    start_time = time.time()

    # Get maximum candidates from all provinces in Vietnam
    num_workers = 10  # Adjust the number of workers as needed
    sbd_max_dict = find_parsbd_max(province_codes, num_workers=num_workers)

    print("Get maximum candidates had been done!!")
    sbd_max_dict = dict(sorted(sbd_max_dict.items()))

    # Get scores of candidates from all provinces in Vietnam
    get_data_of_all_provinces(province_codes, sbd_max_dict, max_workers=10)
    elapsed_time = end_time - start_time
    end_time = time.time()
    print(f"Processing time: {elapsed_time:.4f} seconds")
if __name__ == "__main__":
    main()
