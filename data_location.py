"""Provides the file paths for the data that is pertainant for this program.
   The file paths must be changed to reference the data on the user's computer.

Variables
---------
    WORKSPACE: general file path to majority of CWI Data
    
    allwells: Describes parameters of a well, such as location in (UTM coordinates),
    general strata (aquifer), well construction materials/ parameters of
    the wells (casing diameter/ open hole interval)
    
    CWIPL: Describes the parameters of specific capacity tests perfromed on
    wells across Minnesota. Useful information includes water levels (static and post pumping),
    pumping rate, duration of the test and identification number.
    
    loc = Pumping Test spreadsheet provided by Justin Blum from the
    Minnesota Department of Health. The spreadsheet includes storativity
    values for various aquifers.
    
    THICKNESS = Attribute Table provided by Richard Soule from the
    Minnesota Department of Health. This table estimates aquifer thickness and
    saturated/unsaturated elevations in the given aquifer.

By: Jonny Full
Version: 6/26/2020
-------------------------------------------------------------------------------
"""
WORKSPACE=r"C:\Users\JonnyA\Desktop\Research\Test\water_well_information.gdb"    
allwells = WORKSPACE + r'\allwells'
CWIPL = WORKSPACE + r'\C5PL'
loc = r"C:\Users\JonnyA\Desktop\Research\Current Work\PumpingTestData.xlsx"
THICKNESS = r'C:\Users\JonnyA\Desktop\Research\Test\CWI_hydro.dbf'

         