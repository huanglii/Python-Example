# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pandas as pd
from netCDF4 import Dataset

root_dir = r'F:\\CODE_LIFE\\PycharmProjects\\weather'
var_dic = {
    'TMP': 'TMP_2maboveground',
    'APCP': 'APCP_surface'
}

def deal_data(data, data_type):
    """
    数据处理，取经度 71 - 139，纬度 1 - 59
    :param data:
    :param data_type:
    :return:
    """
    d = data[20:1181, 20:1381, 0][::-1]
    df = pd.DataFrame(d)
    if data_type == 'TMP':
        df = df.apply(lambda x: x - 273.15)  # 转成摄氏度
    # df.index = lat[20:1181]
    # df.columns = lon[20:1381]
    # print(df)
    return df


def plot_png(data, data_type, filename):
    """
    绘图
    :param data:
    :param data_type:
    :param filename:
    :return:
    """
    plt.figure(figsize=(700, 600), dpi=1)
    # 去除空白
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # 去除坐标轴
    plt.xticks([]), plt.yticks([])

    # colors
    if data_type == 'TMP':
        cmap = colors.LinearSegmentedColormap.from_list('tmp', colors=['#9588d3', '#9588d3', '#9588d3', '#9588d3', '#96d0d8', '#80cbc5', '#66b3ba', '#5e8fc5', '#4f8b3d', '#79921c', '#aaa00e', '#deb106', '#f29606', '#ec5e14', '#be4112', '#8a2a0a', '#8a2a0a'])
        # cmap = colors.ListedColormap(['#9588d3', '#9588d3', '#9588d3', '#9588d3', '#96d0d8', '#80cbc5', '#66b3ba', '#5e8fc5', '#4f8b3d', '#79921c', '#aaa00e', '#deb106', '#f29606', '#ec5e14', '#be4112', '#8a2a0a', '#8a2a0a'])
        plt.imshow(data, aspect='equal', vmin=-50, vmax=50, cmap=cmap)

    elif data_type == 'APCP':
        cmap = colors.LinearSegmentedColormap.from_list('apcp', colors=[(0,0,0,0), '#5f587c', '#5f587c', '#5f587c', '#5f587c', '#585c8a', '#35748e', '#2b798c', '#1f8088', '#0c8b82', '#529965', '#fa9dbe', '#f8a1c0', '#f8a1c0'])
        # cmap = colors.ListedColormap(['#5f587c', '#5f587c', '#5f587c', '#5f587c', '#585c8a', '#35748e', '#2b798c', '#1f8088', '#0c8b82', '#529965', '#fa9dbe', '#f8a1c0', '#f8a1c0'])
        plt.imshow(data, aspect='equal', cmap=cmap)

    plt.savefig(filename, format='JPEG', transparent=True, pad_inches=0, bbox_inches=0)
    # plt.show()


def read_data(nc_file, var):
    """
    读取 nc 数据
    :param nc_file:
    :param var:
    :return:
    """
    ds = Dataset(nc_file, mode='r')
    data = ds.variables[var][:]  # 读取数据
    ds.close()
    return data


def processing(file_path, res_path, data_type):
    files = os.listdir(file_path)
    for file in files:
        if not os.path.isdir(file):
            print('processing..' + file)
            data = read_data(os.path.join(file_path, file), var_dic[data_type])
            plt_data = deal_data(data, data_type)

            file_name = data_type + '_' + file.replace('.nc', '.jpg')
            plot_png(plt_data, data_type, os.path.join(res_path, 'jpg', file_name))


def main():
    data_type = 'TMP'
    data_file_path = os.path.join(root_dir, 'weather_data')
    data_res_path = os.path.join(root_dir, 'weather_res', data_type)

    processing(data_file_path, data_res_path, data_type)


if __name__ == '__main__':
    main()
