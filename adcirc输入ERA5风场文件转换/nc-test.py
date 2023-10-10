from netCDF4 import Dataset

# 读取NetCDF文件
nc_path = "./simulation_file/fort.222.nc"
nc = Dataset(nc_path, "r")

# 查看文件的结构
print("NetCDF文件结构: \n", nc)

# 查看文件的变量
print("文件变量: \n", nc.variables.keys())

# 循环打印每一个变量
for var in nc.variables.keys():
    print("变量名称: ", var)

# # 查看某个变量的详细信息
# print("某个变量的详细信息: \n", nc.variables['air'])
#
# # 查看某个变量的属性
# print("某个变量的属性: \n", nc.variables['air'].ncattrs())
#
# # 读取某个变量的数据
# data = nc.variables['air'][:]
# print("某个变量的数据值: \n", data)