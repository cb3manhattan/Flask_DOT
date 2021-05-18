"""
This script iterates through the uploads folder and deletes session upload folders that are
x minutes or x hours old. The script can be set to run daily on pythonanywhere.
"""

import os
import datetime
import shutil

cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'uploads')
now = datetime.datetime.now()

#Iterate through upload folder and get last modified elapsed time for each subfolder.
def clearuploads():
    for folder in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, folder)
        st = os.stat(path)
        mtime = st.st_mtime
        mdatetimes = datetime.datetime.fromtimestamp(mtime)
        print('folder: ' + folder + ' was last modified: ' + "mdatetime = {}".format(datetime.datetime.fromtimestamp(mtime)))
        delta = now - mdatetimes
        print('...This folder is ' + str(delta.seconds) + ' seconds old.')
        del_path = os.path.join(UPLOAD_FOLDER, folder)
        if delta.seconds > 3600:
            shutil.rmtree(del_path)

if __name__ == "__main__":
    clearuploads()


