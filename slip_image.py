from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime

def create_receipt_image(data):
    # Create a new image with white background
    width = 400
    height = 600  # Increased height to accommodate more content
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        # Load fonts
        font = ImageFont.truetype('C:\\Windows\\Fonts\\tahoma.ttf', 16)
        small_font = ImageFont.truetype('C:\\Windows\\Fonts\\tahomabd.ttf', 16)
        normal_font = ImageFont.truetype('C:\\Windows\\Fonts\\tahoma.ttf', 16)
        detail_font = ImageFont.truetype('C:\\Windows\\Fonts\\tahoma.ttf', 12)
        queue_font = ImageFont.truetype('C:\\Windows\\Fonts\\tahomabd.ttf', 24)  # Bold and larger font for queue
        
        # Draw store name
        draw.text((width//2, 15), data['store_name'], font=font, fill='black', anchor='mm')
        
        # Draw queue number first with larger bold font
        draw.text((width//2, 35), f"Queue #{data['queue_number']}", font=queue_font, fill='black', anchor='mm')
        
        # Draw order ID below queue number
        draw.text((width//2, 55), f"Order ID: {data['order_id']}", font=normal_font, fill='black', anchor='mm')
        
        # Draw separator line
        y_pos = 70
        draw.line([(0, y_pos), (width, y_pos)], fill='black', width=1)
        
        # Draw headers
        y_pos += 15
        draw.text((0, y_pos), "รายการสั่งซื้อ", font=small_font, fill='black', anchor='lm')
        draw.text((width-272, y_pos), "ราคาต่อหน่วย", font=small_font, fill='black', anchor='lm')
        draw.text((width-95, y_pos), "จำนวน", font=small_font, fill='black', anchor='rm')
        draw.text((width, y_pos), "ราคารวม", font=small_font, fill='black', anchor='rm')
        
        # Draw order items
        y_pos += 20
        for item in data['order']:
            quantity = item[0]
            name = item[1]
            unit_price = item[2]
            total = quantity * unit_price
            
            # Draw main item details
            draw.text((0, y_pos), name, font=font, fill='black', anchor='lm')
            draw.text((width-205, y_pos), f"{unit_price} ฿", font=font, fill='black', anchor='lm')
            draw.text((width-95, y_pos), f"x {quantity}", font=font, fill='black', anchor='rm')
            draw.text((width, y_pos), f"{total} ฿", font=font, fill='black', anchor='rm')
            
            # Draw additional details if available
            if len(item) > 3:
                details = []
                if len(item) > 3 and item[3]:  # Sweetness
                    y_pos += 16
                    details.append(f"ความหวาน: {item[3]}")
                    draw.text((20, y_pos), details[0], font=detail_font, fill='black', anchor='lm')
                if len(item) > 4 and item[4]:  # Size
                    y_pos += 14
                    details.append(f"ขนาด: {item[4]}")
                    draw.text((20, y_pos), details[1], font=detail_font, fill='black', anchor='lm')
                if len(item) > 5 and item[5]:  # Addon
                    y_pos += 14
                    details.append(f"เพิ่มเติม: {item[5]}")
                    draw.text((20, y_pos), details[2], font=detail_font, fill='black', anchor='lm')
            
            y_pos += 20
        
        # Draw separator line
        y_pos += 5
        draw.line([(0, y_pos), (width, y_pos)], fill='black', width=1)
        
        # Calculate total
        y_pos += 20
        total = sum(item[0] * item[2] for item in data['order'])
        draw.text((width-110, y_pos), "รวมทั้งสิ้น", font=font, fill='black', anchor='rm')
        draw.text((width-15, y_pos), f"{total} ฿", font=font, fill='black', anchor='rm')
        
        # Draw thank you message
        y_pos += 30
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
            [2, "ชาเย็นปืน", 69, "10%", "S", "ไข่มุก"],
            [1, "ชาเย็นปืน", 69, None,None,None],
            [1, "ชาเย็นปืน", 69,"100%","L","ไข่มุก"],
            [1, "ชาเย็นปืน", 69]
        ]
    }
    
    # Create receipt image
    receipt_path = create_receipt_image(sample_data)
    if receipt_path:
        print(f"Receipt image created successfully: {receipt_path}")