# -*- coding: utf-8 -*-

import os
import json
import pandas as pd
from netCDF4 import Dataset


header = {
    'parameterCategory': 2,
    'parameterCategoryName': 'Momentum',
    'parameterNumber': 2,
    'parameterNumberName': 'U-component_of_wind',
    'parameterUnit': 'm.s-1',
    'numberPoints': 4071,
    'gridUnits': 'degrees',
    'resolution': 48,
    'nx': 69,
    'ny': 59,
    'lo1': 71,
    'lo2': 139,
    'la1': 59,
    'la2': 1,
    'dx': 1,
    'dy': 1
}


def process_abnormal(df, lon, lat):
    """
    异常处理
    :return:
    """
    df = df[list(range(20, 1381, 20))]
    df = df.loc[list(range(20, 1181, 20))]
    df.index = lat[20:1181:20]
    df.columns = lon[20:1381:20]
    return df.round(1)  # 小数保留1位


def write_data_json(u_list, v_list, json_name):
    u = {
        "header": header.copy(),
        "data": u_list
    }
    v = {
        "header": header.copy(),
        "data": v_list
    }
    v["header"]["parameterNumberName"] = "V-component_of_current"
    v["header"]["parameterNumber"] = 3
    data = [u, v]
    with open(json_name, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def read_data(file):
    ds = Dataset(file, mode='r')
    # 读取经纬度
    lon = ds.variables['longitude'][:]  # 读取经度
    lat = ds.variables['latitude'][:]  # 读取纬度
    u_df = pd.DataFrame(ds.variables['UGRD_10maboveground'][:, :, 0])
    v_df = pd.DataFrame(ds.variables['VGRD_10maboveground'][:, :, 0])
    ds.close()
    # 数据处理
    u_df = process_abnormal(u_df, lon, lat)
    v_df = process_abnormal(v_df, lon, lat)
    # 将DataFrame转为list
    u_list = u_df.values.flatten().tolist()
    v_list = v_df.values.flatten().tolist()
    return u_list, v_list

def main():
    root_dir = r'F:\CODE_LIFE\PycharmProjects\weather'
    data_file_path = os.path.join(root_dir, 'weather_data')
    data_res_path = os.path.join(root_dir, 'weather_res')

    files = os.listdir(data_file_path)
    for file in files:
        if not os.path.isdir(file):
            print('processing..' + file)
            u_list, v_list = read_data(os.path.join(data_file_path, file))
            json_name = 'WIND_' + file.replace(".nc", ".json")
            # 写入数据
            write_data_json(u_list, v_list, os.path.join(data_res_path, 'WIND', json_name))


if __name__ == '__main__':
    main()












