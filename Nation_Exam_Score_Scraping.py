foreign_language_code = {
    'N1': 'Tiếng Anh',
    'N2': 'Tiếng Nga',
    'N3': 'Tiếng Pháp',
    'N4': 'Tiếng Trung Quốc',
    'N5': 'Tiếng Đức',
    'N6': 'Tiếng Nhật',
    'N7': 'Tiếng Hàn'
}

def process_results(result):
    subject_scores = {}

    for key, value in result.items():
        clean_key = key.strip("'")  # Remove single quotes from key if present
        clean_value = value.strip("' ")  # Remove single quotes and spaces from value if present

        if clean_key == "MA_MON_NGOAI_NGU":
            foreign_language = foreign_language_code.get(clean_value, clean_value)
            subject_scores["TEN_MON_NGOAI_NGU"] = foreign_language
        else:
            subject_scores[clean_key] = clean_value

    return subject_scores

def main():
    base_url = "https://vtvapi3.vtv.vn/handlers/timdiemthi.ashx"
    results = []
    errors = []

    # Example range from 40000001 to 40000100
    start_sobaodanh = 40000001
    end_sobaodanh = 40000100

    # Create a ThreadPoolExecutor with 10 threads (adjust as needed)
    with ThreadPoolExecutor(max_workers=10) as executor, \
            tqdm(total=end_sobaodanh - start_sobaodanh + 1) as pbar:

        futures = []
        for sobaodanh in range(start_sobaodanh, end_sobaodanh + 1):
            api_url = f"{base_url}?keywords={sobaodanh}"
            futures.append(executor.submit(fetch_score, api_url, errors))

        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
            pbar.update(1)  # Update progress bar

    # Process results
    processed_results = []
    for result in results:
        processed_result = process_results(result)
        processed_results.append(processed_result[0])

    # Print or process processed_results as needed
    print("Processed results:")
    print(processed_results)

    # Print errors
    print("Errors encountered for the following numbers:")
    print(errors)

if __name__ == "__main__":
    main()
