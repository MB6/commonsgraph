from requests import get, post
from json import dumps
from matplotlib import pyplot as plt
from ciso8601 import parse_datetime
from pytz import timezone
from datetime import datetime
class commonsgraph(object):
    def __init__(self):
        self.systems = get('http://commonscontrol.harleyschool.org:8000/data/api/systems/').json()
        self.system_map = {}
        self.zone = timezone('US/Eastern')
        for sys in self.systems:
            try:
                self.system_map[sys["system"]].append(sys["subsystem"])
            except KeyError:
                self.system_map[sys["system"]] = [sys['subsystem']]
    def graph(self, payload):
        req = post("http://commonscontrol.harleyschool.org:8000/data/api/series/", data=dumps(payload)).json()
        for series in req:
            data = series['data']
            dates = [self.zone.normalize(parse_datetime(point["Time"])) for point in data]
            cols = [key for key in data[0] if key != "Time"]
            for col in cols:
                if series["index"]:
                    label = "%s %s %s" % (series['index'], series['subsystem'], col)
                else:
                    label = "%s %s" % (series['subsystem'], col)
                plt.plot(dates, [point[col] for point in data], label=label)
            plt.gcf().autofmt_xdate()
            plt.legend(loc=0, fontsize=12, fancybox=True)
            plt.show()
    def ret_service_dict(self, sys, subsys):
        for sysd in self.systems:
            if sysd['system'] == sys and sysd['subsystem'] == subsys:
                return sysd
        else:
            raise ValueError("No system/subsystem pair with giver perameters")
    def graph_one(self, start_timestamp, end_timestamp, payload_list):
        series = []
        payload = {"from": parse_datetime(start_timestamp).isoformat(),
            "to":parse_datetime(end_timestamp).isoformat(),
            "temporary":False,
            "averages":True,
            }
        for sys, subsys, col, idx in payload_list:
            for s in series:
                if s['system'] == sys and s['subsystem'] == subsys:
                    if col:
                        if col not in s['columns']:
                            s['columns'].append(col)
                    else:
                        raise ValueError('Need a column')
                    if idx:
                        if idx not in s['indexes']:
                            s['indexes'].append(idx)
                    break
            else:
                if idx:
                    idx = [idx]
                else:
                    idx = []
                series.append({'system':sys, 'subsystem':subsys, 'columns':[col], 'indexes':idx})
        payload["series"] = series
        print payload
        self.graph(payload)


if __name__ == "__main__":
    g = commonsgraph()
    g.graph()
