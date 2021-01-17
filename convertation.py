import os
from PIL import Image
from PIL import ImageColor 

def remove_transparency(im, bg_colour=(255, 255, 255)):

    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im

def change_size(is_monochrome,  filepath,  filename,  dest_filename,  size):
    im = Image.new('RGB',  size,  color = ImageColor.getcolor('white','RGB'))
    original_file = Image.open(filepath + '/' + filename) # open colour image
    if is_monochrome: 
        original_file = original_file.convert('LA') # convert image to black and white
    else: 
    	original_file = remove_transparency(original_file)
    original_file.thumbnail(size)
    ofset_x = int((im.size[0] - original_file.size[0]) / 2)
    ofset_y = int((im.size[1] - original_file.size[1]) / 2)
    print((ofset_x,  ofset_y))
    im.paste(original_file,  (ofset_x,  ofset_y))
    im.save(dest_filename + '/' + filename)

def main(hight, width):
    #Defining future pictures` resolution 
    size = hight, width

    #reading all the files from source filepath and making changes on examples (expect)
    inp_path_a =  "./trainA_full"
    dest_path_a = "./trainA"
    train_arr_a = os.listdir(path= inp_path_a) 
    for filename_a in train_arr_a:
        change_size(False, inp_path_a,  filename_a,  dest_path_a,  size)
    
    #reading all the files from source filepath and making changes on examples (original)
    inp_path_b =  "./trainB_full"
    dest_path_b = "./trainB"
    train_arr_b = os.listdir(path= inp_path_b) 
    for filename_b in train_arr_b:
        change_size(True, inp_path_b,  filename_b,  dest_path_b,  size)

if __name__ == '__main__':
     if len (sys.argv) < 3:
        print ("Ошибка. Слишком мало параметров.")
        sys.exit (1)

    if len (sys.argv) > 3:
        print ("Ошибка. Слишком много параметров.")
        sys.exit (1)
        
    hight = sys.argv[1]
    width = sys.argv[2]
    
    main(hight, width)
