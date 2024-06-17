# Medical Image Processing App

A user-friendly application for processing and analyzing medical images. This app provides functionalities such as image loading, processing, saving, zooming, and region of interest (ROI) selection. It supports real-time image processing and batch processing for multiple images.

## Features

- **Load Image**: Load medical images in various formats (JPG, PNG, BMP).
- **Process Image**: Apply Gaussian blur, Canny edge detection, and segmentation thresholds to process the image.
- **Save Processed Image**: Save the processed image to your local storage.
- **Clear Display**: Clear the displayed images and reset the app.
- **Zoom**: Adjust the zoom level of the loaded image.
- **Show Histogram**: Display the histogram of the loaded image.
- **Real-Time Processing**: Enable or disable real-time image processing as parameters are adjusted.
- **ROI Selection**: Select and save a region of interest from the loaded image.
- **Batch Processing**: Process multiple images in a selected folder.
- **Histogram Update**: View histogram statistics (mean and standard deviation) of the loaded image.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/medical-image-processing-app.git
    cd medical-image-processing-app
    ```

2. **Install dependencies**:
    Make sure you have Python installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python app.py
    ```

## Dependencies

- `tkinter`: For creating the GUI.
- `opencv-python`: For image processing.
- `numpy`: For numerical operations.
- `Pillow`: For image handling in Tkinter.
- `matplotlib`: For displaying histograms.

Install these dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt

Usage
Load an Image:

Click on "Load Image" to select an image file.
Process the Image:

Adjust the Gaussian blur kernel size, Canny edge detection thresholds, and segmentation threshold using the sliders.
Click "Process Image" to apply the selected processing techniques.
Save the Processed Image:

Click "Save Processed Image" to save the processed image.
Show Histogram:

Click "Show Histogram" to display the histogram of the loaded image.
ROI Selection:

Draw a rectangle on the displayed image by clicking and dragging the mouse to select a region of interest.
Click "Save ROI Image" to save the selected region.
Batch Processing:

Select the "Batch Processing" option from the Tools menu.
Choose a folder containing images to process all images in the folder.

# Screenshots
## Main Interface

## Processed Image

## Histogram

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

About
This Medical Image Processing App is designed to assist in the analysis and processing of medical images, providing essential tools for researchers and healthcare professionals.


Make sure to include the actual screenshots in the `screenshots` folder and adjust the paths accordingly. Replace `yourusername` with your actual GitHub username in the repository URL. Adjust the content as necessary to match your specific implementation and project details.
