import hd_features as hd
import hd_constants

#examples for birth time format
zone = 'Asia/Istanbul'
#birth_time= 1968,2,21,11,15,0 #konrad adenauer
birth_time= 1973,1,19,11,15,0 #konrad adenauer


#automatic timezone(tz) offset calculation (for all avl. timezones see pytz.all_timezones)
hours = hd.get_utc_offset_from_tz(birth_time,zone)

##manual time_zone offset calculation
#hours=8

timestamp = tuple(list(birth_time) + [hours])
single_result = hd.calc_single_hd_features(timestamp,report=True,channel_meaning=True)

hours=2 #time_zone offset
#define persons you want to combine
persons_dict = {"1":(1968,2,21,11,15,0,hours),
                "2":(1972,1,19,11,15,0,hours),
                                        }
print ("#composite channels and chakras")
print (hd.get_composite_combinations(persons_dict))
print ("#full view, with readable meanings")
print (hd.get_composite_combinations(persons_dict).explode(["new_channels","new_ch_meaning"]))
print ("#composite gates matching penta ")
print (hd.get_penta(persons_dict))
