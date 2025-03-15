from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime

def create_receipt_image(data):
    # Create a new image with white background
    width = 400
    height = 500  # Increased height to accommodate more content
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        # Load fonts
        font = ImageFont.truetype('C:\\Windows\\Fonts\\tahoma.ttf', 16)
        small_font = ImageFont.truetype('C:\\Windows\\Fonts\\tahoma.ttf', 14)
        
        # Draw store name
        draw.text((width//2, 20), data['store_name'], font=font, fill='black', anchor='mm')
        
        # Draw order ID and queue number
        draw.text((width//2, 45), f"Order ID: {data['order_id']}", font=small_font, fill='black', anchor='mm')
        draw.text((width//2, 65), f"Queue #{data['queue_number']}", font=small_font, fill='black', anchor='mm')
        
        # Draw separator line
        y_pos = 90
        draw.line([(20, y_pos), (width-20, y_pos)], fill='black', width=1)
        
        # Draw headers
        y_pos += 20
        draw.text((30, y_pos), "จำนวน", font=small_font, fill='black', anchor='lm')
        draw.text((100, y_pos), "รายการสั่งซื้อ", font=small_font, fill='black', anchor='lm')
        draw.text((width-120, y_pos), "ราคา", font=small_font, fill='black', anchor='rm')
        draw.text((width-30, y_pos), "ราคารวม", font=small_font, fill='black', anchor='rm')
        
        # Draw order items
        y_pos += 25
        for item in data['order']:
            quantity, name, unit_price = item
            total = quantity * unit_price
            
            # Draw item details
            draw.text((30, y_pos), str(quantity), font=font, fill='black', anchor='lm')
            draw.text((100, y_pos), name, font=font, fill='black', anchor='lm')
            draw.text((width-120, y_pos), f"{unit_price} ฿", font=font, fill='black', anchor='rm')
            draw.text((width-30, y_pos), f"{total} ฿", font=font, fill='black', anchor='rm')
            y_pos += 25
        
        # Draw separator line
        y_pos += 10
        draw.line([(20, y_pos), (width-20, y_pos)], fill='black', width=1)
        
        # Draw subtotal
        y_pos += 25
        subtotal = sum(item[0] * item[2] for item in data['order'])
        draw.text((width-120, y_pos), "รวมเงิน", font=font, fill='black', anchor='rm')
        draw.text((width-30, y_pos), f"{subtotal} ฿", font=font, fill='black', anchor='rm')
        
        # Draw tax
        y_pos += 25
        tax = data.get('tax', 0)
        draw.text((width-120, y_pos), "ภาษี", font=font, fill='black', anchor='rm')
        draw.text((width-30, y_pos), f"{tax} ฿", font=font, fill='black', anchor='rm')
        
        # Draw total
        y_pos += 25
        total = subtotal + tax
        draw.text((width-120, y_pos), "รวมทั้งสิ้น", font=font, fill='black', anchor='rm')
        draw.text((width-30, y_pos), f"{total} ฿", font=font, fill='black', anchor='rm')
        
        # Draw thank you message
        y_pos += 40
        draw.text((width//2, y_pos), "Thank you", font=font, fill='black', anchor='mm')
        
        # Save the image
        image.save('receipt.png')
        return 'receipt.png'
        
    except Exception as e:
        print(f"Error creating receipt: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Test data
    sample_data = {
        "store_name": "SHOPNAME",
        "order_id": "1234567890",
        "queue_number": "10",
        "order": [
            [1, "ชาเย็นปืน", 69],
            [1, "ชาเย็นปืน", 69],
            [1, "ชาเย็นปืน", 69],
            [1, "ชาเย็นปืน", 69]
        ],
        "tax": 21
    }
    
    # Create receipt image
    receipt_path = create_receipt_image(sample_data)
    if receipt_path:
        print(f"Receipt image created successfully: {receipt_path}")