#global variables
logger = False
verbouseLogger = False
valid_tags = {'INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'}


perform_list_living_married_people = True   #US29
perform_list_deceased_individuals = True    #US30
perform_list_living_single_people = True    #US31
perform_list_multiple_births = True         #US32
perform_list_orphans = True                 #US33
perform_list_large_age_differences = True   #US34

MAX_FAMILIES = 1000
MAX_INDIVIDUALS = 1000
gedcom_file_path = "IgorBichFakeFamily.ged"