from PIL import Image
import os

# 按照点位和时间排序文件
def sort_key(filename):
    parts = filename.split('_')
    location = int(parts[1])
    time = parts[3].split('.')[0]
    return location, time

# 获取文件夹中所有的png文件
folder_path = './pic_time_step'  # 您存放PNG文件的文件夹路径
files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
files.sort(key=sort_key)

# 对于每个点位生成一个GIF
locations = set(file.split('_')[1] for file in files)
for loc in locations:
    file_group = [file for file in files if f"Location_{loc}_" in file]
    images = [Image.open(os.path.join(folder_path, file)) for file in file_group]
    gif_filename = os.path.join("./output_gifs_2", f"Location_{loc}_time_series.gif")
    images[0].save(gif_filename, save_all=True, append_images=images[1:], loop=0, duration=400)
