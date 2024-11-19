#################################################################
#                                                               #
#      Control file for COMCOT tsunami simulation package       #
#      - Configuration for Landslide Modelling (beta)           #
#                                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----#
#===============================================:================
# Parameters for Landslides: [s] - Solid type; [f] - Flow type   
#===============================================:================
# Description: This is a template,change para values if necessary
#===============================================:================
# Parameters for Landslide Modelling            :Values         |
#===============================================:================
 Shape (0:Ellip;1:Ellip_s;2:Gauss;3-Input), [sf]:      0         
 Start Time of Slide Motion      (seconds), [sf]:      0.0       
 X Coord of Start Position (Center of Mass),[sf]:    178.50      
 Y Coord of Start Position (Center of Mass),[sf]:    -40.50      
 X Coord of Stop Position  (Center of Mass),[s-]:    178.00      
 Y Coord of Stop Position  (Center of Mass),[s-]:    -40.00      
 Typical Slope Angle              (degrees),[s-]:      4.0       
 Drag Coefficient (Cd)                     ,[s-]:      1.0       
 Added mass coefficient (Cm)               ,[s-]:      1.0       
 Basal Friction (Coef.=Cn,[s];or Angle=deg),[-f]:      0.0       
 Specific Density (Rho_mass/Rho_water)     ,[sf]:      1.85      
 Length of Sliding Profile  (m along Path) ,[sf]:  10000.0       
 Width of Sliding Profile   (m across Path),[sf]:  10000.0       
 Thickness  (m in Surface-normal direction),[sf]:    200.0       
 Where to decelerate (frac. of total dist.),[s-]:      0.80      
 Scaling Factor for Length (along the path),[s-]:      1.0       
 Scaling Factor for Width (across the path),[s-]:      1.0       
 Earth Pressure Coefficient (Kactpass)     ,[-f]:      1.0       
 Constant Retarding Stress            (kpa),[-f]:     55.0       
