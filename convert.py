#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：arcpy 
@File    ：convert.py
@IDE     ：PyCharm 
@Author  ：Rpower
@Date    ：2025/5/1 16:01 
"""
import os
import arcpy
from arcpy.sa import *
import csv
import re

def process_nc(path,extent_path):
    try:
        if not os.path.exists(path):
            print("请查看目录是否存在")
            return None
        else:
            file_name = os.path.basename(path)
            date = file_name[-7:-3]
            tiff_file = os.path.dirname(path)+"\\tiff"
            arcpy.MakeNetCDFRasterLayer_md(path, "etp",
                                           "lon", "lat", "etp_layer_{}".format(date))   #根据数据修改variable和output raster layer
            if not os.path.exists(tiff_file):
                os.mkdir(tiff_file)
            # 按时间维度（1到12月）处理
            for i in range(1, 13):
                try:
                    file_db = arcpy.SelectByDimension_md("etp_layer_%s" % date, [["time", "%d" % i]], "BY_VALUE")
                    tiff_output = os.path.join(tiff_file, "etp_%s_month_%02d.tif" % (date, i))
                    if not os.path.exists(tiff_output):
                        arcpy.CopyRaster_management(
                            in_raster=file_db,
                            out_rasterdataset=tiff_output,
                            config_keyword="",
                            background_value="",
                            nodata_value="",
                            pixel_type="16_BIT_SIGNED",  # 修正为16位有符号整数
                            scale_pixel_value="",
                            RGB_to_Colormap="NONE",
                            format="TIFF"
                        )
                    sr = arcpy.SpatialReference(4326)
                    arcpy.DefineProjection_management(tiff_output, sr)
                    print "成功导出并投影TIFF: %s" % tiff_output

                    # 直接调用clip和statistics
                    clip_output = clip(extent_path, path, tiff_output, i, date)
                    if clip_output:
                        statistics(os.path.dirname(path), extent_path, clip_output, i, date)

                except Exception, e:
                    print "处理月份 %d 时出错: %s" % (i, str(e))
    except Exception as e:
        print("格式错误：{}".format(e))


def clip(extent_path,path,tiff_output,i,date):
    try:
        # env.workspace = r"D:\Arcmap\Default.gdb"
        clip_path = os.path.dirname(path)+"\\clip"
        if not os.path.exists(clip_path):
            os.mkdir(clip_path)
        clip_output = os.path.join(clip_path,"etp_%s_month_%02d_clip.tif"% (date,i))
        # arcpy.Clip_management(in_raster=tiff_output, rectangle="112.695451 28.972055 113.154344 29.517363",
        #                       out_raster=clip_output, in_template_dataset=extent_path, nodata_value="-32768", clipping_geometry="ClippingGeometry",
        #                       )  # rectangle nodata_value请去arcmap将文件导入查看其值，然后修改
        if not os.path.exists(clip_output):
            outExtractByMask = ExtractByMask(tiff_output, extent_path)
            outExtractByMask.save(clip_output)

        print "已裁剪成%s"% clip_output
        return clip_output

    except Exception as e:
        print("裁剪错误{}".format(e))

def statistics(subdir,extent_path,clip_output,i,date):
    try:
        data_dir = subdir + r"\data"
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        src = os.path.join(data_dir,"etp_%s%02d.dbf"% (date,i))
        if not os.path.exists(src):
            outZSaT = ZonalStatisticsAsTable(extent_path, "OBJECTID", clip_output,
                                          src, "NODATA", "ALL")     # zone field 需要看你的shp
        # 定义输出CSV路径（以年份命名）
        csv_path = os.path.join(data_dir, "etp_%s_stats.csv" % date)

        # 读取DBF字段
        fields = [f.name for f in arcpy.ListFields(src) if f.name != "OID"]
        fields.insert(0, "Month")  # 添加月份列

        # 检查CSV是否已存在，决定是否写入表头
        write_header = not os.path.exists(csv_path)

        # 读取DBF数据并写入CSV
        with open(csv_path, 'a') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            if write_header:
                writer.writerow(fields)  # 写入表头
            with arcpy.da.SearchCursor(src, fields[1:]) as cursor:
                for row in cursor:
                    writer.writerow([i] + list(row))  # 写入月份和统计数据

        print "已将统计数据写入CSV: %s" % csv_path
    except Exception as e:
        print ("统计失败！{}".format(e))

def main():
    extent_path = r"EastDongTingLake\EastDongTingLake.shp"
    root_path = r"D:\Evaporation"
    for root, _, files in os.walk(root_path,topdown=True):
        for name in files:
            if re.match(r'.*\.nc$',name,re.I):
                path = os.path.join(root,name)
                process_nc(path,extent_path)

if __name__ =="__main__":
    main()