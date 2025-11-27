import csv
import requests
from flask import Request, jsonify

# 👇 Tumhare data folder ke RAW GitHub links
CSV_FILES = [
    "https://raw.githubusercontent.com/USERNAME/REPO/main/data/file1.csv",
    "https://raw.githubusercontent.com/USERNAME/REPO/main/data/file2.csv",
    "https://raw.githubusercontent.com/USERNAME/REPO/main/data/file3.csv",
    "https://raw.githubusercontent.com/USERNAME/REPO/main/data/file4.csv",
    # jitne bhi files ho
]

def handler(request: Request):
    user_id = request.args.get("id")

    if not user_id:
        return jsonify({"error": "Please provide ?id="}), 400

    try:
        # Every CSV file streamed one-by-one
        for csv_url in CSV_FILES:

            response = requests.get(csv_url, stream=True)
            response.encoding = "utf-8"

            lines = (line.decode("utf-8") for line in response.iter_lines())
            reader = csv.DictReader(lines)

            for row in reader:
                if row.get("id") == user_id:
                    return jsonify({
                        "status": "success",
                        "source": csv_url,
                        "data": row
                    })

        return jsonify({"status": "not_found"})

    except Exception as e:
        return jsonify({"error": str(e)})
