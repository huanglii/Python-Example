# # -*- coding: utf-8 -*-
#
# import os
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# import pandas as pd
# import numpy as np
# from osgeo import gdal_array
# from netCDF4 import Dataset
#
# tif_file = r'F:\GIS_DATA\Chongqing\cq.tif'
# srcArr = gdal_array.LoadFile(tif_file)
# print(srcArr)
# print('...分割线....')
#
# nc_file = r'F:\GIS_DATA\weather\2019030600_003.nc'
# ds = Dataset(nc_file)
# data = ds.variables['TMAX_2maboveground'][:]
# # srcArr = gdal_array.OpenNumPyArray(np.array(data), binterleave=False)
# print(np.mat(data[::-1]))
# gdal_array.SaveArray(np.mat(data[::-1]), filename='tt.jpg', format='JPEG')

import numpy as np
from netCDF4 import Dataset
from osgeo import gdal
import os

class GRID:

    #读图像文件
    def read_img(self,filename):
        dataset=gdal.Open(filename)       #打开文件

        im_width = dataset.RasterXSize    #栅格矩阵的列数
        im_height = dataset.RasterYSize   #栅格矩阵的行数

        im_geotrans = dataset.GetGeoTransform()  #仿射矩阵
        im_proj = dataset.GetProjection() #地图投影信息
        im_data = dataset.ReadAsArray(0,0,im_width,im_height) #将数据写成数组，对应栅格矩阵

        del dataset
        return im_proj,im_geotrans,im_data

    #写文件，以写成tif为例
    def write_img(self,filename,im_proj,im_geotrans,im_data):
        #gdal数据类型包括
        #gdal.GDT_Byte,
        #gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
        #gdal.GDT_Float32, gdal.GDT_Float64

        #判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        #判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1,im_data.shape

        #创建文件
        driver = gdal.GetDriverByName("GTiff")            #数据类型必须有，因为要计算需要多大内存空间
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)              #写入仿射变换参数
        dataset.SetProjection(im_proj)                    #写入投影

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)  #写入数组数据
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i+1).WriteArray(im_data[i])

        del dataset

if __name__ == "__main__":
    os.chdir(r'F:\GIS_DATA\Chongqing')                        #切换路径到待处理图像所在文件夹
    run = GRID()
    # proj,geotrans,data = run.read_img('cq.tif')        #读数据
    # print(proj)
    # print(geotrans)
    # print(data)
    # print(data.shape)

    nc_file = r'F:\GIS_DATA\weather\2019030600_003.nc'
    ds = Dataset(nc_file)
    data = ds.variables['APCP_surface'][:]
    ds.close()
    d = np.mat(data[::-1])
    proj = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'
    geotrans = (69.975, 0.049999999999997186, 0.0, 60.025000000000006, 0.0, -0.0499999999999972)
    run.write_img('LC81230402013164LGN00_Rewrite.tif',proj,geotrans,d) #写数据