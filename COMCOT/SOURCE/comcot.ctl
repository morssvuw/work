#################################################################
#                                                               #
#      Control file for COMCOT tsunami simulation package       #
#      - Main Configuration File (comcot.ctl)                   #
#                                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----#
#===============================================:================
# General Parameters for Simulation             : Value Field   |
#===============================================:================
# Job Description: One-line brief description may be added here  
 Total Simulated Duration (Wall clock, seconds) :10800
 Time Interval for Snapshot Output    (seconds) :15
 Zmax & Gauge Output (0-Zmax;1-Gauge,ts; 2-Both):     1       
 Start Type (0-Cold; 1-Hot) (,Ambient Sea Level):     0          
 Resuming Time for Hot Start          (Seconds) :  3600000000.00       
 Minimum Offshore Depth {,Arrival Threshold} (m):     0.0,0.05     
 INI.CON.(0:EQ,1:SD,2:WM,3:LS,4:EQ+LS,5:GM,8:FD):     0          
 Boundary Cond.(0-Open;1-Absorb;2-Wall;3-FACTS) :     1          
 Specify Filename of z Input (for BC=3, FACTS)  :23926h.asc
 Specify Filename of u Input (for BC=3, FACTS)  :23926u.asc
 Specify Filename of v Input (for BC=3, FACTS)  :23926v.asc
#
#===============================================:================
# Parameters for EQ Fault Model (Segment 01)    :Values         |
#===============================================:================
 Number of FLT Planes (use fault_multi.ctl if>1):       1        
 Rupture Start Time(,Uplift Duration)  (seconds):       0.0      
 Fault Option (0:FM-PC; 1:Data; 2:GF; 9:FM-TC)  :1
 Focal Depth                            (meters):5000
 Length of Fault Plane                  (meters):300000
 Width of Fault Plane                   (meters):100000
 Dislocation of Fault Plane             (meters):1
 Strike Angle (theta)                  (degrees):0
 Dip  Angle (delta)                    (degrees):55
 Slip/Rake Angle (lamda)               (degrees):5
 Origin of Numerical Domain: Latitude  (degrees):32.0854
 Origin of Numerical Domain: Longitude (degrees):135.0021
 Epicenter Location: Latitude          (degrees):53.3354
 Epicenter Location: Longitude         (degrees):159.3354
 File Name of Input Data                        :/vol/rcet-solar/JAPANGFDATA/Origin/OriginLft.xyz
 Data Format (0-COMCOT;1-MOST;2-XYZ;3-ASC)      :       2        
#
#===============================================:================
#  Parameters for Incident Wave Maker           :Values         |
#===============================================:================
 Wave Type  (1-Solitary; 2-given; 3-focusing)   :       1        
 File Name of Input Data (for Type=2)           :fse.dat
 Incident direction( 1:tp,2:bt,3:lf,4:rt,5:obl) :       2        
 Characteristic Wave Amplitude         (meters) :       0.500    
 Typical Water depth                   (meters) :    2000.000    
#
#===============================================:================
#  Parameters for Landslide / Ground Motion     :Values         |
#===============================================:================
 X_Start of Transient Motion Area               :     177.00     
 X_End of Transient Motion Area                 :     179.00     
 Y_Start of Transient Motion Area               :     -41.00     
 Y_End of Transient Motion Area                 :     -39.00     
 File Name of Shape Input[,format(3-XYZ;4-ASC)] : RockGarden_test.dat
 Option (0-OLD; 1-XYT; 2-LS.Solid; 3-LS.Flow)   :       2        
