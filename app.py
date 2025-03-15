import win32print
from PIL import Image
import tempfile

def print_image(image_path):
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Convert the image to monochrome (1-bit)
        image = image.convert('1')
        
        # Resize image if needed (adjust width according to your printer's specs)
        MAX_WIDTH = 384  # Standard width for many thermal printers
        if image.size[0] > MAX_WIDTH:
            ratio = MAX_WIDTH / float(image.size[0])
            height = int(float(image.size[1]) * ratio)
            image = image.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)
        
        # Get image dimensions
        width = image.size[0]
        height = image.size[1]
        
        # Get the default printer
        printer_name = win32print.GetDefaultPrinter()
        
        # Open the printer
        printer_handle = win32print.OpenPrinter(printer_name)
        try:
            # Start a print job
            job_info = win32print.StartDocPrinter(printer_handle, 1, ("Image", None, "RAW"))
            try:
                # Start a page
                win32print.StartPagePrinter(printer_handle)
                
                # Initialize printer
                init_commands = bytes([0x1B, 0x40])  # ESC @ - Initialize printer
                win32print.WritePrinter(printer_handle, init_commands)
                
                # Set raster mode
                raster_mode = bytes([0x1D, 0x76, 0x30, 0x00])
                
                # Calculate bytes per line (width needs to be divided by 8 since each byte represents 8 pixels)
                bytes_per_line = (width + 7) // 8
                
                # Prepare image data header
                # GS v 0 - Raster format
                # xL xH yL yH - image dimensions (little endian)
                header = raster_mode + bytes([bytes_per_line & 0xFF, bytes_per_line >> 8, height & 0xFF, height >> 8])
                win32print.WritePrinter(printer_handle, header)
                
                # Convert image to bytes
                pixels = list(image.getdata())
                # Process pixels into bytes (8 pixels per byte)
                bytes_data = bytearray()
                for y in range(height):
                    for x in range(0, width, 8):
                        byte = 0
                        for bit in range(8):
                            if x + bit < width:
                                # Black pixels (0) should be printed, white pixels (255) should not
                                if pixels[y * width + x + bit] == 0:
                                    byte |= (1 << (7 - bit))
                        bytes_data.append(byte)
                
                # Send image data
                win32print.WritePrinter(printer_handle, bytes(bytes_data))
                
                # Feed and cut paper
                end_commands = bytes([0x1B, 0x64, 0x05])  # Feed 5 lines
                win32print.WritePrinter(printer_handle, end_commands)
                
                # End the page
                win32print.EndPagePrinter(printer_handle)
                
            finally:
                # End the document
                win32print.EndDocPrinter(printer_handle)
        finally:
            # Close the printer
            win32print.ClosePrinter(printer_handle)
            
        print(f"Successfully sent {image_path} to printer {printer_name}")
        
    except Exception as e:
        print(f"Error printing image: {str(e)}")

if __name__ == "__main__":
    # Print the image
    print_image('receipt.png')