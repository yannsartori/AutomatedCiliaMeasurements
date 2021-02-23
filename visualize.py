import pandas as pd
import csv
import sys
from PIL import Image, ImageDraw, ImageFont

################################# TO CHANGE #################################
cell_csv_path='/Users/sneha/Desktop/mni/cilia-output/MyExpt_Cell.csv'
cilia_csv_path='/Users/sneha/Desktop/mni/cilia-output/MyExpt_Cilia.csv'
im_csv_dir_path='/Users/sneha/Desktop/mni/cilia-output/'
center_to_center_fol_path='/Users/sneha/Desktop/mni/csv_output_ex'
output_im_dir_path='/Users/sneha/Desktop/mni/'
################################# TO CHANGE #################################


def cilia_to_line(): # big func that calls everything else

    fields = ['ImageNumber', 'Location_Center_X', 'Location_Center_Y']
    cell_df = pd.read_csv(cell_csv_path, skipinitialspace=True, usecols=fields)
    num_im = cell_df.ImageNumber.iat[-1]
    grouped_cell = cell_df.groupby(['ImageNumber'])
    cilia_df = pd.read_csv(cilia_csv_path, skipinitialspace=True, usecols=fields)
    grouped_cilia = cilia_df.groupby(['ImageNumber'])

    for num in range(1, num_im+1):
        cell_list, cilia_list, associate_list = make_lists_c2c(num, grouped_cell, grouped_cilia)
        im_path=make_paths(num, '01', False)
        c2c_label(cell_list, cilia_list, associate_list, im_path, num, 3)

        
def make_paths(num, channel, label): #makes paths for us to be able to find init imgs / for images to go 
    if label:
        if channel==3:
            path = output_im_dir_path + '210115_Cortical_NPC_' + str(num) + '_LABELED_FULL.tiff'
        else:
            path = output_im_dir_path + '210115_Cortical_NPC_' + str(num) + '_ch' + channel + '_LABELED.tiff'
    
    else:
        path = im_csv_dir_path + '210115_Cortical_NPC_' + str(num) + '_ch' + channel + '.tiff'

    return path

def make_lists_c2c(im_num, grouped_cell, grouped_cilia): 
    cell_list = helper_make_lists(im_num, grouped_cell)
    cilia_list = helper_make_lists(im_num, grouped_cilia)
    associate_list = helper_c2c_make_list(im_num)
    return cell_list, cilia_list, associate_list

def helper_c2c_make_list(im_num): # finds out what our csv path is 
    csv_path = center_to_center_fol_path + '/im_' + str(im_num) + '.csv'
    fields = ['Cilia', 'Cell']
    df = pd.read_csv(csv_path, skipinitialspace=True, usecols=fields)
    new_list = df.values.tolist()
    return new_list

# cilia to cell line
# takes in two lists of coords, and cell im
def c2c_label(cell_list, cilia_list, associate_list, im, num, channel):
    img = Image.open(im)
    for i, val in enumerate(cell_list): # labels cell li pt
        x_coord = val[0]
        y_coord = val[1]
        d = ImageDraw.Draw(img)
        write_num = str(i+1)
        d.text((x_coord, y_coord), write_num, fill=(255,255,255,255))
    
    for i, val in enumerate(cilia_list): # labels cilia li pt
        x_coord = val[0]
        y_coord = val[1]
        d = ImageDraw.Draw(img)
        write_num = str(i+1)
        d.text((x_coord, y_coord), write_num, fill=(246, 71, 71, 1))
    
    for i, val in enumerate(associate_list):
        cilia_num = val[0]-1
        cell_num = val[1]-1
        if not cell_num == -2: # if cell num exists, find x and y coords of cilia and cell 
            x_cilia= cilia_list[cilia_num][0]
            y_cilia= cilia_list[cilia_num][1]
            x_cell= cell_list[cell_num][0]
            y_cell= cell_list[cell_num][1] 
            line_xy = [(x_cilia, y_cilia), (x_cell, y_cell)]
            d = ImageDraw.Draw(img)
            d.line(line_xy, fill=(255,255,255,255))

    path = make_paths(num, channel, True)
    img.save(path)

def helper_make_lists(im_num, grouped):
    im_df = grouped.get_group(im_num) 
    print(im_df)
    im_df.drop('ImageNumber', axis=1, inplace=True)
    new_list = im_df.values.tolist()
    return new_list

# makes lists
def make_lists(im_num, grouped_cell, grouped_cilia): 
    cell_list = helper_make_lists(im_num, grouped_cell)
    cilia_list = helper_make_lists(im_num, grouped_cilia)

    return cell_list, cilia_list

# labels image
def label_im(coordinate_list, im, num, channel):
    img = Image.open(im)
    for i, val in enumerate(coordinate_list):
        x_coord = val[0]
        y_coord = val[1]
        d = ImageDraw.Draw(img)
        write_num = str(i+1)
        d.text((x_coord, y_coord), write_num, fill=(255,255,255,255))
    
    path = make_paths(num, channel, True)
    img.save(path)

def batch_script(): # runs methods for all images
    fields = ['ImageNumber', 'Location_Center_X', 'Location_Center_Y']
    cell_df = pd.read_csv(cell_csv_path, skipinitialspace=True, usecols=fields)
    num_im = cell_df.ImageNumber.iat[-1]
    grouped_cell = cell_df.groupby(['ImageNumber'])
    cilia_df = pd.read_csv(cilia_csv_path, skipinitialspace=True, usecols=fields)
    grouped_cilia = cilia_df.groupby(['ImageNumber'])

    for num in range(1, num_im+1):
        cell_list, cilia_list = make_lists(num, grouped_cell, grouped_cilia)
        cell_channel = '01'
        cilia_channel = '02'
        im_path_cell=make_paths(num, '01', False)
        im_path_cilia=make_paths(num, '02', False)
        label_im(cell_list, im_path_cell, num, '01')
        label_im(cilia_list, im_path_cilia, num, '02')

def main(): 
    # batch_script()
    cilia_to_line()

if __name__ == "__main__":
    main()
            