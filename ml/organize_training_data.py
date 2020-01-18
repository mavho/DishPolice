import os 
import re
import shutil
#Data clean up on the found face dataset

directory = "training_images/original images"
name_pattern = r"\w{4}"


for filename in os.listdir(directory):
    name = re.match(name_pattern, filename).group()
    pictures_path = f"{directory}/{filename}"
    target_path = f"training_images/{name}"
    if name not in os.listdir("training_images"):
        os.mkdir(target_path)
        
    move_string = f"{target_path}/{filename}"
    
    shutil.move(f"{pictures_path}", f"{move_string}")
