import os
import shutil

# Dictionary storing province codes and names
province_codes = {
    "01": "THÀNH PHỐ HÀ NỘI",
    "02": "THÀNH PHỐ HỒ CHÍ MINH",
    "03": "THÀNH PHỐ HẢI PHÒNG",
    "04": "THÀNH PHỐ ĐÀ NẴNG",
    "05": "TỈNH HÀ GIANG",
    "06": "TỈNH CAO BẰNG",
    "07": "TỈNH LAI CHÂU",
    "08": "TỈNH LÀO CAI",
    "09": "TỈNH TUYÊN QUANG",
    "10": "LẠNG SƠN",
    "11": "TỈNH BẮC KẠN",
    "12": "TỈNH THÁI NGUYÊN",
    "13": "TỈNH YÊN BÁI",
    "14": "TỈNH SƠN LA",
    "15": "TỈNH PHÚ THỌ",
    "16": "TỈNH VĨNH PHÚC",
    "17": "TỈNH QUẢNG NINH",
    "18": "TỈNH BẮC GIANG",
    "19": "TỈNH BẮC NINH",
    "21": "TỈNH HẢI DƯƠNG",
    "22": "TỈNH HƯNG YÊN",
    "23": "TỈNH HÒA BÌNH",
    "24": "TỈNH HÀ NAM",
    "25": "TỈNH NAM ĐỊNH",
    "26": "TỈNH THÁI BÌNH",
    "27": "TỈNH NINH BÌNH",
    "28": "TỈNH THANH HÓA",
    "29": "TỈNH NGHỆ AN",
    "30": "TỈNH HÀ TĨNH",
    "31": "TỈNH QUẢNG BÌNH",
    "32": "TỈNH QUẢNG TRỊ",
    "33": "TỈNH THỪA THIÊN - HUẾ",
    "34": "TỈNH QUẢNG NAM",
    "35": "TỈNH QUẢNG NGÃI",
    "36": "TỈNH KON TUM",
    "37": "TỈNH BÌNH ĐỊNH",
    "38": "TỈNH GIA LAI",
    "39": "TỈNH PHÚ YÊN",
    "40": "TỈNH ĐĂK LĂK",
    "41": "TỈNH KHÁNH HÒA",
    "42": "TỈNH LÂM ĐỒNG",
    "43": "TỈNH BÌNH PHƯỚC",
    "44": "TỈNH BÌNH DƯƠNG",
    "45": "TỈNH NINH THUẬN",
    "46": "TỈNH TÂY NINH",
    "47": "TỈNH BÌNH THUẬN",
    "48": "TỈNH ĐỒNG NAI",
    "49": "TỈNH LONG AN",
    "50": "TỈNH ĐỒNG THÁP",
    "51": "TỈNH AN GIANG",
    "52": "TỈNH BÀ RỊA - VŨNG TÀU",
    "53": "TỈNH TIỀN GIANG",
    "54": "TỈNH KIÊN GIANG",
    "55": "THÀNH PHỐ CẦN THƠ",
    "56": "TỈNH BẾN TRE",
    "57": "TỈNH VĨNH LONG",
    "58": "TỈNH TRÀ VINH",
    "59": "TỈNH SÓC TRĂNG",
    "60": "TỈNH BẠC LIÊU",
    "61": "TỈNH CÀ MAU",
    "62": "TỈNH ĐIỆN BIÊN",
    "63": "TỈNH ĐẮK NÔNG",
    "64": "TỈNH HẬU GIANG"
}

# Specify the base path where folders will be created
base_path = "./data"
# Path to the folder containing the CSV files
csv_folder_path = "./data"

# List all files in the CSV folder
csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]

# Move files to corresponding folders
for file_name in csv_files:
    # Extract the province code from the file name (first two characters)
    province_code = file_name[:2]
    if province_code in province_codes:
        # Construct the destination folder path
        folder_name = f"{province_code}_{province_codes[province_code]}"
        folder_name = folder_name.replace(" ", "_")
        destination_folder = os.path.join(base_path, folder_name)
        # Ensure the destination folder exists
        os.makedirs(destination_folder, exist_ok=True)
        # Construct full paths for source and destination
        source_file = os.path.join(csv_folder_path, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        # Move the file
        shutil.move(source_file, destination_file)
        print(f"Moved file {file_name} to {destination_folder}")

print("All files moved successfully.")
