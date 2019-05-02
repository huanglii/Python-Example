from osgeo import gdal, gdal_array, osr
from PIL import Image, ImageDraw
import shapefile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def hello():
    print('hello')


def array2raster(raster, raster_origin, pixel_width, pixel_height, data, wkid=4326):
    """
    数组转栅格
    :param raster: 输出栅格文件
    :param raster_origin: 左上角坐标
    :param pixel_width: 像素大小
    :param pixel_height: 像素大小
    :param data: 数据
    :param wkid: wkid 默认 4326
    :return:
    """

    cols = data.shape[1]
    rows = data.shape[0]
    origin_x = raster_origin[0]
    origin_y = raster_origin[1]

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(raster, cols, rows, 1, gdal.GDT_Float64)
    out_raster.SetGeoTransform((origin_x, pixel_width, 0, origin_y, 0, pixel_height))
    out_band = out_raster.GetRasterBand(1)
    out_band.WriteArray(data)
    out_raster_srs = osr.SpatialReference()
    out_raster_srs.ImportFromEPSG(wkid)
    out_raster.SetProjection(out_raster_srs.ExportToWkt())
    out_band.FlushCache()


def clip_raster(raster, src_raster, shape_file):
    """
    栅格裁剪
    :param raster:
    :param src_raster:
    :param shape_file:
    :return:
    """

    def image_to_array(i):
        """
        将一个Python图像库的数组转换为一个gdal_array图片
        """
        a = gdal_array.numpy.frombuffer(i.tobytes(), 'b')
        a.shape = i.im.size[1], i.im.size[0]
        return a

    def world_to_pixel(geo_matrix, x, y):
        """
        使用GDAL库的geo_matrix对象((gdal.Getgeo_transform()))计算地理坐标的像素位置
        """
        x_dist = geo_matrix[1]
        y_dist = geo_matrix[5]
        # rtnX = geo_matrix[2]
        # rtnY = geo_matrix[4]
        pixel = int((x - geo_matrix[0]) / x_dist)
        line = int((geo_matrix[3] - y) / abs(y_dist))
        return (pixel, line)

    # 将数据源作为gdal_array载入
    dataay = gdal_array.LoadFile(src_raster)
    dataay = np.array([dataay])
    # geo_transform
    src_img = gdal.Open(src_raster)
    geo_trans = src_img.GetGeoTransform()
    # geo_trans = (71.0, 0.05, 0.0, 59.0, 0.0, -0.05)
    # geo_trans = (8177442.874266411, 6221.79608963611, 0.0, 7091572.570248932, 0.0, -6221.79608963611)
    # 使用PyShp库打开shp文件
    r = shapefile.Reader(shape_file)
    # 将图层扩展转换为图片像素坐标
    min_x, min_y, max_x, max_y = r.bbox
    ul_x, ul_y = world_to_pixel(geo_trans, min_x, max_y)
    lr_x, lr_y = world_to_pixel(geo_trans, max_x, min_y)
    # 计算新图片的尺寸
    px_width = int(lr_x - ul_x)
    px_height = int(lr_y - ul_y)
    clip = dataay[:, ul_y:lr_y, ul_x:lr_x]
    # 为图片创建一个新的geo_matrix对象以便附加地理参照数据
    geo_trans = list(geo_trans)
    geo_trans[0] = min_x
    geo_trans[3] = max_y

    # 在一个空白的8字节黑白掩膜图片上把点映射为像元绘制边界线
    raster_poly = Image.new("L", (px_width, px_height), 1)
    # 使用PIL创建一个空白图片用于绘制多边形
    rasterize = ImageDraw.Draw(raster_poly)
    for shape in r.shapes():
        ps = []
        for p in shape.points:
            ps.append(world_to_pixel(geo_trans, p[0], p[1]))
        rasterize.polygon(ps, 0)

    # 使用PIL图片转换为Numpy掩膜数组
    mask = image_to_array(raster_poly)
    # 根据掩膜图层对图像进行裁剪
    clip = gdal_array.numpy.choose(mask, (clip, 0))

    raster_origin = (geo_trans[0], geo_trans[3])
    pixel_width = geo_trans[1]
    pixel_height = geo_trans[5]
    array2raster(raster, raster_origin, pixel_width, pixel_height, clip[0])


def reproject_raster(raster, src_raster, wkid):
    """
    重投影
    :param raster: 栅格
    :param wkid: wkid
    :return:
    """

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(wkid)
    old_ds = gdal.Open(src_raster)
    vrt_ds = gdal.AutoCreateWarpedVRT(old_ds, old_ds.GetProjection(), srs.ExportToWkt(), gdal.GRA_Bilinear)
    gdal.GetDriverByName('GTiff').CreateCopy(raster, vrt_ds)
    old_ds = None


def classify(file, src_raster):
    """
    分类并保存为图片
    :param file:
    :param src_raster:
    :return:
    """

    classes = np.array([0, 3, 10, 20, 50, 70, 1000])
    lut = [[255, 255, 255], [154, 250, 142], [60, 163, 10], [106, 178, 250], [8, 21, 255], [70, 251, 247],
           [111, 13, 10]]
    start = 0.0001

    # 读取数据
    data = gdal_array.LoadFile(src_raster)
    data[data == 0] = None

    # 根据类别数目将直方图分割成5个颜色区间
    # classes = gdal_array.numpy.histogram(srcArr, bins=5)[1]
    # 创建一个RGB颜色的JPEG输出图片
    rgb = gdal_array.numpy.zeros((3, data.shape[0], data.shape[1]), gdal_array.numpy.float32)
    # 处理所有类并声明颜色
    for i in range(len(classes)):
        mask = gdal_array.numpy.logical_and(start <= data, data <= classes[i])
        for j in range(len(lut[i])):
            rgb[j] = gdal_array.numpy.choose(mask, (rgb[j], lut[i][j]))
        start = classes[i] + 0.001  # 0.001 要<=像元值精度
    # 保存图片
    output = gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8), file, format='PNG')
    # 取消输出避免在某些平台上损坏文件
    output = None


def tif2png(file, src_raster):
    """
    栅格转图片
    :param src_raster_file:
    :return:
    """

    src_data = gdal.Open(src_raster)
    src_array = gdal_array.LoadFile(src_raster)
    src_array[src_array == 0] = None
    data = pd.DataFrame(src_array)
    # print(data)

    plt.figure(figsize=(1146, 841), dpi=1)
    # 去除空白
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # 去除坐标轴
    plt.xticks([]), plt.yticks([])

    # colors
    cmap = colors.LinearSegmentedColormap.from_list('tmp',
                                                    colors=['#9588d3', '#9588d3', '#9588d3', '#9588d3', '#96d0d8',
                                                            '#80cbc5', '#66b3ba', '#5e8fc5', '#4f8b3d', '#79921c',
                                                            '#aaa00e', '#deb106', '#f29606', '#ec5e14', '#be4112',
                                                            '#8a2a0a', '#8a2a0a'])
    # cmap = colors.ListedColormap(['#9588d3', '#9588d3', '#9588d3', '#9588d3', '#96d0d8', '#80cbc5', '#66b3ba', '#5e8fc5', '#4f8b3d', '#79921c', '#aaa00e', '#deb106', '#f29606', '#ec5e14', '#be4112', '#8a2a0a', '#8a2a0a'])
    plt.imshow(data, aspect='equal', vmin=-50, vmax=50, cmap=cmap)
    # plt.imshow(data)

    plt.savefig(file, format='png', transparent=True, pad_inches=0, bbox_inches=0)


