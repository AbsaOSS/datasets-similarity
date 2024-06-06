## amazon

#### product_id: 
	 Type = ALPHANUMERIC
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### product_name: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### category: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### discounted_price: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### actual_price: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### discount_percentage: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### rating: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=2.0, max_value=5.0, range_size=3.0, same_value_length=True)
#### rating_count: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=2.0, max_value=992.0, range_size=990.0, same_value_length=False)
#### about_product: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### user_id: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### user_name: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### review_id: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### review_title: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### review_content: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### img_link: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### product_link: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=https://www.amazon.in/Crompton-convector-adjustable-Thermostats-Standard/dp/B09CGLY5CX/ref=sr_1_120_mod_primary_new?qid=1672923596&s=kitchen&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-120, shortest=https://www.amazon.in/Nokia-150-Cyan/dp/B08H21B6V7/ref=sr_1_301?qid=1672895835&s=electronics&sr=1-301, null_values=False, ratio_max_length=0.12832764505119454)
## edge_cases

#### id_column: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=10, shortest=1, null_values=False, ratio_max_length=0.2)
	 NumericalMetadata(min_value=1, max_value=10, range_size=9, same_value_length=False)
#### id_text_column: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=A, shortest=A, null_values=False, ratio_max_length=0.1)
#### id_column_both: 
	 Type = ALPHANUMERIC
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=AB1, shortest=AB1, null_values=False, ratio_max_length=0.3)
#### number_int: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=1, max_value=8, range_size=7, same_value_length=True)
#### number_int_str: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=1, max_value=8, range_size=7, same_value_length=True)
#### number_float: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=1.2, max_value=4.5, range_size=3.3, same_value_length=True)
#### number_float_str: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=1.2, max_value=1.4, range_size=0.19999999999999996, same_value_length=False)
#### float_but_int: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=1.0, max_value=8.0, range_size=7.0, same_value_length=True)
#### bool_int: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=(2, 3), distribution=(2, 3), longest=None, shortest=None, null_values=False, ratio_max_length=None)
	 NumericalMetadata(min_value=2, max_value=3, range_size=1, same_value_length=True)
#### bool_str: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=('WOMAN', 'MAN'), distribution=(2, 3), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### bool_TF: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=(True, False), distribution=(3, 7), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### bool_TFtf: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=(True, False), distribution=(1, 1), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### constant_number: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CONSTANT
	 KindMetadata(value=(1,), distribution=None, longest=None, shortest=None, null_values=False, ratio_max_length=None)
	 NumericalMetadata(min_value=1, max_value=1, range_size=0, same_value_length=True)
