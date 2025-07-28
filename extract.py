import os
import cv2
import numpy as np
import pywt

def descramble_image(scrambled, perm):
    flat = scrambled.flatten()
    descrambled = np.zeros_like(flat)
    descrambled[perm] = flat
    return descrambled.reshape(scrambled.shape)
def extract_watermark(watermarked_path, svd_data_path, alpha, output_dir):
    base_name = os.path.splitext(os.path.basename(watermarked_path))[0]
    data = np.load(svd_data_path)
    S_LL = data['S_original']
    U_WM = data['U_WM']
    V_WM = data['V_WM']
    perm = data['perm']

    watermarked_img = cv2.imread(watermarked_path)
    ycbcr = cv2.cvtColor(watermarked_img, cv2.COLOR_BGR2YCrCb)
    Y, _, _ = cv2.split(ycbcr)
    LL, _ = pywt.dwt2(Y, 'haar')

    LL = cv2.resize(LL, (S_LL.shape[0], S_LL.shape[0]))
    _, S_LL_mod, _ = np.linalg.svd(LL, full_matrices=False)
    S_WM_extracted = (S_LL_mod - S_LL) / alpha
    scrambled = np.dot(U_WM, np.dot(np.diag(S_WM_extracted), V_WM))
    extracted = descramble_image(scrambled, perm)

    os.makedirs(os.path.join(output_dir, "extracted"), exist_ok=True)
    output_path = os.path.join(output_dir, "extracted", f"{base_name}.png")
    cv2.imwrite(output_path, np.clip(extracted, 0, 255).astype(np.uint8))
    return output_path


# extraction is running on all watermarked images
if __name__ == "__main__":

    output_dir = "output"
    alphas = [0.1, 0.2, 0.3]
    for filename in os.listdir(os.path.join(output_dir, "watermarked")):
        if filename.lower().endswith(".png"):
            watermarked_path = os.path.join(output_dir, "watermarked", filename)
            base_name = os.path.splitext(filename)[0].rsplit("_", 1)[0]
            alpha = float(os.path.splitext(filename)[0].split("_")[-1])
            svd_data_path = os.path.join(output_dir, "svd_data", f"{base_name}_{alpha}.npz")
            extract_watermark(watermarked_path, svd_data_path, alpha, output_dir)
    print("The Extraction is completed.")
