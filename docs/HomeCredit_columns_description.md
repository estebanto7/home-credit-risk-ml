# Home Credit — Classified Variable Dictionary

## Classification Criteria

- **Identifier:** A record key or relational key; even when stored as a number, it should not be treated as a quantity.
- **Nominal categorical / binary nominal:** Categories without an intrinsic ordering; 0/1 flags represent states rather than magnitudes.
- **Ordinal categorical:** Categories with a meaningful order; distances between categories are not assumed to be equal.
- **Discrete quantitative:** Counts, numbers of payments or installments, and days past due recorded as counts.
- **Continuous quantitative:** Monetary amounts, areas, ratios, rates, and other measurements; the conceptual type does not require decimal values in the CSV.
- **Relative-time quantitative:** Days or months measured relative to the application; these are time offsets, not calendar dates.
- **Cyclical:** Day of week or hour of day, with periodic structure; hours are discrete, but 23:00 and 00:00 are adjacent.
- **Mixed categorical:** Combines categories of different kinds (for example, ordered severity levels and special status codes).

## Dictionary by Dataset

### application_train.csv / application_test.csv — 122 variables

| Table | Row | Description | Special | Statistical Type |
| --- | --- | --- | --- | --- |
| application_train.csv / application_test.csv | `SK_ID_CURR` | ID of loan in our sample | — | Identifier (nominal key) |
| application_train.csv / application_test.csv | `TARGET` | Target variable (1 - client with payment difficulties: he/she had late payment more than X days on at least one of the first Y installments of the loan in our sample, 0 - all other cases) | — | Binary nominal categorical (target) |
| application_train.csv / application_test.csv | `NAME_CONTRACT_TYPE` | Identification if loan is cash or revolving | — | Nominal categorical |
| application_train.csv / application_test.csv | `CODE_GENDER` | Gender of the client | — | Nominal categorical |
| application_train.csv / application_test.csv | `FLAG_OWN_CAR` | Flag if the client owns a car | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_OWN_REALTY` | Flag if client owns a house or flat | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `CNT_CHILDREN` | Number of children the client has | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `AMT_INCOME_TOTAL` | Income of the client | — | Continuous quantitative (monetary) |
| application_train.csv / application_test.csv | `AMT_CREDIT` | Credit amount of the loan | — | Continuous quantitative (monetary) |
| application_train.csv / application_test.csv | `AMT_ANNUITY` | Loan annuity | — | Continuous quantitative (monetary) |
| application_train.csv / application_test.csv | `AMT_GOODS_PRICE` | For consumer loans it is the price of the goods for which the loan is given | — | Continuous quantitative (monetary) |
| application_train.csv / application_test.csv | `NAME_TYPE_SUITE` | Who was accompanying client when he was applying for the loan | — | Nominal categorical |
| application_train.csv / application_test.csv | `NAME_INCOME_TYPE` | Clients income type (businessman, working, maternity leave,…) | — | Nominal categorical |
| application_train.csv / application_test.csv | `NAME_EDUCATION_TYPE` | Level of highest education the client achieved | — | Ordinal categorical |
| application_train.csv / application_test.csv | `NAME_FAMILY_STATUS` | Family status of the client | — | Nominal categorical |
| application_train.csv / application_test.csv | `NAME_HOUSING_TYPE` | What is the housing situation of the client (renting, living with parents, ...) | — | Nominal categorical |
| application_train.csv / application_test.csv | `REGION_POPULATION_RELATIVE` | Normalized population of region where client lives (higher number means the client lives in more populated region) | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `DAYS_BIRTH` | Client's age in days at the time of application | time only relative to the application | Relative-time quantitative (day offset) |
| application_train.csv / application_test.csv | `DAYS_EMPLOYED` | How many days before the application the person started current employment | time only relative to the application | Relative-time quantitative (day offset) |
| application_train.csv / application_test.csv | `DAYS_REGISTRATION` | How many days before the application did client change his registration | time only relative to the application | Relative-time quantitative (day offset) |
| application_train.csv / application_test.csv | `DAYS_ID_PUBLISH` | How many days before the application did client change the identity document with which he applied for the loan | time only relative to the application | Relative-time quantitative (day offset) |
| application_train.csv / application_test.csv | `OWN_CAR_AGE` | Age of client's car | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `FLAG_MOBIL` | Did client provide mobile phone (1=YES, 0=NO) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_EMP_PHONE` | Did client provide work phone (1=YES, 0=NO) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_WORK_PHONE` | Did client provide home phone (1=YES, 0=NO) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_CONT_MOBILE` | Was mobile phone reachable (1=YES, 0=NO) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_PHONE` | Did client provide home phone (1=YES, 0=NO) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_EMAIL` | Did client provide email (1=YES, 0=NO) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `OCCUPATION_TYPE` | What kind of occupation does the client have | — | Nominal categorical |
| application_train.csv / application_test.csv | `CNT_FAM_MEMBERS` | How many family members does client have | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `REGION_RATING_CLIENT` | Our rating of the region where client lives (1,2,3) | — | Ordinal categorical |
| application_train.csv / application_test.csv | `REGION_RATING_CLIENT_W_CITY` | Our rating of the region where client lives with taking city into account (1,2,3) | — | Ordinal categorical |
| application_train.csv / application_test.csv | `WEEKDAY_APPR_PROCESS_START` | On which day of the week did the client apply for the loan | — | Cyclical nominal categorical (day of week) |
| application_train.csv / application_test.csv | `HOUR_APPR_PROCESS_START` | Approximately at what hour did the client apply for the loan | rounded | Discrete cyclical time (hour of day) |
| application_train.csv / application_test.csv | `REG_REGION_NOT_LIVE_REGION` | Flag if client's permanent address does not match contact address (1=different, 0=same, at region level) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `REG_REGION_NOT_WORK_REGION` | Flag if client's permanent address does not match work address (1=different, 0=same, at region level) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `LIVE_REGION_NOT_WORK_REGION` | Flag if client's contact address does not match work address (1=different, 0=same, at region level) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `REG_CITY_NOT_LIVE_CITY` | Flag if client's permanent address does not match contact address (1=different, 0=same, at city level) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `REG_CITY_NOT_WORK_CITY` | Flag if client's permanent address does not match work address (1=different, 0=same, at city level) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `LIVE_CITY_NOT_WORK_CITY` | Flag if client's contact address does not match work address (1=different, 0=same, at city level) | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `ORGANIZATION_TYPE` | Type of organization where client works | — | Nominal categorical |
| application_train.csv / application_test.csv | `EXT_SOURCE_1` | Normalized score from external data source | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `EXT_SOURCE_2` | Normalized score from external data source | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `EXT_SOURCE_3` | Normalized score from external data source | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `APARTMENTS_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `BASEMENTAREA_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `YEARS_BEGINEXPLUATATION_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `YEARS_BUILD_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `COMMONAREA_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `ELEVATORS_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `ENTRANCES_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `FLOORSMAX_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `FLOORSMIN_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LANDAREA_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LIVINGAPARTMENTS_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LIVINGAREA_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `NONLIVINGAPARTMENTS_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `NONLIVINGAREA_AVG` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `APARTMENTS_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `BASEMENTAREA_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `YEARS_BEGINEXPLUATATION_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `YEARS_BUILD_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `COMMONAREA_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `ELEVATORS_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `ENTRANCES_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `FLOORSMAX_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `FLOORSMIN_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LANDAREA_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LIVINGAPARTMENTS_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LIVINGAREA_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `NONLIVINGAPARTMENTS_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `NONLIVINGAREA_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `APARTMENTS_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `BASEMENTAREA_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `YEARS_BEGINEXPLUATATION_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `YEARS_BUILD_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `COMMONAREA_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `ELEVATORS_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `ENTRANCES_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `FLOORSMAX_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `FLOORSMIN_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LANDAREA_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LIVINGAPARTMENTS_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `LIVINGAREA_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `NONLIVINGAPARTMENTS_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `NONLIVINGAREA_MEDI` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `FONDKAPREMONT_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Nominal categorical |
| application_train.csv / application_test.csv | `HOUSETYPE_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Nominal categorical |
| application_train.csv / application_test.csv | `TOTALAREA_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Continuous quantitative (normalized) |
| application_train.csv / application_test.csv | `WALLSMATERIAL_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Nominal categorical |
| application_train.csv / application_test.csv | `EMERGENCYSTATE_MODE` | Normalized information about building where the client lives, What is average (_AVG suffix), modus (_MODE suffix), median (_MEDI suffix) apartment size, common area, living area, age of building, number of elevators, number of entrances, state of the building, number of floor | normalized | Nominal categorical |
| application_train.csv / application_test.csv | `OBS_30_CNT_SOCIAL_CIRCLE` | How many observation of client's social surroundings with observable 30 DPD (days past due) default | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `DEF_30_CNT_SOCIAL_CIRCLE` | How many observation of client's social surroundings defaulted on 30 DPD (days past due) | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `OBS_60_CNT_SOCIAL_CIRCLE` | How many observation of client's social surroundings with observable 60 DPD (days past due) default | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `DEF_60_CNT_SOCIAL_CIRCLE` | How many observation of client's social surroundings defaulted on 60 (days past due) DPD | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `DAYS_LAST_PHONE_CHANGE` | How many days before application did client change phone | — | Relative-time quantitative (day offset) |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_2` | Did client provide document 2 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_3` | Did client provide document 3 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_4` | Did client provide document 4 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_5` | Did client provide document 5 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_6` | Did client provide document 6 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_7` | Did client provide document 7 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_8` | Did client provide document 8 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_9` | Did client provide document 9 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_10` | Did client provide document 10 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_11` | Did client provide document 11 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_12` | Did client provide document 12 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_13` | Did client provide document 13 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_14` | Did client provide document 14 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_15` | Did client provide document 15 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_16` | Did client provide document 16 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_17` | Did client provide document 17 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_18` | Did client provide document 18 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_19` | Did client provide document 19 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_20` | Did client provide document 20 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `FLAG_DOCUMENT_21` | Did client provide document 21 | — | Binary nominal categorical |
| application_train.csv / application_test.csv | `AMT_REQ_CREDIT_BUREAU_HOUR` | Number of enquiries to Credit Bureau about the client one hour before application | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `AMT_REQ_CREDIT_BUREAU_DAY` | Number of enquiries to Credit Bureau about the client one day before application (excluding one hour before application) | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `AMT_REQ_CREDIT_BUREAU_WEEK` | Number of enquiries to Credit Bureau about the client one week before application (excluding one day before application) | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `AMT_REQ_CREDIT_BUREAU_MON` | Number of enquiries to Credit Bureau about the client one month before application (excluding one week before application) | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `AMT_REQ_CREDIT_BUREAU_QRT` | Number of enquiries to Credit Bureau about the client 3 month before application (excluding one month before application) | — | Discrete quantitative (count) |
| application_train.csv / application_test.csv | `AMT_REQ_CREDIT_BUREAU_YEAR` | Number of enquiries to Credit Bureau about the client one day year (excluding last 3 months before application) | — | Discrete quantitative (count) |

### bureau.csv — 17 variables

| Table | Row | Description | Special | Statistical Type |
| --- | --- | --- | --- | --- |
| bureau.csv | `SK_ID_CURR` | ID of loan in our sample - one loan in our sample can have 0,1,2 or more related previous credits in credit bureau | hashed | Identifier (nominal key) |
| bureau.csv | `SK_BUREAU_ID` | Recoded ID of previous Credit Bureau credit related to our loan (unique coding for each loan application) | hashed | Identifier (nominal key) |
| bureau.csv | `CREDIT_ACTIVE` | Status of the Credit Bureau (CB) reported credits | — | Nominal categorical |
| bureau.csv | `CREDIT_CURRENCY` | Recoded currency of the Credit Bureau credit | recoded | Nominal categorical |
| bureau.csv | `DAYS_CREDIT` | How many days before current application did client apply for Credit Bureau credit | time only relative to the application | Relative-time quantitative (day offset) |
| bureau.csv | `CREDIT_DAY_OVERDUE` | Number of days past due on CB credit at the time of application for related loan in our sample | — | Discrete quantitative (count) |
| bureau.csv | `DAYS_CREDIT_ENDDATE` | Remaining duration of CB credit (in days) at the time of application in Home Credit | time only relative to the application | Relative-time quantitative (day offset) |
| bureau.csv | `DAYS_ENDDATE_FACT` | Days since CB credit ended at the time of application in Home Credit (only for closed credit) | time only relative to the application | Relative-time quantitative (day offset) |
| bureau.csv | `AMT_CREDIT_MAX_OVERDUE` | Maximal amount overdue on the Credit Bureau credit so far (at application date of loan in our sample) | — | Continuous quantitative (monetary) |
| bureau.csv | `CNT_CREDIT_PROLONG` | How many times was the Credit Bureau credit prolonged | — | Discrete quantitative (count) |
| bureau.csv | `AMT_CREDIT_SUM` | Current credit amount for the Credit Bureau credit | — | Continuous quantitative (monetary) |
| bureau.csv | `AMT_CREDIT_SUM_DEBT` | Current debt on Credit Bureau credit | — | Continuous quantitative (monetary) |
| bureau.csv | `AMT_CREDIT_SUM_LIMIT` | Current credit limit of credit card reported in Credit Bureau | — | Continuous quantitative (monetary) |
| bureau.csv | `AMT_CREDIT_SUM_OVERDUE` | Current amount overdue on Credit Bureau credit | — | Continuous quantitative (monetary) |
| bureau.csv | `CREDIT_TYPE` | Type of Credit Bureau credit (Car, cash,...) | — | Nominal categorical |
| bureau.csv | `DAYS_CREDIT_UPDATE` | How many days before loan application did last information about the Credit Bureau credit come | time only relative to the application | Relative-time quantitative (day offset) |
| bureau.csv | `AMT_ANNUITY` | Annuity of the Credit Bureau credit | — | Continuous quantitative (monetary) |

### bureau_balance.csv — 3 variables

| Table | Row | Description | Special | Statistical Type |
| --- | --- | --- | --- | --- |
| bureau_balance.csv | `SK_BUREAU_ID` | Recoded ID of Credit Bureau credit (unique coding for each application) - use this to join to CREDIT_BUREAU table | hashed | Identifier (nominal key) |
| bureau_balance.csv | `MONTHS_BALANCE` | Month of balance relative to application date (-1 means the freshest balance date) | time only relative to the application | Discrete relative-time quantitative (month offset) |
| bureau_balance.csv | `STATUS` | Status of Credit Bureau loan during the month (active, closed, DPD0-30,… [C means closed, X means status unknown, 0 means no DPD, 1 means maximal did during month between 1-30, 2 means DPD 31-60,… 5 means DPD 120+ or sold or written off ] ) | — | Mixed categorical (ordinal 0–5; nominal C/X) |

### POS_CASH_balance.csv — 8 variables

| Table | Row | Description | Special | Statistical Type |
| --- | --- | --- | --- | --- |
| POS_CASH_balance.csv | `SK_ID_PREV` | ID of previous credit in Home Credit related to loan in our sample. (One loan in our sample can have 0,1,2 or more previous loans in Home Credit) | — | Identifier (nominal key) |
| POS_CASH_balance.csv | `SK_ID_CURR` | ID of loan in our sample | — | Identifier (nominal key) |
| POS_CASH_balance.csv | `MONTHS_BALANCE` | Month of balance relative to application date (-1 means the information to the freshest monthly snapshot, 0 means the information at application - often it will be the same as -1 as many banks are not updating the information to Credit Bureau regularly ) | time only relative to the application | Discrete relative-time quantitative (month offset) |
| POS_CASH_balance.csv | `CNT_INSTALMENT` | Term of previous credit (can change over time) | — | Discrete quantitative (count) |
| POS_CASH_balance.csv | `CNT_INSTALMENT_FUTURE` | Installments left to pay on the previous credit | — | Discrete quantitative (count) |
| POS_CASH_balance.csv | `NAME_CONTRACT_STATUS` | Contract status during the month | — | Nominal categorical |
| POS_CASH_balance.csv | `SK_DPD` | DPD (days past due) during the month of previous credit | — | Discrete quantitative (count) |
| POS_CASH_balance.csv | `SK_DPD_DEF` | DPD during the month with tolerance (debts with low loan amounts are ignored) of the previous credit | — | Discrete quantitative (count) |

### credit_card_balance.csv — 23 variables

| Table | Row | Description | Special | Statistical Type |
| --- | --- | --- | --- | --- |
| credit_card_balance.csv | `SK_ID_PREV` | ID of previous credit in Home credit related to loan in our sample. (One loan in our sample can have 0,1,2 or more previous loans in Home Credit) | hashed | Identifier (nominal key) |
| credit_card_balance.csv | `SK_ID_CURR` | ID of loan in our sample | hashed | Identifier (nominal key) |
| credit_card_balance.csv | `MONTHS_BALANCE` | Month of balance relative to application date (-1 means the freshest balance date) | time only relative to the application | Discrete relative-time quantitative (month offset) |
| credit_card_balance.csv | `AMT_BALANCE` | Balance during the month of previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_CREDIT_LIMIT_ACTUAL` | Credit card limit during the month of the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_DRAWINGS_ATM_CURRENT` | Amount drawing at ATM during the month of the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_DRAWINGS_CURRENT` | Amount drawing during the month of the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_DRAWINGS_OTHER_CURRENT` | Amount of other drawings during the month of the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_DRAWINGS_POS_CURRENT` | Amount drawing or buying goods during the month of the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_INST_MIN_REGULARITY` | Minimal installment for this month of the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_PAYMENT_CURRENT` | How much did the client pay during the month on the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_PAYMENT_TOTAL_CURRENT` | How much did the client pay during the month in total on the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_RECEIVABLE_PRINCIPAL` | Amount receivable for principal on the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_RECIVABLE` | Amount receivable on the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `AMT_TOTAL_RECEIVABLE` | Total amount receivable on the previous credit | — | Continuous quantitative (monetary) |
| credit_card_balance.csv | `CNT_DRAWINGS_ATM_CURRENT` | Number of drawings at ATM during this month on the previous credit | — | Discrete quantitative (count) |
| credit_card_balance.csv | `CNT_DRAWINGS_CURRENT` | Number of drawings during this month on the previous credit | — | Discrete quantitative (count) |
| credit_card_balance.csv | `CNT_DRAWINGS_OTHER_CURRENT` | Number of other drawings during this month on the previous credit | — | Discrete quantitative (count) |
| credit_card_balance.csv | `CNT_DRAWINGS_POS_CURRENT` | Number of drawings for goods during this month on the previous credit | — | Discrete quantitative (count) |
| credit_card_balance.csv | `CNT_INSTALMENT_MATURE_CUM` | Number of paid installments on the previous credit | — | Discrete quantitative (count) |
| credit_card_balance.csv | `NAME_CONTRACT_STATUS` | Contract status (active signed,...) on the previous credit | — | Nominal categorical |
| credit_card_balance.csv | `SK_DPD` | DPD (Days past due) during the month on the previous credit | — | Discrete quantitative (count) |
| credit_card_balance.csv | `SK_DPD_DEF` | DPD (Days past due) during the month with tolerance (debts with low loan amounts are ignored) of the previous credit | — | Discrete quantitative (count) |

### previous_application.csv — 38 variables

| Table | Row | Description | Special | Statistical Type |
| --- | --- | --- | --- | --- |
| previous_application.csv | `SK_ID_PREV` | ID of previous credit in Home credit related to loan in our sample. (One loan in our sample can have 0,1,2 or more previous loan applications in Home Credit, previous application could, but not necessarily have to lead to credit) | hashed | Identifier (nominal key) |
| previous_application.csv | `SK_ID_CURR` | ID of loan in our sample | hashed | Identifier (nominal key) |
| previous_application.csv | `NAME_CONTRACT_TYPE` | Contract product type (Cash loan, consumer loan [POS] ,...) of the previous application | — | Nominal categorical |
| previous_application.csv | `AMT_ANNUITY` | Annuity of previous application | — | Continuous quantitative (monetary) |
| previous_application.csv | `AMT_APPLICATION` | For how much credit did client ask on the previous application | — | Continuous quantitative (monetary) |
| previous_application.csv | `AMT_CREDIT` | Final credit amount on the previous application. This differs from AMT_APPLICATION in a way that the AMT_APPLICATION is the amount for which the client initially applied for, but during our approval process he could have received different amount - AMT_CREDIT | — | Continuous quantitative (monetary) |
| previous_application.csv | `AMT_DOWN_PAYMENT` | Down payment on the previous application | — | Continuous quantitative (monetary) |
| previous_application.csv | `AMT_GOODS_PRICE` | Goods price of good that client asked for (if applicable) on the previous application | — | Continuous quantitative (monetary) |
| previous_application.csv | `WEEKDAY_APPR_PROCESS_START` | On which day of the week did the client apply for previous application | — | Cyclical nominal categorical (day of week) |
| previous_application.csv | `HOUR_APPR_PROCESS_START` | Approximately at what day hour did the client apply for the previous application | rounded | Discrete cyclical time (hour of day) |
| previous_application.csv | `FLAG_LAST_APPL_PER_CONTRACT` | Flag if it was last application for the previous contract. Sometimes by mistake of client or our clerk there could be more applications for one single contract | — | Binary nominal categorical |
| previous_application.csv | `NFLAG_LAST_APPL_IN_DAY` | Flag if the application was the last application per day of the client. Sometimes clients apply for more applications a day. Rarely it could also be error in our system that one application is in the database twice | — | Binary nominal categorical |
| previous_application.csv | `NFLAG_MICRO_CASH` | Flag Micro finance loan | — | Binary nominal categorical |
| previous_application.csv | `RATE_DOWN_PAYMENT` | Down payment rate normalized on previous credit | normalized | Continuous quantitative (normalized) |
| previous_application.csv | `RATE_INTEREST_PRIMARY` | Interest rate normalized on previous credit | normalized | Continuous quantitative (normalized) |
| previous_application.csv | `RATE_INTEREST_PRIVILEGED` | Interest rate normalized on previous credit | normalized | Continuous quantitative (normalized) |
| previous_application.csv | `NAME_CASH_LOAN_PURPOSE` | Purpose of the cash loan | — | Nominal categorical |
| previous_application.csv | `NAME_CONTRACT_STATUS` | Contract status (approved, cancelled, ...) of previous application | — | Nominal categorical |
| previous_application.csv | `DAYS_DECISION` | Relative to current application when was the decision about previous application made | time only relative to the application | Relative-time quantitative (day offset) |
| previous_application.csv | `NAME_PAYMENT_TYPE` | Payment method that client chose to pay for the previous application | — | Nominal categorical |
| previous_application.csv | `CODE_REJECT_REASON` | Why was the previous application rejected | — | Nominal categorical |
| previous_application.csv | `NAME_TYPE_SUITE` | Who accompanied client when applying for the previous application | — | Nominal categorical |
| previous_application.csv | `NAME_CLIENT_TYPE` | Was the client old or new client when applying for the previous application | — | Nominal categorical |
| previous_application.csv | `NAME_GOODS_CATEGORY` | What kind of goods did the client apply for in the previous application | — | Nominal categorical |
| previous_application.csv | `NAME_PORTFOLIO` | Was the previous application for CASH, POS, CAR, … | — | Nominal categorical |
| previous_application.csv | `NAME_PRODUCT_TYPE` | Was the previous application x-sell o walk-in | — | Nominal categorical |
| previous_application.csv | `CHANNEL_TYPE` | Through which channel we acquired the client on the previous application | — | Nominal categorical |
| previous_application.csv | `SELLERPLACE_AREA` | Selling area of seller place of the previous application | — | Continuous quantitative |
| previous_application.csv | `NAME_SELLER_INDUSTRY` | The industry of the seller | — | Nominal categorical |
| previous_application.csv | `CNT_PAYMENT` | Term of previous credit at application of the previous application | — | Discrete quantitative (count) |
| previous_application.csv | `NAME_YIELD_GROUP` | Grouped interest rate into small medium and high of the previous application | grouped | Ordinal categorical |
| previous_application.csv | `PRODUCT_COMBINATION` | Detailed product combination of the previous application | — | Nominal categorical |
| previous_application.csv | `DAYS_FIRST_DRAWING` | Relative to application date of current application when was the first disbursement of the previous application | time only relative to the application | Relative-time quantitative (day offset) |
| previous_application.csv | `DAYS_FIRST_DUE` | Relative to application date of current application when was the first due supposed to be of the previous application | time only relative to the application | Relative-time quantitative (day offset) |
| previous_application.csv | `DAYS_LAST_DUE_1ST_VERSION` | Relative to application date of current application when was the first due of the previous application | time only relative to the application | Relative-time quantitative (day offset) |
| previous_application.csv | `DAYS_LAST_DUE` | Relative to application date of current application when was the last due date of the previous application | time only relative to the application | Relative-time quantitative (day offset) |
| previous_application.csv | `DAYS_TERMINATION` | Relative to application date of current application when was the expected termination of the previous application | time only relative to the application | Relative-time quantitative (day offset) |
| previous_application.csv | `NFLAG_INSURED_ON_APPROVAL` | Did the client requested insurance during the previous application | — | Binary nominal categorical |

### installments_payments.csv — 8 variables

| Table | Row | Description | Special | Statistical Type |
| --- | --- | --- | --- | --- |
| installments_payments.csv | `SK_ID_PREV` | ID of previous credit in Home credit related to loan in our sample. (One loan in our sample can have 0,1,2 or more previous loans in Home Credit) | hashed | Identifier (nominal key) |
| installments_payments.csv | `SK_ID_CURR` | ID of loan in our sample | hashed | Identifier (nominal key) |
| installments_payments.csv | `NUM_INSTALMENT_VERSION` | Version of installment calendar (0 is for credit card) of previous credit. Change of installment version from month to month signifies that some parameter of payment calendar has changed | — | Nominal categorical (version code) |
| installments_payments.csv | `NUM_INSTALMENT_NUMBER` | On which installment we observe payment | — | Discrete quantitative (count) |
| installments_payments.csv | `DAYS_INSTALMENT` | When the installment of previous credit was supposed to be paid (relative to application date of current loan) | time only relative to the application | Relative-time quantitative (day offset) |
| installments_payments.csv | `DAYS_ENTRY_PAYMENT` | When was the installments of previous credit paid actually (relative to application date of current loan) | time only relative to the application | Relative-time quantitative (day offset) |
| installments_payments.csv | `AMT_INSTALMENT` | What was the prescribed installment amount of previous credit on this installment | — | Continuous quantitative (monetary) |
| installments_payments.csv | `AMT_PAYMENT` | What the client actually paid on previous credit on this installment | — | Continuous quantitative (monetary) |

## Cases Requiring Attention When Analyzing the CSV Files

1. **`TARGET` appears under `application_{train|test}` in the dictionary, but the target is present only in `application_train.csv`, not in `application_test.csv`.**
2. **`SK_BUREAU_ID`:** This is the spelling used in the supplied file. The actual Home Credit CSV files generally use `SK_ID_BUREAU`; check the column names in the data before joining tables. The source dictionary spelling has not been altered.
3. **`STATUS` in `bureau_balance`:** Values `0`–`5` represent progressively more severe delinquency levels; `C` (closed) and `X` (unknown) are not part of that ordered scale. Do not automatically encode every category as ordinal.
4. **`NAME_EDUCATION_TYPE` and `NAME_YIELD_GROUP`:** These are conceptually ordinal, but special or uninformative levels should be reviewed before imposing an order.
5. **`*_AVG`, `*_MODE`, `*_MEDI`:** According to the data dictionary, these are normalized building-related measurements. The `MODE` suffix identifies a summary variant; it does not automatically make a numeric measurement categorical. By contrast, `FONDKAPREMONT_MODE`, `HOUSETYPE_MODE`, `WALLSMATERIAL_MODE`, and `EMERGENCYSTATE_MODE` describe categories.
6. **`AMT_REQ_CREDIT_BUREAU_*`:** These fields count credit bureau inquiries. They are classified as counts even if `pandas` stores them as floating-point values due to missing data.
7. **`NUM_INSTALMENT_VERSION`:** This is a schedule-version code (with `0` associated with credit cards, according to the dictionary), not the total installment count or a directly comparable numerical quantity.
8. **Conceptual classification:** The most appropriate nominal, ordinal, or numeric encoding for modeling should be decided after examining the values observed in the training data.

---

*This document is a variable inventory and classification, not a dataset transformation or a finalized preprocessing plan.*