#### constant_str: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.CONSTANT
	 KindMetadata(value=('MA',), distribution=None, longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### float_str_comma: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=2.1, max_value=2.9, range_size=0.7999999999999998, same_value_length=True)
## exams

#### gender: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=('male', 'female'), distribution=(483, 517), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### race/ethnicity: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### parental level of education: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### lunch: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=('standard', 'free/reduced'), distribution=(87, 163), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### test preparation course: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=('none', 'completed'), distribution=(67, 133), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### math score: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=13, max_value=100, range_size=87, same_value_length=False)
#### reading score: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=27, max_value=100, range_size=73, same_value_length=False)
#### writing score: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=23, max_value=100, range_size=77, same_value_length=False)
## games

#### Unnamed: 0: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=1000, shortest=0, null_values=False, ratio_max_length=0.0026455026455026454)
	 NumericalMetadata(min_value=0, max_value=1511, range_size=1511, same_value_length=False)
#### Title: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Release Date: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Team: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Rating: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.7, max_value=4.8, range_size=4.1, same_value_length=True)
#### Times Listed: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.0, max_value=995.0, range_size=995.0, same_value_length=False)
#### Number of Reviews: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.0, max_value=995.0, range_size=995.0, same_value_length=False)
#### Genres: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Summary: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Reviews: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Plays: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.0, max_value=992.0, range_size=992.0, same_value_length=False)
#### Playing: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.0, max_value=999.0, range_size=999.0, same_value_length=False)
#### Backlogs: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=1.0, max_value=999.0, range_size=998.0, same_value_length=False)
#### Wishlist: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=2.0, max_value=995.0, range_size=993.0, same_value_length=False)
## mathScore

#### Student: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=100, shortest=1, null_values=False, ratio_max_length=0.013824884792626729)
	 NumericalMetadata(min_value=1.0, max_value=216.0, range_size=215.0, same_value_length=False)
#### Teacher: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1.0, max_value=3.0, range_size=2.0, same_value_length=True)
#### Gender: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1.0, max_value=2.0, range_size=1.0, same_value_length=True)
#### Ethnic: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1.0, max_value=4.0, range_size=3.0, same_value_length=True)
#### Freeredu: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1.0, max_value=2.0, range_size=1.0, same_value_length=True)
#### Score: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=30.0, max_value=95.0, range_size=65.0, same_value_length=False)
#### wesson: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=(0, 1), distribution=(76, 141), longest=None, shortest=None, null_values=False, ratio_max_length=None)
	 NumericalMetadata(min_value=0, max_value=1, range_size=1, same_value_length=True)
## SAT_california

#### index: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=1000, shortest=0, null_values=False, ratio_max_length=0.001713796058269066)
	 NumericalMetadata(min_value=0, max_value=2333, range_size=2333, same_value_length=False)
#### cds: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=10000000000000, shortest=0, null_values=False, ratio_max_length=0.005998286203941731)
	 NumericalMetadata(min_value=0, max_value=58727695838305, range_size=58727695838305, same_value_length=False)
#### rtype: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### sname: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### dname: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### cname: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### enroll12: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0, max_value=492835, range_size=492835, same_value_length=False)
#### NumTstTakr: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0, max_value=214262, range_size=214262, same_value_length=False)
#### AvgScrRead: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=261.0, max_value=657.0, range_size=396.0, same_value_length=False)
#### AvgScrMath: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=264.0, max_value=710.0, range_size=446.0, same_value_length=False)
#### AvgScrWrit: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=263.0, max_value=677.0, range_size=414.0, same_value_length=False)
#### NumGE1500: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.0, max_value=89840.0, range_size=89840.0, same_value_length=False)
#### PctGE1500: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.0, max_value=98.53, range_size=98.53, same_value_length=False)
#### year: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CONSTANT
	 KindMetadata(value=(1516,), distribution=None, longest=None, shortest=None, null_values=False, ratio_max_length=None)
	 NumericalMetadata(min_value=1516, max_value=1516, range_size=0, same_value_length=True)
## states_all

#### PRIMARY_KEY: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=1992_DISTRICT_OF_COLUMBIA, shortest=1992_IOWA, null_values=False, ratio_max_length=0.014577259475218658)
#### STATE: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### YEAR: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1986, max_value=2019, range_size=33, same_value_length=True)
#### ENROLL: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=43866.0, max_value=6307022.0, range_size=6263156.0, same_value_length=False)
#### TOTAL_REVENUE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=465650.0, max_value=89217262.0, range_size=88751612.0, same_value_length=False)
#### FEDERAL_REVENUE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=31020.0, max_value=9990221.0, range_size=9959201.0, same_value_length=False)
#### STATE_REVENUE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.0, max_value=50904567.0, range_size=50904567.0, same_value_length=False)
#### LOCAL_REVENUE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=22093.0, max_value=36105265.0, range_size=36083172.0, same_value_length=False)
#### TOTAL_EXPENDITURE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=481665.0, max_value=85320133.0, range_size=84838468.0, same_value_length=False)
#### INSTRUCTION_EXPENDITURE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=265549.0, max_value=43964520.0, range_size=43698971.0, same_value_length=False)
#### SUPPORT_SERVICES_EXPENDITURE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=139963.0, max_value=26058021.0, range_size=25918058.0, same_value_length=False)
#### OTHER_EXPENDITURE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=11541.0, max_value=3995951.0, range_size=3984410.0, same_value_length=False)
#### CAPITAL_OUTLAY_EXPENDITURE: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=12708.0, max_value=10223657.0, range_size=10210949.0, same_value_length=False)
#### GRADES_PK_G: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=96.0, max_value=256222.0, range_size=256126.0, same_value_length=False)
#### GRADES_KG_G: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=5122.0, max_value=535379.0, range_size=530257.0, same_value_length=False)
#### GRADES_4_G: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=4577.0, max_value=493415.0, range_size=488838.0, same_value_length=False)
#### GRADES_8_G: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=3371.0, max_value=500143.0, range_size=496772.0, same_value_length=False)
#### GRADES_12_G: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=2572.0, max_value=498403.0, range_size=495831.0, same_value_length=False)
#### GRADES_1_8_G: 
	 Type = INT
	 Incomplete = True
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=37698.0, max_value=3929869.0, range_size=3892171.0, same_value_length=False)
#### GRADES_9_12_G: 
	 Type = INT
	 Incomplete = True
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=13530.0, max_value=2013687.0, range_size=2000157.0, same_value_length=False)
#### GRADES_ALL_G: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=68449.0, max_value=6441557.0, range_size=6373108.0, same_value_length=False)
#### AVG_MATH_4_SCORE: 
	 Type = INT
	 Incomplete = True
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=192.0, max_value=253.0, range_size=61.0, same_value_length=False)
#### AVG_MATH_8_SCORE: 
	 Type = INT
	 Incomplete = True
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=231.0, max_value=301.0, range_size=70.0, same_value_length=False)
#### AVG_READING_4_SCORE: 
	 Type = INT
	 Incomplete = True
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=179.0, max_value=237.0, range_size=58.0, same_value_length=False)
#### AVG_READING_8_SCORE: 
	 Type = INT
	 Incomplete = True
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=236.0, max_value=280.0, range_size=44.0, same_value_length=False)
## steam

