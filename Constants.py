#global variables
logger = False
verbouseLogger = False
valid_tags = {'INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'}

perform_check_unique_ids = True              #US22
perform_detect_duplicate_infividuals = True  #US23
perform_detect_duplicate_families=True       #US24
perform_detect_duplicate_children = True     #US25

perform_list_living_married_people = False   #US29
perform_list_deceased_individuals = False    #US30
perform_list_living_single_people = False    #US31
perform_list_multiple_births = False         #US32
perform_list_orphans = False                 #US33
perform_list_large_age_differences = False   #US34

MAX_FAMILIES = 1000
MAX_INDIVIDUALS = 1000
gedcom_file_path = "IgorBichFakeFamily.ged"