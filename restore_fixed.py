import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
from PIL import Image
import io
import os
import urllib.request
import ssl

print("=== Enhanced Image Restoration Process ===")

def download_image_alternative():
    """Try multiple methods to download the image"""
    url = "https://learnwithdsn.com/pluginfile.php/22518/mod_assign/intro/Corrupted%20Student%20Picture.png"
    
    methods = [
        ("Method 1: Direct download with session", download_with_session),
        ("Method 2: URL opener with SSL context", download_with_urllib),
        ("Method 3: Using requests with different headers", download_with_requests_alternative)
    ]
    
    for method_name, method_func in methods:
        print(f"\n🔧 Trying {method_name}...")
        result = method_func(url)
        if result is not None:
            return result
    
    return None

def download_with_session(url):
    """Download using requests session"""
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://learnwithdsn.com/'
        })
        
        response = session.get(url, timeout=30, stream=True)
        if response.status_code == 200:
            return process_image_response(response.content)
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    return None

def download_with_urllib(url):
    """Download using urllib with SSL context"""
    try:
        # Create SSL context to avoid certificate issues
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, context=ssl_context, timeout=30) as response:
            image_data = response.read()
            return process_image_response(image_data)
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    return None

def download_with_requests_alternative(url):
    """Alternative requests method"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        if response.status_code == 200:
            return process_image_response(response.content)
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    return None

def process_image_response(image_data):
    """Process the downloaded image data"""
    try:
        # Try to open as image
        image = Image.open(io.BytesIO(image_data))
        
        # Check if it's a valid image
        if image.format not in [None, 'WEBP', 'JPEG', 'PNG', 'GIF', 'BMP']:
            # Save the raw data for inspection
            with open('images/raw_download.bin', 'wb') as f:
                f.write(image_data)
            print("   ⚠️  Downloaded content might not be an image. Saved as raw_download.bin")
            return None
        
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Convert to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return img_cv
    except Exception as e:
        print(f"   ❌ Image processing failed: {e}")
        # Save the problematic data for inspection
        with open('images/debug_download.bin', 'wb') as f:
            f.write(image_data)
        print("   💾 Saved problematic data as debug_download.bin for inspection")
        return None

def create_sample_corrupted_image():
    """Create a sample corrupted image for testing"""
    print("\n🔄 Creating sample corrupted image for demonstration...")
    
    # Create a sample image (512x512)
    height, width = 512, 512
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Add some sample content (faces, text, etc.)
    # Draw a simple face
    cv2.ellipse(img, (256, 200), (80, 100), 0, 0, 360, (255, 200, 150), -1)  # Face
    cv2.circle(img, (220, 180), 15, (255, 255, 255), -1)  # Left eye
    cv2.circle(img, (292, 180), 15, (255, 255, 255), -1)  # Right eye
    cv2.circle(img, (220, 180), 7, (0, 0, 0), -1)  # Left pupil
    cv2.circle(img, (292, 180), 7, (0, 0, 0), -1)  # Right pupil
    cv2.ellipse(img, (256, 230), (40, 20), 0, 0, 360, (150, 100, 100), -1)  # Mouth
    
    # Add text
    cv2.putText(img, 'SAMPLE STUDENT PHOTO', (100, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, 'Corrupted Version', (150, 450), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    # Corrupt the image (reduce contrast and change colors)
    corrupted = cv2.convertScaleAbs(img, alpha=0.3, beta=50)
    
    # Change color balance
    corrupted[:,:,0] = corrupted[:,:,0] * 1.2  # Boost blue
    corrupted[:,:,2] = corrupted[:,:,2] * 0.8  # Reduce red
    
    return corrupted

def restore_image_process(img, alpha=1.8, beta=20):
    """Restore the image using computer vision techniques"""
    print(f"\n🎨 Applying restoration with alpha={alpha}, beta={beta}")
    
    # Store original
    original_img = img.copy()
    original_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    
    # Calculate original metrics
    original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    original_contrast = np.std(original_gray)
    original_brightness = np.mean(original_gray)
    
    print(f"   Original - Contrast: {original_contrast:.2f}, Brightness: {original_brightness:.2f}")
    
    # Step 1: Contrast and brightness adjustment
    adjusted = cv2.convertScaleAbs(original_img, alpha=alpha, beta=beta)
    
    # Step 2: Color correction in LAB space
    lab = cv2.cvtColor(adjusted, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)
    
    # Merge back
    lab_eq = cv2.merge([l_eq, a, b])
    color_corrected = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)
    
    # Step 3: White balance
    result = automatic_white_balance(color_corrected)
    
    # Calculate final metrics
    final_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    final_contrast = np.std(final_gray)
    final_brightness = np.mean(final_gray)
    
    print(f"   Restored - Contrast: {final_contrast:.2f}, Brightness: {final_brightness:.2f}")
    print(f"   Improvement - Contrast: +{final_contrast-original_contrast:.2f}, "
          f"Brightness: +{final_brightness-original_brightness:.2f}")
    
    return original_img, result, original_contrast, original_brightness, final_contrast, final_brightness

def automatic_white_balance(img):
    """Simple automatic white balance"""
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

def display_and_save_results(original, restored, alpha, beta):
    """Display and save the results"""
    # Convert to RGB for display
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    restored_rgb = cv2.cvtColor(restored, cv2.COLOR_BGR2RGB)
    
    # Create comparison image
    comparison = np.hstack([original, restored])
    comparison_rgb = cv2.cvtColor(comparison, cv2.COLOR_BGR2RGB)
    
    # Save images
    cv2.imwrite('images/original_image.jpg', original)
    cv2.imwrite('output/restored_image.jpg', restored)
    cv2.imwrite('output/comparison.jpg', comparison)
    
    # Display results
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.imshow(original_rgb)
    plt.title('Original Corrupted Image')
    plt.axis('off')
    
    plt.subplot(2, 2, 2)
    plt.imshow(restored_rgb)
    plt.title(f'Restored Image (α={alpha}, β={beta})')
    plt.axis('off')
    
    plt.subplot(2, 1, 2)
    plt.imshow(comparison_rgb)
    plt.title('Side-by-Side Comparison (Left: Original, Right: Restored)')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('output/full_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

def main():
    """Main function"""
    # Create directories
    os.makedirs('images', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    print("1. Attempting to download the image...")
    downloaded_img = download_image_alternative()
    
    if downloaded_img is not None:
        print("✅ Successfully downloaded and processed the image!")
        img_to_process = downloaded_img
    else:
        print("❌ Could not download the image. Creating a sample for demonstration.")
        img_to_process = create_sample_corrupted_image()
        cv2.imwrite('images/sample_corrupted.jpg', img_to_process)
        print("💾 Sample corrupted image saved as 'images/sample_corrupted.jpg'")
    
    print("\n2. Starting image restoration...")
    
    # Test different parameters
    parameters_to_test = [
        (1.8, 20),   # Best guess
        (2.0, 25),   # Higher contrast
        (1.6, 15),   # Lower contrast
    ]
    
    best_improvement = 0
    best_result = None
    best_params = (1.8, 20)
    
    for alpha, beta in parameters_to_test:
        print(f"\n--- Testing α={alpha}, β={beta} ---")
        original, restored, orig_contrast, orig_brightness, final_contrast, final_brightness = restore_image_process(
            img_to_process, alpha, beta
        )
        
        improvement = (final_contrast - orig_contrast) + (final_brightness - orig_brightness)
        
        if improvement > best_improvement:
            best_improvement = improvement
            best_result = restored
            best_params = (alpha, beta)
            best_metrics = (orig_contrast, orig_brightness, final_contrast, final_brightness)
    
    print(f"\n🎯 Best parameters: α={best_params[0]}, β={best_params[1]}")
    
    # Display final results
    display_and_save_results(img_to_process, best_result, best_params[0], best_params[1])
    
    # Print final summary
    orig_contrast, orig_brightness, final_contrast, final_brightness = best_metrics
    print("\n" + "="*60)
    print("🎉 IMAGE RESTORATION COMPLETED!")
    print("="*60)
    print(f"📊 OPTIMAL PARAMETERS:")
    print(f"   - Contrast (alpha): {best_params[0]}")
    print(f"   - Brightness (beta): {best_params[1]}")
    print(f"📈 QUALITY IMPROVEMENT:")
    print(f"   - Contrast: {orig_contrast:.2f} → {final_contrast:.2f} (+{final_contrast-orig_contrast:.2f})")
    print(f"   - Brightness: {orig_brightness:.2f} → {final_brightness:.2f} (+{final_brightness-orig_brightness:.2f})")
    print("💾 OUTPUT FILES:")
    print("   - images/original_image.jpg: Original image")
    print("   - output/restored_image.jpg: Restored image")
    print("   - output/comparison.jpg: Side-by-side comparison")
    print("   - output/full_analysis.png: Complete analysis report")
    print("="*60)

if __name__ == "__main__":
    main()
