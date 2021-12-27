import numpy                          as np
import nkVTKRoutines.vtkDataConverter as vdc

# ------------------------------------------------- #
# --- [1] settings                              --- #
# ------------------------------------------------- #

inpFile  = "dat/ems_port.field"
outFile  = "dat/ems_port.vts"
skiprows = 3

# ------------------------------------------------- #
# --- [2] Data Loading                          --- #
# ------------------------------------------------- #

with open( inpFile, "r" ) as f:
    Data = np.loadtxt( inpFile, skiprows=skiprows )
nCmp  = Data.shape[1]
print()
print( "[convert__vtsFile] skiprows    == {0} ".format( skiprows      ) )
print( "[convert__vtsFile] Data Length == {0} ".format( Data.shape[0] ) )
print()

# ------------------------------------------------- #
# --- [3] Data Order Check                      --- #
# ------------------------------------------------- #
if   ( ( ( Data[1,0] - Data[0,0] ) == 0.0 ) & \
       ( ( Data[1,1] - Data[0,1] ) == 0.0 ) & \
       ( ( Data[1,2] - Data[0,2] ) != 0.0 ) ):
    DataOrder = "kji"
elif ( ( ( Data[1,0] - Data[0,0] ) != 0.0 ) & \
       ( ( Data[1,1] - Data[0,1] ) == 0.0 ) & \
       ( ( Data[1,2] - Data[0,2] ) == 0.0 ) ):
    DataOrder = "ijk"    
else:
    print( "[vtsDataConvertor.py] DataOrder == ??? " )
    sys.exit()
print( "[vtsDataConverter.py] DataOrder == {0}".format( DataOrder ) )

# ------------------------------------------------- #
# --- [4] Data shape                            --- #
# ------------------------------------------------- #

LI    = len( set( Data[:,0] ) )
LJ    = len( set( Data[:,1] ) )
LK    = len( set( Data[:,2] ) )

print()
print( " (LI,LJ,LK) = ({0},{1},{2})".format( LI, LJ, LK ) )
print()

if   ( DataOrder=="ijk" ):
    shape  = ( LK, LJ, LI, nCmp )
    Data  = np.reshape( Data, shape )
elif ( DataOrder=="kji" ):
    shape_ = ( LI, LJ, LK )
    shape  = ( LK, LJ, LI, nCmp )
    Data_  = np.zeros( shape )
    for ik in range( nCmp ):
        Data_[:,:,:,ik] = np.copy( np.transpose( np.reshape( Data[:,ik], shape_ ) ) )
    Data   = np.copy( Data_ )

vdc.vtkDataConverter( Data=Data, vtkFile=outFile, tag="data", DataFormat="binary" )
