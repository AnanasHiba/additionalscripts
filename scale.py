import os
from PIL import Image
from PIL import ImageColor 
import time
import subprocess
import psutil

def get_gpu_temperature():
    process = subprocess.Popen(['nvidia-smi', '-q', '-d', 'temperature'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    p = str(stdout).replace("\\n", "\n").replace(" ","").replace("C",  "").split("\n")
    for l in p:
        if l.find("GPUurrentTemp:") != -1:
            return int(l.replace("GPUurrentTemp:", ""))

def check_temperature():
    gpu_temp = get_gpu_temperature()
    cpu_temp = psutil.sensors_temperatures().get('k10temp')[0].current
    print("GPU: " + str(gpu_temp) + "`C")
    print("CPU: " + str(cpu_temp) + "`C")
    while gpu_temp > 70 or cpu_temp > 70:
        time.sleep(60.1)
        gpu_temp = get_gpu_temperature()
        cpu_temp = psutil.sensors_temperatures().get('k10temp')[0].current
        print("GPU: " + str(gpu_temp) + "`C")
        print("CPU: " + str(cpu_temp) + "`C")
        
        
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

def change_size(filepath,  filename,  dest_filename):
    original_file = Image.open(filepath + '/' + filename)
    width, height = original_file.size 
    
    max_side = max(height, width)
    
    resol = max_side
    while resol < 2048:
    	resol *= 2
    
    scale = resol / max_side
    size2 = 2048 / scale
       
    original_file = remove_transparency(original_file)
    original_file.thumbnail((size2, size2))
    original_file.save(dest_filename + '/' + filename)
    
    check_temperature()
    
    if scale > 1:
    	os.system("python test.py -i '" + dest_filename + str(i) + '/' + filename + "' --checkpoint 'data/checkpoints/proSRGAN_x8.pth' --scale " + scale + " -o outputs")	
    	
def main():

    #reading all the files from source filepath and making changes on examples (expect)
    inp_path_a =  "./NEW"
    dest_path_a = "./resScale"
    train_arr_a = os.listdir(path= inp_path_a) 
    for filename_a in train_arr_a:
        change_size(inp_path_a,  filename_a,  dest_path_a)
    

if __name__ == '__main__':
    args = parse_args()
    main()
