import numpy as np

# ========================================================= #
# ===  post__process                                    === #
# ========================================================= #

def post__process():
    
    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )

    # ------------------------------------------------- #
    # --- [2] load data field                       --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    inpFile = "dat/ems_pst_total.field"
    Data    = lpf.load__pointFile( inpFile=inpFile, returnType="point" )

    # ------------------------------------------------- #
    # --- [3] store in grid                         --- #
    # ------------------------------------------------- #
    import nkBasicAlgs.store__inGrid3D as sig
    Data = sig.store__inGrid3D( Data=Data, x1MinMaxNum=const["channel.x1MinMaxNum"], \
                                x2MinMaxNum=const["channel.x2MinMaxNum"], \
                                x3MinMaxNum=const["channel.x3MinMaxNum"] )
    
    # ------------------------------------------------- #
    # --- [4] boundary condition                    --- #
    # ------------------------------------------------- #
    if ( const["channel.reflect_z"] ):
        import nkBasicAlgs.reflect__boundary as ref
        Data = ref.reflect__boundary( Data=Data, boundary="z", parity="even" )

    # ------------------------------------------------- #
    # --- [5] y-shift                               --- #
    # ------------------------------------------------- #
    Data[:,:,:,y_] = Data[:,:,:,y_] + const["bfield.yoffset"]
    
    # ------------------------------------------------- #
    # --- [6] save file                             --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/ems_port.field"
    spf.save__pointFile( outFile=outFile, Data=Data )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    post__process()
