import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def process_local_image(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        print("Please download the image manually and place it in the current directory")
        return
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Could not load the image. It might be corrupted or in an unsupported format.")
        return
    
    print("✅ Image loaded successfully!")
    print(f"   Image dimensions: {img.shape}")
    
    # Restoration parameters
    alpha = 1.8  # Contrast
    beta = 20    # Brightness
    
    # Apply restoration
    restored = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    
    # Apply CLAHE for better color correction
    lab = cv2.cvtColor(restored, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)
    lab_eq = cv2.merge([l_eq, a, b])
    final_restored = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)
    
    # Save results
    os.makedirs('output', exist_ok=True)
    cv2.imwrite('output/restored.jpg', final_restored)
    
    # Display
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Corrupted Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(final_restored, cv2.COLOR_BGR2RGB))
    plt.title(f'Restored (α={alpha}, β={beta})')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print(f"🎉 Restoration complete!")
    print(f"📊 Parameters used: Contrast (alpha)={alpha}, Brightness (beta)={beta}")
    print("💾 Restored image saved as: output/restored.jpg")

# Usage
process_local_image('corrupted_image.png')  # or whatever you named the downloaded file
