from fastapi import FastAPI
import uvicorn
import tf_code
import supabase
import json

app = FastAPI()


def is_csv_file(file_path):
    # Check if the file starts with the CSV signature
    csv_signature = b"\xEF\xBB\xBF"
    with open(file_path, "rb") as f:
        return f.read(len(csv_signature)) == csv_signature

@app.get("/")
def home():
    return {'message': "hello!"}

@app.get("/gene")
def process_file():
    gene_list_test = [
        "GRHL2",
        "GCM1",
        "NECTIN4",
        "EPPK1",
        "MSX2",
        "PARD6B",
        "SP6",
        "DLX3",
        "NFKB2",
        "LAPTM5",
        "RELB",
        "CYTH1",
        "CSRNP1",
        "ARHGAP45",
        "LCP2",
        "TNFRSF1B",
        "RASSF5",
        "HLA-A",
        "RNASET2",
        "PIM3",
        "HCLS1",
        "HLA-E",
        "CD83",
        "CD53",
        "MYO1G",
        "CORO7",
        "TAP1",
        "PTPN6",
        "LIMD2",
        "CYBA",
        "RHOG",
        "RASAL3",
        "GPSM3",
        "TRAF1",
        "CD7",
        "FMNL1",
        "RIN3",
        "ARHGAP4",
        "IL10RA",
        "TBL1XR1",
        "CSNK1A1",
        "PPP1CB",
        "SRSF6",
        "AEBP2",
        "TLK1",
        "LSM12",
        "TRA2A",
        "TMEM33",
        "ETNK1",
        "CACUL1",
        "EIF4E",
        "BAG4",
        "TRIM59",
        "HNRNPH1",
        "PDS5B",
        "ADNP",
        "SKIL",
        "LCLAT1",
        "MAPK1IP1L",
        "RO60",
        "MMS22L",
        "ANP32E",
        "SAR1A",
        "CAPZA1",
        "TOR1AIP2",
        "CNOT9",
        "CBX5",
        "MORF4L1",
        "PAFAH1B2",
        "PTBP2",
        "INO80D",
        "ENAH",
        "SBNO1",
        "CASP2",
        "TSPYL1",
        "ZNF286A",
        "MIER1",
        "NHSL1",
        "SDF4",
        "TMEM209",
        "LIN7C",
        "FAM117B",
        "TMTC3",
        "CHP1",
        "BARD1",
        "SRSF3",
        "THUMPD1",
        "ZFX",
        "RAP2C",
        "EIF2S3",
        "NAA15",
        "SOX4",
        "DCUN1D1",
        "PPP6R3",
        "HELLS",
        "CFL1",
        "CXADR",
        "RANBP17",
        "DAAM1",
        "MRPL42",
        "ARID1B",
        "ELOVL6",
        "LCOR",
        "NUCB1",
        "THRAP3",
        "ANKRD10",
        "MARCH6",
        "RAB5C",
        "KMT2C",
        "SET",
        "DPYSL2",
        "UBA6",
        "MDM4",
        "MTPAP",
        "NR6A1",
    ]
    data = tf_code.gene_output(
        "gene_list_test_file.csv", gene_list_test, "HGNC symbol", "gene_list_test_file"
    )

    # # Check if a file was uploaded
    # if "file" not in request.files:
    #     return jsonify({"error": "No file provided"}), 400

    # file = request.files["file"]

    return data
    # # Check if the file is of CSV or TSV format
    # if file and (is_csv_file(file.filename) or file.filename.endswith(".tsv")):
    #     # Save the uploaded file to a temporary location
    #     temp_path = f"/tmp/{file.filename}"
    #     file.save(temp_path)
    #     if file.filename.endswith(".tsv"):
    #         file_type = "tsv"
    #     elif file.filename.endswith(".csv"):
    #         file_type = "csv"

    #     try:
    #         # Call the tf_code.py script to process the file
    #         json_result = tf_code.file_intake(temp_path, file_type, "HGNC symbol")

    #         # Return the JSON result as the response
    #         return jsonify(json_result), 200
    #     except Exception as e:
    #         return jsonify({"error": str(e)}), 500
    # else:
    #     return (
    #         jsonify(
    #             {"error": "Invalid file format. Only CSV and TSV files are allowed."}
    #         ),
    #         400,
    #     )


uvicorn.run(app)