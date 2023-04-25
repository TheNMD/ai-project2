import os

dir_path = './raw_images'
count = 0
# Iterate directory
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1