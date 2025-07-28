import os
import cv2
import numpy as np
import pywt

def logistic_map_sequence(length, x0, r):
    x = x0
    seq = [x]
    for _ in range(length - 1):
        x = r * x * (1 - x)
        seq.append(x)
    return np.array(seq)

def scramble_image(image, x0, r):
    h, w = image.shape
    seq = logistic_map_sequence(h * w, x0, r)
    perm = np.argsort(seq)
    scrambled = image.flatten()[perm].reshape((h, w))
    return scrambled, perm

def embed_watermark(original_path, watermark_path, alpha, output_dir):
    original_color = cv2.imread(original_path)
    watermark = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)

    if original_color is None or watermark is None:
        raise FileNotFoundError(f"Could not load: {original_path} or watermark")

    original_color = cv2.resize(original_color, (512, 512))
    watermark = cv2.resize(watermark, (256, 256))

    ycbcr = cv2.cvtColor(original_color, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(ycbcr)
    LL, (LH, HL, HH) = pywt.dwt2(Y, 'haar')
    U_LL, S_LL, V_LL = np.linalg.svd(LL, full_matrices=False)

    x0, r = 0.7, 3.99
    scrambled, perm = scramble_image(watermark, x0, r)
    U_WM, S_WM, V_WM = np.linalg.svd(scrambled, full_matrices=False)

    S_LL_mod = S_LL + alpha * S_WM
    LL_mod = np.dot(U_LL, np.dot(np.diag(S_LL_mod), V_LL))
    Y_mod = pywt.idwt2((LL_mod, (LH, HL, HH)), 'haar')
    Y_mod = np.clip(Y_mod, 0, 255).astype(np.uint8)

    watermarked_ycbcr = cv2.merge((Y_mod, Cr, Cb))
    watermarked_bgr = cv2.cvtColor(watermarked_ycbcr, cv2.COLOR_YCrCb2BGR)

    os.makedirs(os.path.join(output_dir, "watermarked"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "svd_data"), exist_ok=True)

    base_name = os.path.splitext(os.path.basename(original_path))[0]
    out_name = f"{base_name}_{alpha}.png"
    cv2.imwrite(os.path.join(output_dir, "watermarked", out_name), watermarked_bgr)

    np.savez(os.path.join(output_dir, "svd_data", f"{base_name}_{alpha}.npz"),
             S_original=S_LL, U_WM=U_WM, V_WM=V_WM, perm=perm)

    return out_name


# embedding is run on all 20 images
if __name__ == "__main__":
    image_dir = "input/images"
    watermark_path = "input/watermark.jpg"
    output_dir = "output"
    alphas = [0.1, 0.2, 0.3]

    for filename in sorted(os.listdir(image_dir)):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(image_dir, filename)
            for alpha in alphas:
                embed_watermark(image_path, watermark_path, alpha, output_dir)
    print("Embedding completed.")
