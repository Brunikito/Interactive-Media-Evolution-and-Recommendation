/**
 * @file relation_properties.h
 * @brief Contains constants, enumerations, and mappings related to languages, countries, and time zones.
 */

#ifndef RELATION_PROPERTIES_H
#define RELATION_PROPERTIES_H

namespace RelationProperties{
/**
 * @brief Maximum number of languages per country.
 */
constexpr int MAX_LANGS_PER_COUNTRY = 26;

/**
 * @brief Number of distinct occupation types (or work roles).
 */
constexpr int NUMWORKS = 144;

/**
 * @brief Number of supported countries.
 */
constexpr int NUMCOUNTRIES = 61;

/**
 * @brief Number of distinct supported languages.
 */
constexpr int NUMLANGUAGES = 157;

/**
 * @brief Number of tag categories used for content tagging.
 */
constexpr int NUMTAGS = 15;

/**
 * @brief Maximum possible age for users in the system.
 */
constexpr int USERMAXAGE = 100;

/**
 * @enum LanguageCode
 * @brief Enumeration of supported language codes.
 *
 * This enum provides symbolic constants for each language.
 * It maps directly to language indices used throughout the platform.
 */
enum LanguageCode {
    ABX = 0, ADY, AF, AKL, AR, AS, AV, AY, AZ, BA,
    BCL, BER, BG, BH, BIK, BN, BR, BUA, CA, CAU, CBK,
    CE, CEB, CHM, CMN, CO, CS, CV, CY, DA, DE, DIQ,
    DOI, DTA, EL, EN, ES, ET, EU, FA, FI, FIL, FO,
    FR, FRP, FY, GA, GD, GL, GN, GU, HAK, HAW, HE,
    HI, HIL, HR, HU, IBG, ID, ILO, INC, INH, IT, IU,
    JA, JV, KBD, KM, KN, KO, KOK, KRC, KRJ, KS, KU,
    KV, LB, LT, LUS, LV, MDF, MDH, MI, ML, MNI, MNS,
    MR, MRW, MS, MSB, MTA, MWL, MYV, NAN, NB, NE, NL,
    NN, NO, NOG, NR, NSO, OC, OR, PA, PAG, PAM, PL,
    PT, QU, RM, RO, ROM, RU, SA, SAH, SAT, SC, SD,
    SE, SGD, SIT, SK, SL, SMA, SMN, SR, SS, ST, SV,
    TA, TE, TH, TL, TN, TR, TS, TSG, TT, TUT, TYV,
    UDM, UG, UK, UR, VE, VI, WAR, WUU, XAL, XH, YKA,
    YUE, ZA, ZH, ZU
};

/**
 * @enum TimeZone
 * @brief Enumeration of time zone offsets in seconds from UTC.
 *
 * These values represent standard time zone offsets and are used to localize user and content data.
 */
enum TimeZone {
    UTC_n12 = -43200, UTC_n11 = -39600, UTC_n10 = -36000, UTC_n9 = -32400, UTC_n8 = -28800, 
    UTC_n7 = -25200, UTC_n6 = -21600, UTC_n5 = -18000, UTC_n4 = -14400, UTC_n3 = -10800,
    UTC_n2 = -7200, UTC_n1 = -3600, UTC_0 = 0, UTC_1 = 3600, UTC_2 = 7200, UTC_3 = 10800, 
    UTC_4 = 14400, UTC_5 = 18000, UTC_5_5 = 19800, UTC_6 = 21600, UTC_7 = 25200, 
    UTC_8 = 28800, UTC_9 = 32400, UTC_10 = 36000, UTC_11 = 39600, UTC_12 = 43200
};

/**
 * @var countryLanguages
 * @brief Array that maps each country (by index) to its official or spoken languages.
 *
 * Each country is represented as an array of LanguageCode enums, with a maximum of MAX_LANGS_PER_COUNTRY entries.
 * 
 * @note Countries with fewer languages use zero-padding or redundant values.
 */
constexpr LanguageCode countryLanguages[61] = {
    ES, ES, EN, ES, ES, ES, EN, 
    ES, ES, PT, EN, EN, 
    PT, DE, NL, DE, CS, DE, 
    DA, ES, FR, HR, 
    HU, IT, LB, AR, NL, 
    NO, PL, SV, SK, BG, 
    EL, ET, AR, FI, EL, HE, 
    LT, LV, RO, UK, 
    ZU, RU, AR, TR, AR, 
    EN, ID, TH, VI, ZH, 
    ZH, MS, TL, CMN, ZH, 
    JA, KO, EN, EN
};

/**
 * @var countryTimeZones
 * @brief Array mapping each country (by index) to its time zone.
 *
 * The time zone is represented by the TimeZone enum and indicates the UTC offset.
 * Useful for localizing scheduling and content interaction data.
 */
constexpr TimeZone countryTimeZones[61] = {
    UTC_n6, UTC_n6,   ///< 2 países no UTC -6
    UTC_n5, UTC_n5, UTC_n5, UTC_n5, UTC_n5,   ///< 5 países no UTC -5
    UTC_n4,   ///< 1 país no UTC -4
    UTC_n3, UTC_n3,   ///< 2 países no UTC -3
    UTC_0, UTC_0, UTC_0,   ///< 3 países no UTC +0
    UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1, UTC_1,  ///< 18 países no UTC +1
    UTC_2, UTC_2, UTC_2, UTC_2, UTC_2, UTC_2, UTC_2, UTC_2, UTC_2, UTC_2, UTC_2,   ///< 12 países no UTC +2
    UTC_3, UTC_3, UTC_3,   ///< 3 países no UTC +3
    UTC_4,   ///< 1 país no UTC +4
    UTC_5, UTC_5, UTC_5,  ///< 3 países no UTC +5
    UTC_5_5,   ///< 1 país no UTC +5:30
    UTC_7, UTC_7, UTC_7,   ///< 3 países no UTC +7
    UTC_8, UTC_8, UTC_8, UTC_8, UTC_8, UTC_8,   ///< 6 países no UTC +8
    UTC_9, UTC_9,   ///< 2 países no UTC +9
    UTC_10,   ///< 1 país no UTC +10
    UTC_12    ///< 1 país no UTC +12
};


/**
 * @brief Horários fixos para o primeiro turno (7h–15h).
 */
constexpr Relations::Schedule FIRST_SHIFT_SCHEDULE = {
    22,  // bedTime
    6,   // wakeTime
    12,  // lunchTime
    21,  // dinnerTime
    7,   // workTime
    15,  // freeFromWorkTime
    0b0111110 // workDays: segunda a sexta (bitmask)
};

/**
 * @brief Horários fixos para o segundo turno (14h–22h).
 */
constexpr Relations::Schedule SECOND_SHIFT_SCHEDULE = {
    0,   // bedTime
    8,   // wakeTime
    12,  // lunchTime
    23,  // dinnerTime
    14,  // workTime
    22,  // freeFromWorkTime
    0b0111110 // workDays: segunda a sexta
};
};
#endif