import os


# for complex commands, with many args, use string + `shell=True`:
cmd_str = "ccextractor ../../video_test.mp4 -stdout -out=ttxt -o output"
os.system(cmd_str)