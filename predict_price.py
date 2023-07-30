from sklearn import tree
import csv

x = []
y = []
with open('laptops.csv', 'r') as csvfile:
    data = csv.reader(csvfile)
    for line in data:
        x.append(line[2:11])
        y.append(line[1])

    main_processor_values = {
    'AMD Ryzen 9 6900HX': 10,
    'AMD Ryzen 7 6800H': 9,
    'AMD Ryzen 5 6800H': 8,
    'AMD Ryzen 7 5800H': 9,
    'AMD Ryzen 7 6800HS': 8,
    'intel Core i9 12900H': 10,
    'intel Core i7 12700H': 9,
    'intel Core i7 1165G7': 7,
    'intel Core i7 10700T': 8,
    'intel Core i5 11500B': 6,
    'intel Core i5 10500T': 5,
    'intel Core i5 10210U': 4,
    'intel Core i5 1135G7': 6,
    'intel Core i5': 5,
    'intel Core i7 12650H': 9,
    'intel core i7 12700H': 9,
    'intel core i7 12500H': 8,
    'intel core i7 11700B': 8,
    'intel Core i5 12500H': 7,
    'intel Core i7 11370H': 9,
    'intel Core i7 1260P': 4,
    'AMD Ryzen 5 5600H': 8,
    'intel core i7 12650H': 9,
    'AMD Ryzen 5 5500U': 6,
    'intel Core i7 1250U': 6,
    'intel Core i7 1255U': 6
}

    graphics_processor_values = {
    'NVIDIA GeForce RTX 3080Ti GDDR6': 10,
    'NVIDIA GeForce RTX 3080 GDDR6': 9,
    'NVIDIA GeForce RTX 3070Ti GDDR6': 8,
    'NVIDIA GeForce RTX 3070 GDDR6': 7,
    'NVIDIA GeForce RTX 3060Ti GDDR6': 6,
    'NVIDIA GeForce RTX 3060 GDDR6': 5,
    'NVIDIA GeForce RTX 3050Ti': 4,
    'NVIDIA GeForce RTX 3050': 3,
    'NVIDIA GeForce GTX 1650': 2,
    'Intel Iris Xe': 1,
    'Radeon Graphics': 1,
    'NVIDIA GeForce RTX3050': 6,
    'intel Iris Xe': 1,
    'Intel Iris Xᵉ Graphics': 4,
    'NVIDIA GeForce RTX 3060': 5,
    'Iris Xe Graphics': 6,
    'NVIDIA GeForce RTX 3050 GDDR6': 4,
    'NVIDIA GeForce RTX 3070': 7,
    'NVIDIA GeForce MX350': 8,
    'NVIDIA GeForce MX330': 6,
    'NVIDIA RTX3050 Ti': 5,
    'intel Iris X': 5     
}

    resolution_values = {
    'FHD 1920 x 1080': 7,
    'WUXGA 1920x1200': 8,
    'QHD 2560x1440': 9,
    '3K OLED 2880 x 1620': 9,
    '4K OLED 3840 x 2400': 10,
    '2880x1800': 8,
    'WQXGA 2880x1800': 8,
    'OLED 2880x1800': 9,
    '2K': 7,
    'FHD 1920x1080': 7,
    'FHD': 6,
    'OLED 2.8K': 8,
    'FHD OLED': 9,
    'WUXGA 1920 x 1200': 8,
    '3200x2000': 8,
    'OLED 2560x1920': 8,
    '1920x1080': 7
}

    main_storage_values = {
        '2048 SSD': 10,
        '1024 SSD': 9,
        '512 SSD': 8,
        '256 SSD': 7,
        '128 SDD': 6,
        '2048': 5,
        '1024': 4,
        '512': 3,
        '256':2,
        '128':1


    }

    cpu_mapped_values = [line[:2] + [main_processor_values.get(line[2])] + line[3:] for line in x]
    gpu_cpu_mapped_values = [line[:4] + [graphics_processor_values.get(line[4])] + line[5:] for line in cpu_mapped_values]
    mapped_values = [line[:7] + [resolution_values.get(line[7])] + line[8:] for line in gpu_cpu_mapped_values]
    train_data = [line[:0] + [main_storage_values.get(line[0])] + line[1:] for line in mapped_values]

    
 
float_train_data = [[float(item) for item in line] for line in train_data]
     

clf = tree.DecisionTreeClassifier()
clf = clf.fit(float_train_data, y) 

# Give information of new laptops. informations must exist in main_storage_values and main_processor_values and  graphics_processor_values and resolution_values
new_laptops = [['512 SSD','8','intel Core i5','13.0','NVIDIA GeForce MX350','2.0','1.8','FHD','42.0'], 
              ['1024 SSD','16','intel Core i7 12700H','17.0','intel Iris X','4.0','2.1','1920x1080','60.0']]


for i in new_laptops:
    if i[0] in main_storage_values.keys():
        i[0] = main_storage_values[i[0]]
for i in new_laptops:
    if i[2] in main_processor_values.keys():
        i[2] = main_processor_values[i[2]]
for i in new_laptops:
    if i[4] in graphics_processor_values.keys():
        i[4] = graphics_processor_values[i[4]]
for i in new_laptops:
    if i[7] in resolution_values.keys():
        i[7] = resolution_values[i[7]]  

float_new_data = [[float(item) for item in line] for line in new_laptops]                              

print(clf.predict(float_new_data))

