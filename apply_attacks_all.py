import cv2
import numpy as np
import os
#applying guassian noise
def add_gaussian_noise(image, mean=0, var=10):
    sigma = var ** 0.5
    gaussian = np.random.normal(mean, sigma, image.shape).astype(np.float32)
    noisy_image = image.astype(np.float32) + gaussian
    return np.clip(noisy_image, 0, 255).astype(np.uint8)
#applying salt pepper
def add_salt_pepper_noise(image, salt_prob=0.01, pepper_prob=0.01):
    noisy_image = image.copy()
    total_pixels = image.size
    num_salt = int(np.ceil(salt_prob * total_pixels))
    coords = [np.random.randint(0, i, num_salt) for i in image.shape]
    noisy_image[tuple(coords)] = 255
    num_pepper = int(np.ceil(pepper_prob * total_pixels))
    coords = [np.random.randint(0, i, num_pepper) for i in image.shape]
    noisy_image[tuple(coords)] = 0
    return noisy_image
#applying jpeg compression
def jpeg_compression(image, quality=30):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, enc_img = cv2.imencode('.jpg', image, encode_param)
    return cv2.imdecode(enc_img, cv2.IMREAD_GRAYSCALE)
#applying guassian blur
def gaussian_blur(image, ksize=3):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)
#applying histgram equalization
def histogram_equalization(image):
    return cv2.equalizeHist(image)
#applying brightness
def adjust_brightness(image, factor=1.2):
    return np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)
#applying crop
def apply_crop(image):
    h, w = image.shape
    return image[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
#applying rotation
def apply_rotation(image, angle=15):
    h, w = image.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
    return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REFLECT)
#applying resize attack
def apply_resize(image, scale=0.5):
    h, w = image.shape
    small = cv2.resize(image, (int(w*scale), int(h*scale)))
    return cv2.resize(small, (w, h))
#applying filtering
def apply_filtering(image, ksize=3):
    return cv2.medianBlur(image, ksize)

# setting up the directory
watermarked_dir = 'output/watermarked'
output_dir = 'output/attacks'
os.makedirs(output_dir, exist_ok=True)

# Attacks
attacks = {
    'gaussian_noise': add_gaussian_noise,
    'salt_pepper': add_salt_pepper_noise,
    'jpeg_compression': jpeg_compression,
    'gaussian_blur': gaussian_blur,
    'hist_eq': histogram_equalization,
    'brightness': adjust_brightness,
    'cropped': apply_crop,
    'rotated': apply_rotation,
    'resized': apply_resize,
    'filtered': apply_filtering
}
#running for all 20
for i in range(1, 21):
    extensions = ['.png', '.jpg', '.jpeg']
    img_path = None
    for ext in extensions:
        candidate = os.path.join(watermarked_dir, f'image{i}_0.1{ext}')
        if os.path.exists(candidate):
            img_path = candidate
            break
    if img_path is None:
        print(f" not find watermarked image{i}")
        continue

    watermarked = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if watermarked is None:
        print(f"Loading failed{img_path}")
        continue

    for name, func in attacks.items():
        try:
            attacked = func(watermarked)
            out_path = os.path.join(output_dir, f'{name}_image{i}.png')
            cv2.imwrite(out_path, attacked)
            print(f"{name} attack on image{i} saved")
        except Exception as e:
            print(f"Failed {name} on image{i}: {e}")