import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

def select_photo():
    """Open a file dialog to select the photo."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an old photo to restore",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
    )
    return file_path

def save_restored_photo():
    """Open a file dialog to specify the save location."""
    root = tk.Tk()
    root.withdraw()
    output_path = filedialog.asksaveasfilename(
        title="Save Restored Photo",
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
    )
    return output_path

def apply_restoration(image):
    """
    Apply advanced restoration techniques to the photo.
    Includes noise reduction, edge-preserving filters, contrast enhancement, and sharpening.
    """
    try:
        print("Applying restoration...")

        # Step 1: Noise Reduction with Bilateral Filtering
        print("Step 1: Noise Reduction with Edge Preservation...")
        noise_reduced = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

        # Step 2: Enhance Contrast using CLAHE
        print("Step 2: Enhancing Contrast...")
        lab = cv2.cvtColor(noise_reduced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l_clahe = clahe.apply(l)
        lab_clahe = cv2.merge((l_clahe, a, b))
        contrast_enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

        # Step 3: Sharpen the Image
        print("Step 3: Sharpening the Image...")
        sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(contrast_enhanced, -1, sharpening_kernel)

        # Step 4: Smooth Edges for Final Touch (Gaussian Blur)
        print("Step 4: Refining Edges...")
        restored = cv2.GaussianBlur(sharpened, (0, 0), 0.5)
        
        print("Restoration completed!")
        return restored
    except Exception as e:
        raise RuntimeError(f"Error in restoration process: {e}")

def restore_photo(input_path, output_path):
    """Restore the photo using advanced techniques."""
    try:
        print("Loading the input image...")
        image = cv2.imread(input_path)
        if image is None:
            raise ValueError("Could not load the input image. Check the file path.")

        # Apply the restoration pipeline
        restored_image = apply_restoration(image)

        # Display before and after images side by side
        combined = np.hstack((image, restored_image))
        cv2.imshow("Сэргээхээс өмнө ба дараа", combined)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Save the final image
        cv2.imwrite(output_path, restored_image)
        print(f"Restored photo saved at: {output_path}")
        messagebox.showinfo("Success", f"Image restored and saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    """Main program for photo restoration."""
    input_path = select_photo()
    if not input_path:
        messagebox.showwarning("No File Selected", "Please select a valid photo.")
        return

    output_path = save_restored_photo()
    if not output_path:
        messagebox.showwarning("No Save Location", "Please specify where to save the restored photo.")
        return

    restore_photo(input_path, output_path)

if __name__ == "__main__":
    main()
