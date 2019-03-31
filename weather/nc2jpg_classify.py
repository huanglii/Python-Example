# -*- coding: utf-8 -*-


import os
import numpy as np
from osgeo import gdal_array
from netCDF4 import Dataset


def read_nc_data(file, var):
    """
    读取 NC 数据
    :param file: nc 文件
    :param var: 变量
    :return:
    """
    ds = Dataset(file, mode='r')
    val = ds.variables[var][:]
    ds.close()
    # 异常处理：取经度 71 - 139，纬度 1 - 59
    data = val[20:1181, 20:1381, 0][::-1]
    return np.mat(data)


def classify(file_path, file_name, classes, lut, start=0):
    """
    分类并保存为图片
    :param file_path:
    :param file_name
    :param classes: 分类区间
    :param lut: 颜色 RGB 元祖, len(classes)+1
    :param start
    :return:
    """
    # 读取数据
    src_arr = read_nc_data(file_path, var='APCP_surface')
    # 根据类别数目将直方图分割成5个颜色区间
    # classes = gdal_array.numpy.histogram(srcArr, bins=5)[1]
    # 创建一个RGB颜色的JPEG输出图片
    rgb = gdal_array.numpy.zeros((3, src_arr.shape[0], src_arr.shape[1]), gdal_array.numpy.float32)
    # 处理所有类并声明颜色
    for i in range(len(classes)):
        mask = gdal_array.numpy.logical_and(start <= src_arr, src_arr <= classes[i])
        for j in range(len(lut[i])):
            rgb[j] = gdal_array.numpy.choose(mask, (rgb[j], lut[i][j]))
        start = classes[i] + 0.001  # 0.001 要<=像元值精度
    # 保存图片
    output = gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8), file_name, format='JPEG')
    # 取消输出避免在某些平台上损坏文件
    output = None


def main():
    root_dir = r'F:\CODE_LIFE\PycharmProjects\weather'
    data_file_path = os.path.join(root_dir, 'weather_data')
    data_res_path = os.path.join(root_dir, 'weather_res')

    classes = np.array([0, 10, 25, 50, 100, 1000])
    lut = [[255, 255, 255], [182, 241, 169], [59, 186, 62], [93, 182, 248], [0, 1, 251], [255, 0, 253]]

    files = os.listdir(data_file_path)
    for file in files:
        if not os.path.isdir(file):
            print('processing..' + file)
            file_path = os.path.join(data_file_path, file)
            file_name = os.path.join(data_res_path, 'APCP' + '_' + file.replace('.nc', '.jpg'))
            classify(file_path=file_path, file_name=file_name, classes=classes, lut=lut)


if __name__ == '__main__':
    main()
