import numpy as np

# ========================================================= #
# ===  restrict__rMax.py                                === #
# ========================================================= #

def restrict__rMax():

    x_, y_, z_ = 0, 1, 2
    vx_,vy_,vz_= 3, 4, 5
    
    # ------------------------------------------------- #
    # --- [1] load bfield                           --- #
    # ------------------------------------------------- #
    inpFile = "dat/ems_total_intrp.field"
    with open( inpFile, "r" ) as f:
        Data = np.loadtxt( f, skiprows=2 )

    # ------------------------------------------------- #
    # --- [2] calculate radius                      --- #
    # ------------------------------------------------- #
    radii                 = np.sqrt( Data[:,x_]**2 + ( Data[:,y_]-const["bfield.yoffset"] )**2 )
    index                 = np.where( radii >= const["main.rMax"] )
    print( "[restrict__rMax.py] #.of zero element :: {0} ".format( len( index[0] ) ) )
    Data[index,vx_:vz_+1] = 0.0

    # ------------------------------------------------- #
    # --- [3] save again                            --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/ems_total_limit.field"
    spf.save__pointFile( outFile=outFile, Data=Data )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    restrict__rMax()
