#global variables
logger = False
verbouseLogger = False
valid_tags = {'INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'}

perform_check_unique_ids = False              #US22
perform_detect_duplicate_infividuals = False  #US23
perform_detect_duplicate_families= False      #US24
perform_detect_duplicate_children = False     #US25

perform_list_living_married_people = False   #US29
perform_list_deceased_individuals = False    #US30
perform_list_living_single_people = False    #US31
perform_list_multiple_births = False         #US32
perform_list_orphans = False                 #US33
perform_list_large_age_differences = False   #US34

perform_Corresponding_entries = False
perform_include_individual_ages = False
perform_order_siblings_by_age = False
perform_list_large_age_differences = False

MAX_FAMILIES = 1000
MAX_INDIVIDUALS = 1000
gedcom_file_path = "IgorBichFakeFamily.ged"