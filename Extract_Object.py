# -*- coding: utf-8 -*-
"""
Created on Sat May 19 00:14:58 2018

@author: Hao J.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

from skimage import io,filters,color
import os

import xlwt
from tempfile import TemporaryFile

def load_images(folder):
    img_list = []
    for filename in os.listdir(folder):
        img =  io.imread(os.path.join(folder, filename))
        if img is not None:
            img_list.append(img)
    
    return img_list
        
        
def extract_object_for_single_image(im, save_dir, refer_index, name_list):
    #im: rgb image
    #refer_index: integer, used to name the extracted objects

    im_grey = color.rgb2grey(im)
    edges = filters.roberts(im_grey)
    pix_row_sum =[sum(row) for row in edges]
    
    condition = 3
    index = [i for i,x in enumerate(pix_row_sum) if x < condition]
    
    if index[0] == 0:
        status = 'wait'
    else:
        status = 'Ready for cut'
        start_point = 0
    
    for i in index[1:-1]:
        if status=='Ready for cut':
            img = im[start_point:i,:,:]
            io.imsave(save_dir+'cp'+str(refer_index)+'.jpg', img)
            name_list.append('cp'+str(refer_index)+'.jpg')
            refer_index += 1
            status = 'wait'
            start_point = i
        elif pix_row_sum[i+1]>=condition:
            status = 'Ready for cut'
            start_point = i
            
    return refer_index

def save_name_list(name_list):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    
    for i,e in enumerate(name_list):
        sheet1.write(i,0,e)
    
    name = "data_labels.xls"
    book.save(name)
    book.save(TemporaryFile())


folder = 'chopstick_data/'    
save_dir = 'data/'
img_list = load_images(folder)
refer_index = 0
name_list =[]
for im in img_list:
    refer_index = extract_object_for_single_image(im, save_dir, refer_index, name_list)
    
save_name_list(name_list)   
