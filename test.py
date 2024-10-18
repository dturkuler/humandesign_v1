import hd_features as hd
import hd_constants
import convertJSON as cj

#examples for birth time format
zone = 'Asia/Istanbul'
birth_time= 1968,2,21,11,15,0 #DT
#birth_time= 1973,1,19,11,15,0 #BT


#automatic timezone(tz) offset calculation (for all avl. timezones see pytz.all_timezones)
hours = hd.get_utc_offset_from_tz(birth_time,zone)

##manual time_zone offset calculation
#hours=8

timestamp = tuple(list(birth_time) + [hours])
single_result = hd.calc_single_hd_features(timestamp,report=True,channel_meaning=False)
# Example usage:
#------------------------------------------------
#Get JSON output
#------------------------------------------------
data = {
    "birth_date": (1967, 11, 26, 18, 29),
    "create_date": (1967, 11, 26, 18, 29),
    "energie_type": single_result[0],
    "inner_authority": single_result[1],
    "inc_cross": single_result[2],
    "profile": single_result[4],
    "active_chakras": single_result[7],
    "split": single_result[5],
    "variables": {'right_up': 'right', 'right_down': 'left', 'left_up': 'right', 'left_down': 'right'}
}

data = {
    "birth_date": single_result[9],
    "create_date": single_result[10],
    "energie_type": single_result[0],
    "inner_authority": single_result[1],
    "inc_cross": single_result[2],
    "profile": single_result[4],
    "active_chakras": single_result[7],
    "split": "{}".format(single_result[5]) ,
    "variables": {'right_up': 'right', 'right_down': 'left', 'left_up': 'right', 'left_down': 'right'}
}

# Get the JSON output
json_result = cj.general(data)
print(json_result)

gatesJS = cj.gatesJSON(single_result[6]) 
# Call the function and print the updated data
print(gatesJS)

channelsJS = cj.channelsJSON(single_result[8],False)
print(channelsJS)
#------------------------------------------------

#hours=2 #time_zone offset
#define persons you want to combine
#persons_dict = {"1":(1968,2,21,11,15,0,hours), "2":(1973,1,19,11,00,0,hours)}
#print ("#composite channels and chakras")
#print (hd.get_composite_combinations(persons_dict))
#print ("#full view, with readable meanings")
#print (hd.get_composite_combinations(persons_dict).explode(["new_channels","new_ch_meaning"]))
#print ("#composite gates matching penta ")
#print (hd.get_penta(persons_dict))


#working