#### appid: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=1000080, shortest=10, null_values=False, ratio_max_length=0.00025854108956602033)
	 NumericalMetadata(min_value=10, max_value=1069460, range_size=1069450, same_value_length=False)
#### name: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### release_date: 
	 Type = DATE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### english: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=(1, 0), distribution=(511, 26564), longest=None, shortest=None, null_values=False, ratio_max_length=None)
	 NumericalMetadata(min_value=0, max_value=1, range_size=1, same_value_length=True)
#### developer: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### publisher: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### platforms: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### required_age: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0, max_value=18, range_size=18, same_value_length=False)
#### categories: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### genres: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### steamspy_tags: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### achievements: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0, max_value=9821, range_size=9821, same_value_length=False)
#### positive_ratings: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0, max_value=2644404, range_size=2644404, same_value_length=False)
#### negative_ratings: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0, max_value=487076, range_size=487076, same_value_length=False)
#### average_playtime: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0, max_value=190625, range_size=190625, same_value_length=False)
#### median_playtime: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0, max_value=190625, range_size=190625, same_value_length=False)
#### owners: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### price: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.0, max_value=421.99, range_size=421.99, same_value_length=False)
## supermarket_sales

#### Invoice ID: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=750-67-8428, shortest=750-67-8428, null_values=False, ratio_max_length=0.011)
#### Branch: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### City: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### Customer type: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=('Member', 'Normal'), distribution=(499, 501), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### Gender: 
	 Type = ALPHABETIC
	 Incomplete = False
	 Kind = DataKind.BOOL
	 KindMetadata(value=('Female', 'Male'), distribution=(499, 501), longest=None, shortest=None, null_values=False, ratio_max_length=None)
#### Product line: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### Unit price: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=10.08, max_value=99.96, range_size=89.88, same_value_length=False)
#### Quantity: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1, max_value=10, range_size=9, same_value_length=False)
#### Tax 5%: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.5085, max_value=49.65, range_size=49.1415, same_value_length=False)
#### Total: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=10.6785, max_value=1042.65, range_size=1031.9715, same_value_length=False)
#### Date: 
	 Type = DATE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### Time: 
	 Type = DATE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Payment: 
	 Type = PHRASE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### cogs: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=10.17, max_value=993.0, range_size=982.83, same_value_length=False)
