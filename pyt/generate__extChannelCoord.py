import numpy as np

# ========================================================= #
# ===  generate__extChannelCoord.py                     === #
# ========================================================= #

def generate__extChannelCoord( cnsFile="dat/parameter.conf" ):

    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    const   = lcn.load__constants( inpFile=cnsFile )
    
    # ------------------------------------------------- #
    # --- [2] generate coordinate grid              --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ const["channel.x1MinMaxNum"][0], const["channel.x1MinMaxNum"][1], \
                    int( const["channel.x1MinMaxNum"][2] ) ]
    x2MinMaxNum = [ const["channel.x2MinMaxNum"][0], const["channel.x2MinMaxNum"][1], \
                    int( const["channel.x2MinMaxNum"][2] ) ]
    x3MinMaxNum = [ const["channel.x3MinMaxNum"][0], const["channel.x3MinMaxNum"][1], \
                    int( const["channel.x3MinMaxNum"][2] ) ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    
    # ------------------------------------------------- #
    # --- [3] coordinate point selection            --- #
    # ------------------------------------------------- #
    acoef  = np.tan( const["channel.angle"] * np.pi / 180.0 )
    y0     = const["channel.yoffset"]
    hwy    = const["channel.width"] * 0.50
    lbound = acoef * coord[:,x_] + y0 - hwy
    ubound = acoef * coord[:,x_] + y0 + hwy
    radii  = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 )
    index  = np.where( ( coord[:,y_] >= lbound ) & ( coord[:,y_] <= ubound ) & \
                       ( radii > const["channel.rMin"] ) & ( radii <= const["channel.rMax"] ) )
    coord  = coord[index]

    # ------------------------------------------------- #
    # --- [4] save coordinate                       --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/coordinates_in_extchannel.dat"
    spf.save__pointFile( outFile=outFile, Data=coord )


# ========================================================= #
# ===  display__extChannelCoord                         === #
# ========================================================= #

def display__extChannelCoord():

    x_,y_                    = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )
    
    # ------------------------------------------------- #
    # --- [2] load coordinate                       --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    inpFile = "dat/coordinates_in_extchannel.dat"
    coord   = lpf.load__pointFile( inpFile=inpFile, returnType="point" )

    # ------------------------------------------------- #
    # --- [3] calculate circle min / max            --- #
    # ------------------------------------------------- #
    nth         = 101
    theta       = np.linspace( 0.0, 2.0*np.pi, nth )
    unit_circle = np.concatenate( [ np.cos(theta)[:,None], np.sin(theta)[:,None], \
                                    np.zeros( (nth,1) )], axis=1 )
    circle_rMin = const["channel.rMin"] * unit_circle
    circle_rMax = const["channel.rMax"] * unit_circle

    bb_x_maxmin = np.array( [const["channel.x1MinMaxNum"][0],const["channel.x1MinMaxNum"][1]] )
    bb_y_maxmin = np.array( [const["channel.x2MinMaxNum"][0],const["channel.x2MinMaxNum"][1]] )
    bb_x        = bb_x_maxmin[ [0,1,1,0,0] ]
    bb_y        = bb_y_maxmin[ [0,0,1,1,0] ]
    bb          = np.concatenate( [bb_x[:,None],bb_y[:,None]], axis=1 )
    
    # ------------------------------------------------- #
    # --- [4] display as points                     --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    pngFile                  = "png/coordinate_in_extchannel.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = bb_x_maxmin + np.array( [-0.1,+0.1] )
    config["plt_yRange"]     = bb_y_maxmin + np.array( [-0.1,+0.1] )

    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=coord[:,x_], yAxis=coord[:,y_], linestyle="none", marker="."  )
    fig.add__plot( xAxis=circle_rMin[:,x_], yAxis=circle_rMin[:,y_], \
                   linestyle="--", color="red"    )
    fig.add__plot( xAxis=circle_rMax[:,x_], yAxis=circle_rMax[:,y_], \
                   linestyle="--", color="green"  )
    fig.add__plot( xAxis=bb[:,x_], yAxis=bb[:,y_], linestyle="--", color="blue"  )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    generate__extChannelCoord()
    display__extChannelCoord()
