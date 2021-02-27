from PIL import Image
import os, sys

def main():

    base_path = os.getcwd()
    file_output = ''
    path_output = ''

    #Image file extensions to be included
    ext_list = ['.png', '.jpg']

    for folder, sub, files in os.walk(base_path):
        
        for f in files:

            # check of file extension is in list specified above...
            if os.path.splitext(f)[1].lower() in ext_list:
                f_path = os.path.join(folder, f)
                width, height = Image.open(f_path).size
                
                if(width > 128 and '\\backgrounds\\' not in f_path):
                    file_output += f_path + ' ' + str(width) + ' ' + str(height) + '\n'
                    path_output += f_path + '\n'


    output_file = open('imageDimensions.txt', 'w')
    output_file.write(file_output)
    output_file.write('\n')
    output_file.write(path_output)
    output_file.close()

if __name__ == '__main__':
    main()