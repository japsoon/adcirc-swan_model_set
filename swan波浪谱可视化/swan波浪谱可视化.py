import matplotlib.pyplot as plt
from PIL import Image
import os
import numpy as np
import shutil

# the Specout_file_name is
Specout_file_name = "p140"
# Reading the file
with open(f"{Specout_file_name}.txt", 'r', encoding='utf-8', errors='ignore') as file:
    lines = file.readlines()

# Extracting frequencies
freq_start_index = lines.index('AFREQ                                   absolute frequencies in Hz\n') + 2
num_frequencies = int(lines[freq_start_index - 1].split()[0])
frequencies = [float(line.strip()) for line in lines[freq_start_index:freq_start_index + num_frequencies]]


# Function to extract spectra for a given location index at a given line
def extract_spectra(location_index, start_line):
    spectra_start_index = None
    for i, line in enumerate(lines[start_line:], start=start_line):
        if 'LOCATION' in line and int(line.split()[1]) == location_index:
            spectra_start_index = i + 1
            break
    if spectra_start_index is None:
        print(f"Warning: Location {location_index} not found in the file!")
        return None

    spectra_values = [float(line.split()[0]) if float(line.split()[0]) != -0.9900E+02 else np.nan for line in lines[spectra_start_index:spectra_start_index + num_frequencies]]

    return spectra_values

# Correcting the method to determine how many locations are in the file
locations_line = lines[lines.index('LONLAT                                  locations in spherical coordinates\n') + 1]
num_locations = int(locations_line.split()[0])

line_index = 0
current_timestamp = None

# 获取文件夹中所有的png文件
pic_time_step = './pic_time_step'  # 您存放PNG文件的文件夹路径
# 如果文件夹不存在，则创建它
if not os.path.exists(pic_time_step):
    os.makedirs(pic_time_step)

while line_index < len(lines):
    line = lines[line_index]

    # Check for a timestamp
    if 'date and time' in line:
        current_timestamp = line.strip()
        line_index += 1
        continue

    if current_timestamp is not None:
        for i in range(1, num_locations + 1):
            spectra_values = extract_spectra(i, line_index)
            if spectra_values is None:
                continue

            # Plotting the spectra for the current location
            plt.figure(figsize=(10, 6))
            plt.plot(frequencies, spectra_values, marker='o')
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Variance Density (m^2/Hz)")
            plt.title(f"Wave Spectrum for Location {i} at Time {current_timestamp}")
            plt.grid(True)
            plt.xscale("log")
            # plt.yscale("log")
            # plt.ylim(0, 1000)  # Set y-axis limits based on global min and max
            # plt.ylim(10 ** -12, 10 ** 3)
            plt.xlim(0.03, 1.1)  # Set x-axis limits based on global min and max

            # Modify x-axis ticks to only show specific values
            x_ticks = [0.03, 0.1, 0.5, 1.0]  # Adjust this list as needed
            plt.xticks(x_ticks, [str(x) for x in x_ticks])

            plt.savefig(f"pic_time_step/Location_{i}_Wave_Spectrum Time_{current_timestamp}.png")
            plt.close()  # Close the current figure to free memory

        current_timestamp = None

    line_index += 1

# 按照点位和时间排序文件
def sort_key(filename):
    parts = filename.split('_')
    location = int(parts[1])
    time = parts[3].split('.')[0]
    return location, time

files = [f for f in os.listdir(pic_time_step) if f.endswith('.png')]
files.sort(key=sort_key)

# 定义输出的文件夹路径
output_folder_path = f"./specout_gif_{Specout_file_name}"
# 如果文件夹不存在，则创建它
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 对于每个点位生成一个GIF
locations = set(file.split('_')[1] for file in files)
for loc in locations:
    file_group = [file for file in files if f"Location_{loc}_" in file]
    images = [Image.open(os.path.join(pic_time_step, file)) for file in file_group]

    # 使用新定义的文件夹路径来保存gif
    gif_filename = os.path.join(output_folder_path, f"Location_{loc}_time_series.gif")

    images[0].save(gif_filename, save_all=True, append_images=images[1:], loop=0, duration=400)
    print(f"Location_{loc} 生成结束")

# 在所有处理完成后，清空pic_time_step文件夹
shutil.rmtree(pic_time_step)  # 删除整个文件夹
os.makedirs(pic_time_step)    # 重新创建空的同名文件夹


