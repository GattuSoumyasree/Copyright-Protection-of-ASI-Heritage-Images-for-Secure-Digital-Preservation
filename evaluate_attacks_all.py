import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def evaluate_images(img1, img2):
    img1 = cv2.resize(img1, img2.shape[::-1])
    psnr_val = psnr(img1, img2)
    ssim_val = ssim(img1, img2)

    img1_flat = img1.flatten()
    img2_flat = img2.flatten()

    std1 = np.std(img1_flat)
    std2 = np.std(img2_flat)
    ncc_val = np.corrcoef(img1_flat, img2_flat)[0, 1] if std1 != 0 and std2 != 0 else float('nan')

    return psnr_val, ssim_val, ncc_val

# Paths
original_wm_path = 'input/watermark.jpg'
extracted_dir = 'output/extracted_from_attacks'
output_dir = 'output/evaluation'
os.makedirs(output_dir, exist_ok=True)

# Load original watermark
original_wm = cv2.imread(original_wm_path, cv2.IMREAD_GRAYSCALE)
if original_wm is None:
    raise FileNotFoundError(f"❌ Original watermark not found at {original_wm_path}")

# Attack types
attack_names = ['gaussian_noise', 'salt_pepper', 'jpeg_compression', 'gaussian_blur', 'hist_eq', 'brightness','cropped', 'rotated', 'resized', 'filtered']
results_dict = {}

# Evaluate each attack result
for i in range(1, 21):
    image_key = f"image{i}"
    results_dict[image_key] = {}
    for attack in attack_names:
        extracted_path = next(
            (os.path.join(extracted_dir, f'extracted_{attack}_image{i}{ext}') for ext in ['.png', '.jpg', '.jpeg']
             if os.path.exists(os.path.join(extracted_dir, f'extracted_{attack}_image{i}{ext}'))), None)
        if extracted_path is None:
            print(f"⚠ Extracted watermark not found for {attack} on {image_key}")
            continue

        extracted_wm = cv2.imread(extracted_path, cv2.IMREAD_GRAYSCALE)
        if extracted_wm is None:
            print(f"⚠ Failed to load extracted watermark at {extracted_path}")
            continue

        psnr_val, ssim_val, ncc_val = evaluate_images(original_wm, extracted_wm)
        results_dict[image_key][attack] = (psnr_val, ncc_val, ssim_val)
        print(f"✅ Eval for {attack} on {image_key} -> PSNR: {psnr_val:.2f}, SSIM: {ssim_val:.4f}, NCC: {ncc_val:.4f}")

# -------- Print Table and Save Results -------- #
header_top = ["Image"] + [attack.center(25) for attack in attack_names]
header_mid = [""] + ["PSNR    NCC     SSIM"] * len(attack_names)

rows = []
for i in range(1, 21):
    image_key = f"image{i}"
    row = [image_key.ljust(7)]
    for attack in attack_names:
        vals = results_dict[image_key].get(attack)
        if vals:
            psnr_val, ncc_val, ssim_val = vals
            row.append(f"{psnr_val:6.2f} {ncc_val:7.4f} {ssim_val:7.4f}")
        else:
            row.append("   N/A           N/A       N/A  ")
    rows.append(row)

cols = [header_top] + [header_mid] + rows
col_widths = [max(len(str(cols[r][c])) for r in range(len(cols))) for c in range(len(cols[0]))]

def print_sep(char="+", fill="-"):
    print(char + char.join([fill * (w + 2) for w in col_widths]) + char)

def print_row(row):
    print("|" + "|".join(f" {cell.ljust(col_widths[i])} " for i, cell in enumerate(row)) + "|")

# Save to file and print to console
results_path = os.path.join(output_dir, 'results_attacks_all.txt')
with open(results_path, 'w') as f:
    def fprint(*args): print(*args, file=f)

    fprint_sep = lambda: fprint("+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+")
    fprint_sep()
    fprint("|" + "|".join(f" {cell.center(col_widths[i])} " for i, cell in enumerate(header_top)) + "|")
    fprint_sep()
    fprint("|" + "|".join(f" {cell.center(col_widths[i])} " for i, cell in enumerate(header_mid)) + "|")
    fprint_sep()
    for row in rows:
        fprint("|" + "|".join(f" {cell.ljust(col_widths[i])} " for i, cell in enumerate(row)) + "|")
        fprint_sep()

# -------- Graphs -------- #
def plot_metric(metric_index, title, ylabel, filename):
    plt.figure(figsize=(12, 6))
    for attack in attack_names:
        y = [results_dict[f"image{i}"].get(attack, (np.nan, np.nan, np.nan))[metric_index] for i in range(1, 21)]
        x = [f"image{i}" for i in range(1, 21)]
        plt.plot(x, y, marker='o', label=attack)
    plt.title(f"{title} across Attacks")
    plt.xlabel("Image")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

plot_metric(0, "PSNR", "PSNR", "psnr_graph.png")
plot_metric(1, "NCC", "NCC", "ncc_graph.png")
plot_metric(2, "SSIM", "SSIM", "ssim_graph.png")


# Function to print separator line
def print_sep_console(char="+", fill="-"):
    print(char + char.join([fill * (w + 2) for w in col_widths]) + char)

# Print table to console
print_sep_console()
print("|" + "|".join(f" {cell.center(col_widths[i])} " for i, cell in enumerate(header_top)) + "|")
print_sep_console()
print("|" + "|".join(f" {cell.center(col_widths[i])} " for i, cell in enumerate(header_mid)) + "|")
print_sep_console()
for row in rows:
    print("|" + "|".join(f" {cell.ljust(col_widths[i])} " for i, cell in enumerate(row)) + "|")
    print_sep_console()


print(f"✅ Evaluation complete. Results saved in {output_dir}")
