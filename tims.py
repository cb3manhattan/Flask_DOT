"""
This script parses and processes TIMS data
- Create Crash Mode Column
- Create Victim Info Columns
- Recode coded columns to actual values using dictionary lookup
"""

import geopandas as gpd


Projection = '2227'

# Set UPLOAD_FOLDER
cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'uploads')

# Set input and output file names and locations

TIMS_Folder = os.path.join(UPLOAD_FOLDER, session['usertime'])
TIMS_Output = os.path.join(TIMS_Folder, 'outputs', 'collisions_mapped.shp')
Hex_Grid_Output = os.path.join(TIMS_Folder, 'outputs', 'hex_grid.shp')
BUILD_Crashes_output = os.path.join(TIMS_Folder, 'outputs', 'build_crashes.shp')


# Iterate through TIMS data folder and create a list of filepaths.
# This will be used to read all csvs into pandas dataframes
tims_list = os.listdir(TIMS_Folder)
tims_fp = [TIMS_Folder + '/' + file for file in tims_list]

# Set datatypes for columns where the type is important
dtypes = {
    'LONGITUDE' : float,
    'LATITUDE' : float,
    'POINT_X' : float,
    'POINT_Y': float
    }

# Read Collision CSVs
collisions = "Collision"
collisions_df_list = [pd.read_csv(file, dtype=dtypes) for file in tims_fp if collisions in file]

