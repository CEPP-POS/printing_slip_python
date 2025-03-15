from PIL import Image, ImageDraw, ImageFont

def create_receipt_image(data):
    width = 400  # Fixed width
    base_height = 206  # Space for headers, queue number, and footer
    line_height = 26   # Height per order item
    detail_height = 16  # Additional height per extra detail (sweetness, size, addon)
    
    # Calculate required height
    item_count = len(data['order'])
    extra_details = sum(len(item) - 3 for item in data['order'] if len(item) > 3)  # Count additional details
    content_height = item_count * line_height + extra_details * detail_height

    total_height = base_height + content_height
    
    # Create image with dynamic height
    image = Image.new('RGB', (width, total_height), 'white')
    draw = ImageDraw.Draw(image)

    try:
        # Load fonts
        font = ImageFont.truetype('fonts/tahoma.ttf', 18)
        small_font = ImageFont.truetype('fonts/tahomabd.ttf', 18)
        normal_font = ImageFont.truetype('fonts/tahoma.ttf', 18)
        detail_font = ImageFont.truetype('fonts/tahoma.ttf', 16)
        queue_font = ImageFont.truetype('fonts/tahomabd.ttf', 26)

        # Draw store name
        draw.text((width//2, 15), data['store_name'], font=font, fill='black', anchor='mm')

        # Draw queue number
        draw.text((width//2, 35), f"** คิวที่ {data['queue_number']} **", font=queue_font, fill='black', anchor='mm')

        # Draw order ID
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
            quantity, name, unit_price = item[:3]
            total = quantity * unit_price
            
            # Draw main item details
            draw.text((0, y_pos), name, font=font, fill='black', anchor='lm')
            draw.text((width-205, y_pos), f"{unit_price} ฿", font=font, fill='black', anchor='lm')
            draw.text((width-95, y_pos), f"x {quantity}", font=font, fill='black', anchor='rm')
            draw.text((width, y_pos), f"{total} ฿", font=font, fill='black', anchor='rm')

            # Draw additional details
            if len(item) > 3:
                details = []
                if item[3]:  # Type
                    y_pos += detail_height
                    details.append(f"ประเภท: {item[3]}")
                    draw.text((20, y_pos), details[-1], font=detail_font, fill='black', anchor='lm')
                    
                if len(item) > 4 and item[4]:  # Sweetness
                    y_pos += detail_height
                    details.append(f"ความหวาน: {item[4]}")
                    draw.text((20, y_pos), details[-1], font=detail_font, fill='black', anchor='lm')
                    
                if len(item) > 5 and item[5]:  # Size
                    y_pos += detail_height
                    details.append(f"ขนาด: {item[5]}")
                    draw.text((20, y_pos), details[-1], font=detail_font, fill='black', anchor='lm')
                    
                if len(item) > 6 and item[6]:  # Addon
                    y_pos += detail_height
                    details.append(f"เพิ่มเติม: {item[6]}")
                    draw.text((20, y_pos), details[-1], font=detail_font, fill='black', anchor='lm')

            y_pos += line_height

        # Draw separator line
        y_pos += 5
        draw.line([(0, y_pos), (width, y_pos)], fill='black', width=1)

        # Calculate total
        y_pos += 20
        total = sum(item[0] * item[2] for item in data['order'])
        draw.text((width-110, y_pos), "ยอดรวม", font=font, fill='black', anchor='rm')
        draw.text((width-15, y_pos), f"{total} ฿", font=font, fill='black', anchor='rm')

        # Draw thank you message
        y_pos += 30
        draw.text((width//2, y_pos), "ขอบคุณที่ใช้บริการค่ะ", font=font, fill='black', anchor='mm')

        # Save the image
        image.save('receipt.png')
        return 'receipt.png'
        
    except Exception as e:
        print(f"Error creating receipt: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    sample_data = {
        "store_name": "สุขเสมอคาเฟ่",
        "order_id": "1234567890",
        "queue_number": "10",
        "order": [
            [2, "ชานมไต้หวัน", 69,"เย็น", "10%", "S", "ไข่มุก"],
            [1, "โกโก้", 69,"ปั่น", "10%", "S", "ไข่มุก"],
            [1, "คาปูชิโน่", 69, "ร้อน","100%", "L", "ไข่มุก"],
            [1, "ลาเต้", 69,"เย็น", "10%", "S", "ไข่มุก"]
        ]
    }
    
    receipt_path = create_receipt_image(sample_data)
    if receipt_path:
        print(f"Receipt image created successfully: {receipt_path}")
