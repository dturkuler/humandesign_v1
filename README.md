
# Human design (HD) engine 
HD engine is a script for calculation of single, composite and multiple human design features in python. 

# Forked
https://github.com/MicFell/human_design_engine




-------------------------------------------
# issues to be fixed
Error on types: 
manifesting generator and generator compared to app.mybodygraph.com  and other bodygraph generators.

Ex date: 21 feb 1968  
- mybodygraph: manifesting generator
- human_design_engine: Generator

Ex date: 19 Jan 1973
- mybodygraph: Generator
- human_design_engine: manifesting generator

**Correction:**
- **MG / G Case:** 
	- Sacral is defined (can be Generator or Manifesting Generator)
		- SC==true

- **Manifesting Generator**=>Check connections from motor centers to throat
	- HT==TT | EM==TT |  RT==TT |  SC == TT 

- **Generator**=> No connection to throat
-------------------------------------------
## Addition
- Test.py added for testing
- display func changed with print

## Supported Features
### Calculations of single features
- Basic values from planetary positions
	- longitude
	- gate
	- line
	- color
	- tone
	- base
- profile
- inner authority
- typ
- active chakras
- active channels
- split
- variables

### Calculations of composite features
- composite channels
- composite chakras

### Calculations of mutliple instances
Based on a list of birth times, for each birth time all single features are calculated

## Examples
### Single instance calculations
  ```python
  import hd_features as hd
  import hd_constants

	#examples for birth time format
	zone = 'Europe/Berlin'
	birth_time= 1876,1,5,10,2,4 #konrad adenauer
	zone = 'Asia/Shanghai'
	birth_time= 1935,7,6,4,48,0 #dalai lama

	#automatic timezone(tz) offset calculation (for all avl. timezones see pytz.all_timezones)
	hours = hd.get_utc_offset_from_tz(birth_time,zone)

	##manual time_zone offset calculation
	hours=8

	timestamp = tuple(list(birth_time) + [hours])
	single_result = hd.calc_single_hd_features(timestamp,report=True,channel_meaning=True)
  ```
### Composite instance calculations
  ```python
	hours=2 #time_zone offset
	#define persons you want to combine
	persons_dict = {"1":(1990,1,30,1,2,0,hours),
                   "2":(2010,2,30,1,2,0,hours),
                   "3":(2020,6,30,1,2,0,hours),
				           }
	#composite channels and chakras
	hd.get_composite_combinations(persons_dict)
	#full view, with readable meanings
	hd.get_composite_combinations(persons_dict).explode(["new_channels","new_ch_meaning"])
	#composite gates matching penta 
	hd.get_penta(persons_dict)
  ```
### Multiple instance calculations
  ```python
	start_date = 1781-30,1,1,1,1
	end_date = 2027+30, 12, 31,23,1
	percentage = 1 #percentage of processed list (1=100%,0=0%)
	time_unit = "days" #years,months,days,hours,minutes are supported
	intervall = 10 #every X unit, note gates changing every ~5 days, lines every 0.9 day
	num_cpu = 6
	result,timestamp_list = hd.calc_mult_hd_features(
							start_date,end_date,percentage,time_unit,intervall,num_cpu)
	result_lists = hd.unpack_mult_features(result,full=True) #lists are structured as dict

	#Example for simple "Typ"-distribution
	typ_dist = pd.Series(result_lists["typ_list"]).value_counts()/len(result_lists["typ_list"])
	labels=typ_dist.index
    plt.pie(typ_dist,labels=labels,autopct='%1.1f%%',startangle=90);
  ```
  ![Result](https://github.com/MicFell/human_design_engine/blob/main/result.png)
