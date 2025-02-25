import qrcode

# Function to generate a QR code
def generate_qr_code(data, filename="qr_code.png"):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # Version 1 is the smallest, you can change this if you need more data capacity
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Low error correction (you can adjust this)
        box_size=10,  # Size of each box in the QR code grid
        border=4,  # Thickness of the border
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill="black", back_color="white")

    # Save the image to a PNG file
    img.save(filename)
    print(f"QR code saved as {filename}")

# Prompt the user for input text
if __name__ == "__main__":
    data = input("Enter the text or URL you want to encode in the QR code: ")
    generate_qr_code(data)
