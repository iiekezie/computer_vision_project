# computer_vision_project
=======
# Computer Vision Project - Image Restoration

## Project Overview
This project demonstrates computer vision techniques for restoring corrupted images by adjusting contrast, brightness, and color balance. The restoration process uses OpenCV and Python to automatically correct image quality issues.

## Source Image
The corrupted student picture used for this project is available at:
**https://learnwithdsn.com/pluginfile.php/22518/mod_assign/intro/Corrupted%20Student%20Picture.png**

## Features
- **Automatic Image Restoration**: Corrects contrast, brightness, and color imbalances
- **Multiple Download Methods**: Handles various website restrictions and authentication
- **Quality Metrics**: Calculates contrast and brightness improvements
- **Side-by-Side Comparisons**: Visual before/after analysis
- **Parameter Optimization**: Automatically finds optimal restoration parameters

## Installation

### Prerequisites
- Ubuntu 18.04 or higher
- Python 3.6+
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/iiekezie/computer_vision_project.git
cd computer_vision_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Restoration (Automated Download)
```bash
# Run the main restoration script - it will automatically download the image
python3 restore_image.py
```

### Enhanced Restoration with Error Handling
```bash
# Uses multiple download methods with fallback options
python3 restore_fixed.py
```

### Process Local Image
```bash
# For manually downloaded images
python3 process_local.py
```

## Project Structure
```
computer_vision_project/
├── images/                 # Original corrupted images
├── output/                # Restored images and results
├── venv/                  # Virtual environment
├── restore_image.py       # Main restoration script
├── restore_fixed.py       # Enhanced version with error handling
├── process_local.py       # Local image processing
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Source Image Details
- **URL**: https://learnwithdsn.com/pluginfile.php/22518/mod_assign/intro/Corrupted%20Student%20Picture.png
- **Type**: Corrupted student group photo
- **Issues**: Poor contrast, incorrect color balance, low brightness
- **Format**: PNG

## Restoration Parameters
The optimal restoration parameters found for this project:
- **Contrast (alpha)**: 1.8
- **Brightness (beta)**: 20

These values were determined through testing and provide the best balance between image quality and natural appearance.

## Technical Details

### Algorithms Used
1. **Contrast Limited Adaptive Histogram Equalization (CLAHE)**
2. **Linear Contrast/Brightness Adjustment**
3. **LAB Color Space Transformation**
4. **Automatic White Balance**
5. **Gamma Correction**

### Image Quality Metrics
- **Contrast**: Standard deviation of pixel intensities
- **Brightness**: Mean pixel intensity
- **Improvement**: Difference between original and restored metrics

## Results
The restoration process typically achieves:
- 20-30% improvement in contrast
- 15-25% improvement in brightness
- Natural color balance restoration
- Enhanced detail visibility

## Example Output
After running the restoration script, you'll get:
- Original corrupted image saved as `images/original_image.jpg`
- Restored image saved as `output/restored_image.jpg`
- Side-by-side comparison as `output/comparison.jpg`
- Full analysis report as `output/full_analysis.png`

## Troubleshooting

### Common Issues
1. **Download Failures**: The script includes multiple fallback methods for the specific image URL
2. **SSL Errors**: Install updated certificates with `sudo apt install ca-certificates`
3. **Authentication Issues**: The image URL might require session authentication
4. **Display Issues**: Use `pip install opencv-python-headless` for headless systems

### Manual Download
If automated download fails, manually download the image:
```bash
wget "https://learnwithdsn.com/pluginfile.php/22518/mod_assign/intro/Corrupted%20Student%20Picture.png" -O corrupted_image.png
```

### Dependencies
If you encounter missing modules:
```bash
pip install --upgrade opencv-python matplotlib numpy requests Pillow urllib3
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Author
Ifeanyi Ekezie
