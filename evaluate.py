import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
from tabulate import tabulate
#this evalute function evalutes the psnr ncc ssim values
def evaluate(original_path, extracted_path):
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    extracted = cv2.imread(extracted_path, cv2.IMREAD_GRAYSCALE)
    original = cv2.resize(original, extracted.shape[::-1])
    psnr_val = psnr(original, extracted)
    ssim_val = ssim(original, extracted)
    ncc_val = np.corrcoef(original.flatten(), extracted.flatten())[0, 1]
    return psnr_val, ssim_val, ncc_val

# evalute is run on all extracted images
if __name__ == "__main__":
    output_dir = "output"
    watermark_path = "input/watermark.jpg"
    eval_path = os.path.join(output_dir, "evaluation")
    os.makedirs(eval_path, exist_ok=True)

    records = []
    for filename in sorted(os.listdir(os.path.join(output_dir, "extracted"))):
        if filename.lower().endswith(".png"): #file names are ending with png
            extracted_path = os.path.join(output_dir, "extracted", filename)
            base = filename.rsplit("_", 1)[0]
            alpha = float(filename.rsplit("_", 1)[-1].replace(".png", ""))
            psnr_val, ssim_val, ncc_val = evaluate(watermark_path, extracted_path)
            records.append({
                "Image": base,
                "Alpha": alpha,
                "PSNR": psnr_val,
                "SSIM": ssim_val,
                "NCC": ncc_val
            })

    # The result is saved and organised in a table
    alphas = sorted(set([rec["Alpha"] for rec in records]))
    grouped = {}
    for rec in records:
        key = rec["Image"]
        alpha = rec["Alpha"]
        if key not in grouped:
            grouped[key] = {}
        grouped[key][alpha] = {
            "PSNR": f"{rec['PSNR']:.2f}", #upto 2 decimals
            "SSIM": f"{rec['SSIM']:.4f}", #upto 4 decimals
            "NCC": f"{rec['NCC']:.4f}" #upto 4 decimals
        }

    main_header = ["Image"] + [f"Alpha {a}" for a in alphas]
    sub_header = [""] + ["PSNR  NCC   SSIM" for _ in alphas] #table heading

    table_rows = []
    for image in sorted(grouped.keys(), key=lambda x: int(''.join(filter(str.isdigit, x)))):
        row = [image]
        for alpha in alphas:
            if alpha in grouped[image]:
                val = grouped[image][alpha]
                row.append(f"{val['PSNR']:>5}  {val['NCC']:>5}  {val['SSIM']:>6}")
            else:
                row.append("N/A")
        table_rows.append(row)

    final_table = [main_header, sub_header] + table_rows
    result_str = tabulate(final_table, headers="firstrow", tablefmt="grid")
    save_path = os.path.join(eval_path, "results.txt")
    with open(save_path, "w") as f:
        f.write(result_str)
    print(result_str)
    print(f"The Evaluation results saved at : {save_path}") #final results
