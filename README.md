<img width="1568" height="561" alt="image" src="https://github.com/user-attachments/assets/697dff64-ce44-40ae-a149-ca04f0402a0f" /># Copyright-Protection-of-ASI-Heritage-Images-for-Secure-Digital-Preservation
🛡️ Copyright Protection of ASI Heritage Images for Secure Digital Preservation
This project implements a robust digital watermarking system to protect the intellectual property of ASI (Archaeological Survey of India) heritage images. It uses Singular Value Decomposition (SVD) techniques for embedding watermarks into images in a way that is invisible, secure, and resistant to common image-processing attacks.


**🔍 Introduction**
With the rise of digital media, protecting the ownership and authenticity of historical and cultural assets has become crucial. This project provides a secure watermarking framework that:
Embeds a digital watermark into heritage images.
Allows extraction and verification of the watermark.
Withstands various attacks (noise, rotation, compression, etc.).
Measures watermark integrity and image quality after attacks.

**✨ Features**
✅ SVD-based robust watermark embedding
✅ Extraction from both original and attacked images
✅ Batch processing of multiple files
✅ Resistance to various image-processing attacks
✅ Quality evaluation with PSNR, SSIM, and Normalized Correlation
✅ Modular Python codebase for ease of experimentation

**📁 Project Structure**
📦 Copyright Protection of ASI Heritage Images for Secure Digital Preservation
├── 📂 input
│   └── 📂 images                  # Original input images and watermark.jpg
├── 📂 output
│   ├── 📂 attacks                 # Images after various attacks (noise, blur, etc.)
│   ├── 📂 evaluation              # Evaluation metrics like PSNR, SSIM, NC
│   ├── 📂 extracted               # Watermarks extracted from original watermarked images
│   ├── 📂 extracted_from_attacks # Watermarks extracted after attacks
│   ├── 📂 svd_data                # Stores singular value decomposition matrices
│   └── 📂 watermarked             # Output images with embedded watermark
├── 📄 embed.py                   # Embeds watermark into original images
├── 📄 extract.py                 # Extracts watermark from watermarked images
├── 📄 apply_attacks_all.py       # Applies multiple types of attacks in batch
├── 📄 extract_from_attacks_all.py# Extracts watermark from attacked images
├── 📄 evaluate.py                # Evaluates image quality (PSNR, SSIM)
├── 📄 evaluate_attacks_all.py    # Evaluates watermark robustness after attacks
├── 📄 runall.py                  # Runs entire pipeline: embed → attack → extract → evaluate
├── 📄 requirements.txt           # Python libraries and dependencies


**⚙️ Requirements**
Install all dependencies using:
pip install -r requirements.txt
📌 Make sure you have Python 3.7+ installed.

**🚀 Usage**
Follow these steps in order to process your dataset end-to-end:

🔹 1. Embed Watermark into Images
Embeds the watermark into all original images and saves the results to output/watermarked/.
python embed.py


🔹 2. Extract Watermark from Clean Watermarked Images
Extracts the watermark from the clean watermarked images (before any attack) and stores results in output/extracted/.
python extract.py


🔹 3. Evaluate Watermarked Images (Pre-Attack)
Computes PSNR, SSIM, and Normalized Correlation (NC) between:

Original and watermarked images

Original and extracted watermarks

Results are stored in output/evaluation/.
python evaluate.py


🔹 4. Apply Attacks to Watermarked Images
Applies a variety of attacks (noise, rotation, compression, etc.) to watermarked images. Output is stored in output/attacks/.
python apply_attacks_all.py


🔹 5. Extract Watermark from Attacked Images
Extracts the watermark from each attacked image and stores them in output/extracted_from_attacks/.
python extract_from_attacks_all.py


🔹 6. Evaluate Watermark Robustness After Attacks
Measures the degradation of watermark quality after attacks using PSNR, SSIM, and NC between original watermark and extracted ones.
python evaluate_attacks_all.py


🔹 ✅ Optional: Run Entire Pipeline
If you want to automate all the above steps in sequence:
python runall.py

**🧪 Supported Attacks**
These are the transformations applied to test the robustness of the watermarking scheme:

| Attack Name        | Description                                             |
| ------------------ | ------------------------------------------------------- |
| `gaussian_noise`   | Adds Gaussian-distributed noise to the image            |
| `salt_pepper`      | Introduces salt-and-pepper noise (black & white specks) |
| `jpeg_compression` | Applies lossy JPEG compression                          |
| `gaussian_blur`    | Blurs the image using a Gaussian kernel                 |
| `hist_eq`          | Enhances contrast using histogram equalization          |
| `brightness`       | Alters the brightness levels                            |
| `cropped`          | Crops part of the image                                 |
| `rotated`          | Rotates the image by a certain angle                    |
| `resized`          | Scales the image (up or down)                           |
| `filtered`         | Applies filtering (like median or edge filters)         |

**📊 Evaluation Metrics**

| Metric   | Description                                                     |
| -------- | --------------------------------------------------------------- |
| **PSNR** | Peak Signal-to-Noise Ratio                                      |
| **SSIM** | Structural Similarity Index                                     |
| **NC**   | Normalized Correlation between original and extracted watermark |


**📸 Sample Results**
•	Watermark embedding was performed with three alpha values: 0.1, 0.2, and 0.3.
•	Evaluation metrics: PSNR, SSIM, and NCC were used to assess the watermark quality.


