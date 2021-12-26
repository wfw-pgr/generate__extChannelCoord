import numpy as np

# ========================================================= #
# ===  make__ems_input.py                               === #
# ========================================================= #

def make__ems_input():

    # ------------------------------------------------- #
    # --- [1] extraction Channel coordinates        --- #
    # ------------------------------------------------- #
    import generate__extChannelCoord as gec
    gec.generate__extChannelCoord()
    gec.display__extChannelCoord()
    
    # ------------------------------------------------- #
    # --- [2] load parameter                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )
    
    # ------------------------------------------------- #
    # --- [3]  load coordinates                     --- #
    # ------------------------------------------------- #
    import nkEMSRoutines.parallelize__emsInput as pei
    ptsFile = "dat/coordinates_in_extchannel.dat"
    refFile = "dat/ems_ref.inp"
    pei.parallelize__emsInput( nParallel=const["channel.nParallel"], \
                               ptsFile=ptsFile, refFile=refFile )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    make__ems_input()
