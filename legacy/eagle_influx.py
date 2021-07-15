#!/usr/bin/python3
from influxdb import InfluxDBClient
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

def cmdT(type_in, time1, time2, host):
	string = """SELECT value FROM "collectd-sv.plugin_value" WHERE host=\'{}\' AND type_instance=\'{}\' AND time > '{}' AND time < '{}';""".format(host,type_in,time1,time2)
	return string

def weather_get(time1, time2, host = '192.168.10.8', interval='1min'):
	client = InfluxDBClient(host = 'eagle.sai.msu.ru', port=80)

	# def cmdT(type_in,dtime,host):
	# 	string = 'SELECT value FROM "collectd-sv.plugin_value" WHERE host=\'{}\' AND type_instance=\'{}\' AND time > now() - {};'.format(host,type_in,dtime)
	# 	return string

	def cmd(time1,time2,host):#2021-01-01T00:00:00Z
		string = """SELECT value,type_instance FROM "collectd-sv.plugin_value" WHERE host='{}' AND time >= '{}' AND time < '{}';""".format(host,time1,time2)
		return string

	data = client.query(cmd(time1, time2, host), database='collectd').get_points()
	result = pd.DataFrame(data)
	result = result.set_index(pd.DatetimeIndex(result['time'])).drop(columns='time')
	groups = result.groupby('type_instance')
	result = groups.apply(lambda g:g.resample(interval).mean().rename(columns={'value':g.name})) 
	result.index = result.index.droplevel(0)
	result = result.groupby(result.index).mean()
	result = result.tz_convert('Europe/Moscow')

	return result

def get_wdata(time1,time2):
    data = weather_get(time1,time2)

    # Другая темпратура неба
    dtime='10h'
    client = InfluxDBClient(host='eagle.sai.msu.ru', port=80)
    asm_t = client.query(cmdT('TEMP_SKY', time1, time2, '192.168.10.5'), database='collectd').get_points()
    dfA = pd.DataFrame(asm_t)
    dfA = dfA.set_index(pd.DatetimeIndex(dfA['time'])).drop(columns='time')
    dfA = dfA.rename(columns={'value' : 'TEMP_SKY'} )
    dfA = dfA.tz_convert('Europe/Moscow')
    data = data.join(dfA.resample('1min').mean(), how = 'outer')
    return data


# t_start = datetime.datetime(2020,11,30,0,0,0)
# t_start = datetime.datetime(2021,4,13,0,0,0)
# ttt=time.time()
# dt = datetime.timedelta(days=1)
# t_end = t_start + dt
# t_data = get_wdata(t_start.isoformat()+'Z',t_end.isoformat()+'Z')
# t_start += dt

# while t_start<datetime.datetime.now():
#     t_end = t_start + dt
#     print(t_start.isoformat()+'Z',t_end.isoformat()+'Z')
#     print(time.time()-ttt)
#     t_data = pd.concat([t_data,get_wdata(t_start.isoformat()+'Z',t_end.isoformat()+'Z') ])
#     t_data.to_pickle("all_data.pkl")
#     time.sleep(5)
#     t_start += dt

data  = pd.read_pickle('temperature/all_data.pkl')
plt.plot(data.index, data['TEMP_SKY'], 'o', markersize = 0.1)
plt.show()

# flist = glob.glob('/mnt/d/sci_tmp/irmaps/*2021*.fits')
 
# dates_list = np.array(list(map(lambda s: pd.Timestamp(datetime.datetime.strptime(s.split('/')[-1][:-12],r'MAP%Y-%m-%dT%H-%M'),tz='UTC'),flist) ) )
# flist = list(map(lambda s: s.split('/')[-1],flist ) )
# fseries = pd.Series(flist,index = dates_list)

# # import collections
# # print([item for item, count in collections.Counter(dates_list).items() if count > 1])
# # print(len(dates_list),len(np.unique(dates_list) ) )	#datetime.datetime(2020, 9, 8, 19, 9)

# # print(fseries)

# data['FITS'] = fseries
# data = data.dropna()
# print(data)
# # data.to_pickle("all_data_wname.pkl")

# mask = (data['TEMP']<=1) & (data['TEMP']>0 )
# print(data[mask])