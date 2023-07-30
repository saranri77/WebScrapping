import requests
from bs4 import BeautifulSoup
import mysql.connector
import re

url = "https://asusiran.com/shop/page/%s"

cnx = mysql.connector.connect(user='root', password='#Sarajj9636',
                               host='127.0.0.1', database='LAPTOPS')
cursor = cnx.cursor()

for i in range(5):
    response = requests.get(url % i)
    soup = BeautifulSoup(response.text, 'html.parser')
    laptops = soup.find_all('div', class_='product-wrapper')

    for laptop in laptops:
        model_element = laptop.find('h3', class_='wd-entities-title')
        model_raw = model_element.text.strip().encode('latin-1').decode('utf-8')
        model = re.sub(r'[^a-zA-Z0-9 ]+', '', model_raw).strip()

        price_element = laptop.find('span', class_='price')
        if price_element is None:
            continue

        price_bdi = price_element.find('bdi')
        if price_bdi is None:
            continue

        price = int(re.sub(r'[^\d]+', '', price_bdi.text))

    
        specifications = laptop.find('div', class_='hover-content-inner').find('ul')
        specs = specifications.find_all('li')


        storage_capacity = None
        ram_capacity = None
        main_processor = None
        display_size = None
        graphics_processor = None
        graphics_memory = None
        weight = None
        resolution = None
        battery_capacity = None

        # Extract the laptop specifications if available
        for spec in specs:
            text = spec.text.strip().encode('latin-1').decode('utf-8', 'ignore')

            if 'حافظه داخلی' in text or 'ظرفیت حافظه داخلی' in text:
                storage_capacity_match = re.search(r'\d+', text)
                if storage_capacity_match:
                    storage_capacity_value = int(storage_capacity_match.group())

                    if 'ترابایت' in text:
                        storage_capacity_value *= 1024  # Convert terabytes to gigabytes

                    if 'SSD' in text:
                        storage_capacity = f'{storage_capacity_value} SSD'
                    else:
                        storage_capacity = str(storage_capacity_value)

            elif 'حافظه رم' in text:
                ram_capacity_match = re.search(r'\d+', text)
                if ram_capacity_match:
                    ram_capacity = int(ram_capacity_match.group())

            elif text.startswith('پردازنده:') or 'پردازنده اصلی' in text or text.startswith('سری پردازنده:'):
                main_processor_parts = text.split(':')
                if len(main_processor_parts) > 1:
                    main_processor = main_processor_parts[1].strip()

            elif 'اندازه صفحه نمایش' in text:
                display_size_match = re.search(r'\d+', text)
                if display_size_match:
                    display_size = int(display_size_match.group())

            elif text.startswith('حافظه پردازنده گرافیکی') or text.startswith('حافظه گرافیکی:'):
                if 'بدون' not in text:
                    graphics_memory_match = re.search(r'\d+', text)
                    if graphics_memory_match:
                        graphics_memory = int(graphics_memory_match.group())   
                elif 'بدون' in text:
                    graphics_memory = 0         

            elif 'پردازنده گرافیکی' in text:
                graphics_processor_parts = text.split(':')
                if len(graphics_processor_parts) > 1:
                    graphics_processor = graphics_processor_parts[1].strip()

            elif 'وزن' in text:
                weight_match = re.search(r'\d+\.\d+', text)
                if weight_match:
                    weight = float(weight_match.group())

            elif 'رزولوشن' in text or text.startswith('دقت'):
                resolution_parts = text.split(':')
                if len(resolution_parts) > 1:
                    resolution = resolution_parts[1].strip()

            elif text.startswith('ظرفیت باتری') or text.startswith('باتری:'):
                battery_capacity_match = re.search(r'\d+', text)
                if battery_capacity_match:
                    battery_capacity = int(battery_capacity_match.group())

        try:
            # Insert the laptop details into the database
            cursor.execute('''INSERT INTO asus 
                            (model, price, storage_capacity, ram_capacity, main_processor, 
                            display_size, graphics_processor, graphics_memory, weight, resolution, battery_capacity)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                           (model, price, storage_capacity, ram_capacity, main_processor, display_size,
                            graphics_processor, graphics_memory, weight, resolution, battery_capacity))
            cnx.commit()
        except mysql.connector.IntegrityError as e:
            # Handle duplicate entry error
            if 'Duplicate entry' in str(e):
                print("Duplicate product:", model)
            else:
                print("Error:", str(e))

cursor.close()
cnx.close()