#### gross margin percentage: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.CONSTANT
	 KindMetadata(value=(4.761904762,), distribution=None, longest=None, shortest=None, null_values=False, ratio_max_length=None)
	 NumericalMetadata(min_value=4.761904762, max_value=4.761904762, range_size=0.0, same_value_length=True)
#### gross income: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.5085, max_value=49.65, range_size=49.1415, same_value_length=False)
#### Rating: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=4.0, max_value=10.0, range_size=6.0, same_value_length=False)
## vgsales

#### Rank: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.ID
	 KindMetadata(value=None, distribution=None, longest=10000, shortest=1, null_values=False, ratio_max_length=0.0003012411133871551)
	 NumericalMetadata(min_value=1, max_value=16600, range_size=16599, same_value_length=False)
#### Name: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
#### Platform: 
	 Type = ALPHANUMERIC
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### Year: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1980.0, max_value=2020.0, range_size=40.0, same_value_length=False)
#### Genre: 
	 Type = ALL
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### Publisher: 
	 Type = ARTICLE
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
#### NA_Sales: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.0, max_value=41.49, range_size=41.49, same_value_length=False)
#### EU_Sales: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.0, max_value=29.02, range_size=29.02, same_value_length=False)
#### JP_Sales: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.0, max_value=10.22, range_size=10.22, same_value_length=False)
#### Other_Sales: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.0, max_value=10.57, range_size=10.57, same_value_length=False)
#### Global_Sales: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.01, max_value=82.74, range_size=82.72999999999999, same_value_length=False)
## winequality-red

#### fixed acidity: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=4.6, max_value=15.9, range_size=11.3, same_value_length=False)
#### volatile acidity: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.12, max_value=1.58, range_size=1.46, same_value_length=False)
#### citric acid: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.0, max_value=1.0, range_size=1.0, same_value_length=False)
#### residual sugar: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.9, max_value=15.5, range_size=14.6, same_value_length=False)
#### chlorides: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.012, max_value=0.611, range_size=0.599, same_value_length=False)
#### free sulfur dioxide: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1.0, max_value=72.0, range_size=71.0, same_value_length=False)
#### total sulfur dioxide: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=6.0, max_value=289.0, range_size=283.0, same_value_length=False)
#### density: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.99007, max_value=1.00369, range_size=0.013619999999999965, same_value_length=False)
#### pH: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=2.74, max_value=4.01, range_size=1.2699999999999996, same_value_length=False)
#### sulphates: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.33, max_value=2.0, range_size=1.67, same_value_length=False)
#### alcohol: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=8.4, max_value=14.9, range_size=6.5, same_value_length=False)
#### quality: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=3, max_value=8, range_size=5, same_value_length=True)
## winequality

#### fixed acidity: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=4.6, max_value=15.9, range_size=11.3, same_value_length=False)
#### volatile acidity: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.12, max_value=1.58, range_size=1.46, same_value_length=False)
#### citric acid: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.0, max_value=1.0, range_size=1.0, same_value_length=False)
#### residual sugar: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.9, max_value=15.5, range_size=14.6, same_value_length=False)
#### chlorides: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.012, max_value=0.611, range_size=0.599, same_value_length=False)
#### free sulfur dioxide: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=1.0, max_value=72.0, range_size=71.0, same_value_length=False)
#### total sulfur dioxide: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=6.0, max_value=289.0, range_size=283.0, same_value_length=False)
#### density: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.UNDEFINED
	 NumericalMetadata(min_value=0.99007, max_value=1.00369, range_size=0.013619999999999965, same_value_length=False)
#### pH: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=2.74, max_value=4.01, range_size=1.2699999999999996, same_value_length=False)
#### sulphates: 
	 Type = HUMAN_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=0.33, max_value=2.0, range_size=1.67, same_value_length=False)
#### alcohol: 
	 Type = COMPUTER_GENERATED
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=8.4, max_value=14.9, range_size=6.5, same_value_length=False)
#### quality: 
	 Type = INT
	 Incomplete = False
	 Kind = DataKind.CATEGORICAL
	 NumericalMetadata(min_value=3, max_value=8, range_size=5, same_value_length=True)