#
#===============================================:================
# Configurations for all grid layers, add more layers if needed  
#===============================================:================
# Parameters for 1st-level grids -- layer 01    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Grid Size       (dx, sph:minutes, Cart:meters) :4.5
 Time Step Size                       (seconds) :45
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :1
 X_start                                        :135.00209045410156
 X_end                                          :162.45208740234375
 Y_Start                                        :32.08541488647461
 Y_end                                          :54.13541793823242
 File Name of Digital Elevation Model (DEM) data:g1.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :      01        
 Grid Level                                     :1
 Parent Grid Layer's ID Number                  :-1
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 02    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :135.00209045410156
 X_end                                          :144.07708740234375
 Y_Start                                        :32.08541488647461
 Y_end                                          :39.360416412353516
 File Name of Digital Elevation Model (DEM) data:g2.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :2
 Grid Level                                     :2
 Parent Grid Layer's ID Number                  :1
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 03    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :135.00209045410156
 X_end                                          :144.07708740234375
 Y_Start                                        :39.43541717529297
 Y_end                                          :46.71041488647461
 File Name of Digital Elevation Model (DEM) data:g3.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :3
 Grid Level                                     :2
 Parent Grid Layer's ID Number                  :1
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 04    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :135.00209045410156
 X_end                                          :144.07708740234375
 Y_Start                                        :46.78541564941406
 Y_end                                          :54.06041717529297
 File Name of Digital Elevation Model (DEM) data:g4.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :4
 Grid Level                                     :2
 Parent Grid Layer's ID Number                  :1
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 05    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :144.15208435058594
 X_end                                          :153.22708129882812
 Y_Start                                        :39.43541717529297
 Y_end                                          :46.71041488647461
 File Name of Digital Elevation Model (DEM) data:g5.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :5
 Grid Level                                     :2
 Parent Grid Layer's ID Number                  :1
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 06    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :144.15208435058594
 X_end                                          :153.22708129882812
 Y_Start                                        :46.78541564941406
 Y_end                                          :54.06041717529297
 File Name of Digital Elevation Model (DEM) data:g6.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :6
 Grid Level                                     :2
 Parent Grid Layer's ID Number                  :1
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 07    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :153.3020782470703
 X_end                                          :162.37709045410156
 Y_Start                                        :46.78541564941406
 Y_end                                          :54.06041717529297
 File Name of Digital Elevation Model (DEM) data:g7.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :7
 Grid Level                                     :2
 Parent Grid Layer's ID Number                  :1
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 08    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :135.00209045410156
 X_end                                          :137.97708129882812
 Y_Start                                        :32.08541488647461
 Y_end                                          :34.485416412353516
 File Name of Digital Elevation Model (DEM) data:g8.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :8
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :2
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 09    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :135.00209045410156
 X_end                                          :137.97708129882812
 Y_Start                                        :34.51041793823242
 Y_end                                          :36.91041564941406
 File Name of Digital Elevation Model (DEM) data:g9.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :9
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :2
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 10    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :135.00209045410156
 X_end                                          :137.97708129882812
 Y_Start                                        :36.93541717529297
 Y_end                                          :39.33541488647461
 File Name of Digital Elevation Model (DEM) data:g10.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :10
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :2
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 11    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :32.08541488647461
 Y_end                                          :34.485416412353516
 File Name of Digital Elevation Model (DEM) data:g11.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :11
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :2
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 12    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :34.51041793823242
 Y_end                                          :36.91041564941406
 File Name of Digital Elevation Model (DEM) data:g12.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :12
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :2
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 13    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :36.93541717529297
 Y_end                                          :39.33541488647461
 File Name of Digital Elevation Model (DEM) data:g13.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :13
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :2
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 14    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :141.00209045410156
 X_end                                          :143.97708129882812
 Y_Start                                        :36.93541717529297
 Y_end                                          :39.33541488647461
 File Name of Digital Elevation Model (DEM) data:g14.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :14
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :2
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 15    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :39.43541717529297
 Y_end                                          :41.83541488647461
 File Name of Digital Elevation Model (DEM) data:g15.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :15
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :3
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 16    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :41.860416412353516
 Y_end                                          :44.26041793823242
 File Name of Digital Elevation Model (DEM) data:g16.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :16
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :3
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 17    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :44.28541564941406
 Y_end                                          :46.68541717529297
 File Name of Digital Elevation Model (DEM) data:g17.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :17
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :3
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 18    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :141.00209045410156
 X_end                                          :143.97708129882812
 Y_Start                                        :39.43541717529297
 Y_end                                          :41.83541488647461
 File Name of Digital Elevation Model (DEM) data:g18.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :18
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :3
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 19    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :141.00209045410156
 X_end                                          :143.97708129882812
 Y_Start                                        :41.860416412353516
 Y_end                                          :44.26041793823242
 File Name of Digital Elevation Model (DEM) data:g19.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :19
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :3
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 20    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :141.00209045410156
 X_end                                          :143.97708129882812
 Y_Start                                        :44.28541564941406
 Y_end                                          :46.68541717529297
 File Name of Digital Elevation Model (DEM) data:g20.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :20
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :3
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 21    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :46.78541564941406
 Y_end                                          :49.18541717529297
 File Name of Digital Elevation Model (DEM) data:g21.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :21
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :4
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 22    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :138.00209045410156
 X_end                                          :140.97708129882812
 Y_Start                                        :49.21041488647461
 Y_end                                          :51.610416412353516
 File Name of Digital Elevation Model (DEM) data:g22.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :22
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :4
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 23    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :141.00209045410156
 X_end                                          :143.97708129882812
 Y_Start                                        :46.78541564941406
 Y_end                                          :49.18541717529297
 File Name of Digital Elevation Model (DEM) data:g23.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :23
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :4
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 24    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :141.00209045410156
 X_end                                          :143.97708129882812
 Y_Start                                        :49.21041488647461
 Y_end                                          :51.610416412353516
 File Name of Digital Elevation Model (DEM) data:g24.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :24
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :4
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 25    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :141.00209045410156
 X_end                                          :143.97708129882812
 Y_Start                                        :51.63541793823242
 Y_end                                          :54.03541564941406
 File Name of Digital Elevation Model (DEM) data:g25.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :25
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :4
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 26    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :144.15208435058594
 X_end                                          :147.12709045410156
 Y_Start                                        :41.860416412353516
 Y_end                                          :44.26041793823242
 File Name of Digital Elevation Model (DEM) data:g26.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :26
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :5
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 27    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :144.15208435058594
 X_end                                          :147.12709045410156
 Y_Start                                        :44.28541564941406
 Y_end                                          :46.68541717529297
 File Name of Digital Elevation Model (DEM) data:g27.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :27
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :5
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 28    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :147.15208435058594
 X_end                                          :150.12709045410156
 Y_Start                                        :44.28541564941406
 Y_end                                          :46.68541717529297
 File Name of Digital Elevation Model (DEM) data:g28.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :28
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :5
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 29    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :150.15208435058594
 X_end                                          :153.12709045410156
 Y_Start                                        :44.28541564941406
 Y_end                                          :46.68541717529297
 File Name of Digital Elevation Model (DEM) data:g29.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :29
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :5
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 30    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :144.15208435058594
 X_end                                          :147.12709045410156
 Y_Start                                        :46.78541564941406
 Y_end                                          :49.18541717529297
 File Name of Digital Elevation Model (DEM) data:g30.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :30
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :6
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 31    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :144.15208435058594
 X_end                                          :147.12709045410156
 Y_Start                                        :49.21041488647461
 Y_end                                          :51.610416412353516
 File Name of Digital Elevation Model (DEM) data:g31.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :31
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :6
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 32    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :150.15208435058594
 X_end                                          :153.12709045410156
 Y_Start                                        :46.78541564941406
 Y_end                                          :49.18541717529297
 File Name of Digital Elevation Model (DEM) data:g32.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :32
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :6
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 33    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :153.3020782470703
 X_end                                          :156.27708435058594
 Y_Start                                        :46.78541564941406
 Y_end                                          :49.18541717529297
 File Name of Digital Elevation Model (DEM) data:g33.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :33
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :7
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 34    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :153.3020782470703
 X_end                                          :156.27708435058594
 Y_Start                                        :49.21041488647461
 Y_end                                          :51.610416412353516
 File Name of Digital Elevation Model (DEM) data:g34.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :34
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :7
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 35    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :153.3020782470703
 X_end                                          :156.27708435058594
 Y_Start                                        :51.63541793823242
 Y_end                                          :54.03541564941406
 File Name of Digital Elevation Model (DEM) data:g35.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :35
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :7
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 36    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :156.3020782470703
 X_end                                          :159.27708435058594
 Y_Start                                        :49.21041488647461
 Y_end                                          :51.610416412353516
 File Name of Digital Elevation Model (DEM) data:g36.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :36
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :7
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 37    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :156.3020782470703
 X_end                                          :159.27708435058594
 Y_Start                                        :51.63541793823242
 Y_end                                          :54.03541564941406
 File Name of Digital Elevation Model (DEM) data:g37.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :37
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :7
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 38    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :0
 Friction Switch (0-ON,Const.,1-OFF,2:ON,Var.n) :0
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :2
 GridSize Ratio of Parent Grid to Current Grid  :3.0
 X_start                                        :159.3020782470703
 X_end                                          :162.27708435058594
 Y_Start                                        :51.63541793823242
 Y_end                                          :54.03541564941406
 File Name of Digital Elevation Model (DEM) data:g38.xyz
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       3        
 Grid Identification Number (ID)                :38
 Grid Level                                     :3
 Parent Grid Layer's ID Number                  :7
#