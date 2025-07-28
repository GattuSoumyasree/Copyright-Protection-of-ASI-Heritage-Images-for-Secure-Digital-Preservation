import cv2
import numpy as np
import os
import pywt

def descramble_image(scrambled, perm):
    flat_scrambled = scrambled.flatten()
    descrambled = np.zeros_like(flat_scrambled)
    descrambled[perm] = flat_scrambled
    return descrambled.reshape(scrambled.shape)

# Load original SVD and watermark SVD components
svd_data_path = 'output/svd_data'  # folder where you save npz files per image+alpha
alpha = 0.1
attacks_dir = 'output/attacks'
output_dir = 'output/extracted_from_attacks'
os.makedirs(output_dir, exist_ok=True)

for i in range(1, 21):
    # Load SVD data for image i, alpha=0.1
    svd_file = os.path.join(svd_data_path, f'image{i}_0.1.npz')
    if not os.path.exists(svd_file):
        print(f"⚠️ SVD data not found for image{i} at {svd_file}")
        continue

    data = np.load(svd_file)
    S_LL = data['S_original']
    U_WM = data['U_WM']
    V_WM = data['V_WM']
    perm = data['perm']

    for attack in ['gaussian_noise', 'salt_pepper', 'jpeg_compression', 'gaussian_blur', 'hist_eq', 'brightness','cropped', 'rotated', 'resized', 'filtered']:
        # Flexible extension search for attacked images
        extensions = ['.png', '.jpg', '.jpeg']
        attacked_path = None
        for ext in extensions:
            candidate = os.path.join(attacks_dir, f'{attack}_image{i}{ext}')
            if os.path.exists(candidate):
                attacked_path = candidate
                break
        if attacked_path is None:
            print(f"⚠️ Could not find attacked image for {attack} on image{i}")
            continue

        attacked_image = cv2.imread(attacked_path)
        if attacked_image is None:
            print(f"⚠️ Failed to load attacked image at {attacked_path}")
            continue

        attacked_ycbcr = cv2.cvtColor(attacked_image, cv2.COLOR_BGR2YCrCb)
        Y, _, _ = cv2.split(attacked_ycbcr)

        LL, (LH, HL, HH) = pywt.dwt2(Y, 'haar')
        LL_resized = cv2.resize(LL, (S_LL.shape[0], S_LL.shape[0]))
        U_LL, S_LL_modified, V_LL = np.linalg.svd(LL_resized, full_matrices=False)
        S_WM_extracted = (S_LL_modified - S_LL) / alpha

        scrambled_wm = np.dot(U_WM, np.dot(np.diag(S_WM_extracted), V_WM))
        extracted_wm = descramble_image(scrambled_wm, perm)

        out_name = f'extracted_{attack}_image{i}.png'
        output_path = os.path.join(output_dir, out_name)
        cv2.imwrite(output_path, np.clip(extracted_wm, 0, 255).astype(np.uint8))
        print(f"✅ Extracted watermark from {attack} on image{i} saved to {output_path}")
