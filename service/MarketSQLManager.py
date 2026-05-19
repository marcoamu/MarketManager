import configparser
import sqlite3
from datetime import datetime
import pandas as pd

import datetime

class MarketSQLManager:

    # def __init__(self):
    #     self.name = None
    #     self.url = None
    #     self.eth_min_val
    #     self.results = list()


    def __init__(self, simulation = False):
        print("inicializando")
        config = configparser.ConfigParser()
        config.read('config.ini')
        sqliteConnection = ""
        try:
            self.env = config['DEFAULT']['DEF_CONF']
        except Exception as e:
            import platform
            sistema = platform.system()
            if sistema == "Windows":
                self.env = "WINDOWS"
            else:
                print("Error defaut LINUX MarketSQLManager")
                self.env = "LINUX"

        # print(f"Active env : {self.env}")
        path = "/home/MarketManager/market.db"
        if "WINDOWS" in self.env:
            path = "F:\\WORK\\2026\\MarketManager\\market.db"
            simpath = "F:\WORK\2026\MarketManager\marketSimulation.db"
            if simulation:
                path = "F:\WORK\2026\MarketManager\marketSimulation.db"

        else:
            path = "/home/MarketManager/market.db"
            simpath = "/home/MarketManager/marketSimulation.db"
            if simulation:
                path = "/home/MarketManager/marketSimulation.db"

        self.db = path
        self.dbSim = simpath
        # self.db = "/home/selenium/market.db"
        # self.db = "/home/pi/PYTHON/axie/market.db"

    def getValueWithID(self, id):
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE from MARKET where id = ?"""
            cursor.execute(sqlite_select_query, (id,))
            records = cursor.fetchall()
            res = list()
            for row in records:
                result = {}
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                result["id"] = id
                result["name"]=name
                result["datevalue"]= datevalue
                result["value"]=value
                result["lastValue"]=lastValue
                result["lastdif"]=lastdif
                result["acumulate"]=acumulate
                res.append(result)


            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 1", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

        return res

    def insert_indicator_snapshot(
            self,
            symbol,
            indicators: dict,
            signals: dict,
            dateValue=None
    ):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()

            if dateValue is None:
                dateValue = datetime.datetime.utcnow().isoformat()

            sqlite_insert_with_param = """
                                       INSERT INTO indicator_snapshots (ts, \
                                                                        symbol, \
                                                                        price, \
                                                                        momentum_5, \
                                                                        momentum_15, \
                                                                        velocity, \
                                                                        acceleration, \
                                                                        volume, \
                                                                        volume_rel, \
                                                                        range_high, \
                                                                        range_low, \
                                                                        breakout_up, \
                                                                        breakout_down, \
                                                                        volume_spike, \
                                                                        signal_score, \
                                                                        alert_triggered, \
                                                                        alert_type)
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); \
                                       """

            data_tuple = (
                dateValue,
                symbol,

                indicators.get('price'),
                indicators.get('momentum_5'),
                indicators.get('momentum_15'),
                indicators.get('velocity'),
                indicators.get('acceleration'),

                indicators.get('volume'),
                indicators.get('volume_rel'),

                indicators.get('range_high'),
                indicators.get('range_low'),

                signals.get('breakout_up'),
                signals.get('breakout_down'),
                signals.get('volume_spike'),

                signals.get('signal_score'),
                signals.get('alert_triggered'),
                signals.get('alert_type')
            )

            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("❌ Error while working with SQLite (indicator_snapshots):", error)

        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def getLastValueWithName(self, name):
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, max(DATEVALUE), VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE, 
            TENDENCE_COUNT, TENDENCE_ACU, MIN_VALUE, MAX_VALUE, MIN_ACU, MAX_ACU, ACTION, 
            DIRECTION, MIN_DIR, MAX_DIR, INDI_DIR, MOTION_MIN, MOTION_MAX, GLOBAL_MIN,GLOBAL_MAX, ACTION_COUNT, ACTION_ACUM,
            WEEK_FLOW, WEEK_FLOW_STD, WEEK_FLOW_MED, REl_FCST, REl_FCST_STD, REl_FCST_MED, REl_FCST_MIN, REl_FCST_MAX, REl_FCST_PERCENT,
            CLOSE_NXT_UP, CLOSE_NXT_DOWN, CLOSE_NXT_MIDDLE, WEEK_DIR, WEEK_MIN_DIR, WEEK_MAX_DIR,WEEK_DIR_FLOW, ANGLE_IMA, ANGLE_IMA_COUNTER, ANGLE,ANGLE_COUNTER, 
            MONTH_DIR_BOT_DST, WEEK_DIR_BOT_DST, WEEK_DIR_BOT_DST_NEW, OPENVALUE, QTY, PROTECT
            from MARKET where name = ? """
            cursor.execute(sqlite_select_query, (name,))
            records = cursor.fetchall()
            res = list()
            for row in records:
                result = {}
                id = row[0]
                if id is None:
                    return None
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence = row[7]
                tendence_count = row[8]
                tendence_acu = row[9]
                min_value = row[10]
                max_value = row[11]
                min_acu = row[12]
                max_acu = row[13]
                action = row[14]
                direction = row[15]
                min_dir = row[16]
                max_dir = row[17]
                indi_dir = row[18]
                motion_min = row[19]
                motion_max = row[20]
                global_min = row[21]
                global_max = row[22]
                action_count = row[23]
                action_acum = row[24]
                week_flow = row[25]
                week_flow_std = row[26]
                week_flow_med = row[27]
                rel_fcst = row[28]
                rel_fcst_std = row[29]
                rel_fcst_med = row[30]
                rel_fcst_min = row[31]
                rel_fcst_max = row[32]
                rel_fcst_percent = row[33]
                close_nxt_up = row[34]
                close_nxt_down = row[35]
                close_nxt_middle = row[36]
                week_dir = row[37]
                week_min_dir = row[38]
                week_max_dir = row[39]
                week_dir_flow = row[40]
                angle_ima = row[41]
                angle_ima_counter = row[42]
                angle = row[43]
                angle_counter = row[44]
                month_dir_bot_dst = row[45]
                week_dir_bot_dst = row[46]
                week_dir_bot_dst_new = row[47]
                openvalue = row[48]
                qty = row[49]
                protect = row[50]
                result["id"] = id
                result["name"]=name
                result["datevalue"]= datevalue
                result["value"]=value
                result["lastValue"]=lastValue
                result["lastdif"]=lastdif
                result["acumulate"]=acumulate
                result["tendence"]=tendence
                result["tendence_count"]=tendence_count
                result["tendence_acu"]=tendence_acu
                result["min_value"]=min_value
                result["max_value"]=max_value
                result["min_acu"]=min_acu
                result["max_acu"]=max_acu
                result["action"]=action
                result["direction"]=direction
                result["min_dir"]=min_dir
                result["max_dir"]=max_dir
                result["indi_dir"]=indi_dir
                result["motion_min"]=motion_min
                result["motion_max"]=motion_max
                result["global_min"] = global_min
                result["global_max"] = global_max
                result["action_count"] = action_count
                result["action_acum"] = action_acum
                result["week_flow"] = week_flow
                result["week_flow_std"] = week_flow_std
                result["week_flow_med"] = week_flow_med
                result["rel_fcst"] = rel_fcst
                result["rel_fcst_std"] = rel_fcst_std
                result["rel_fcst_med"] = rel_fcst_med
                result["rel_fcst_min"] = rel_fcst_min
                result["rel_fcst_max"] = rel_fcst_max
                result["rel_fcst_percent"] = rel_fcst_percent
                result["close_nxt_up"] = close_nxt_up
                result["close_nxt_down"] = close_nxt_down
                result["close_nxt_middle"] = close_nxt_middle
                result["week_dir"] = week_dir
                result["week_min_dir"] = week_min_dir
                result["week_max_dir"] = week_max_dir
                result["week_dir_flow"] = week_dir_flow
                result["angle_ima"] = angle_ima
                result["angle_ima_counter"] = angle_ima_counter
                result["angle"] = angle
                result["angle_counter"] = angle_counter

                result["month_dir_bot_dst"] = month_dir_bot_dst
                result["week_dir_bot_dst"] = week_dir_bot_dst
                result["week_dir_bot_dst_new"] = week_dir_bot_dst_new
                result["openValue"] = openvalue
                result["qty"] = qty
                result["protect"] = protect

                res.append(result)
                # print(
                #     f" valores recuperados id: {id} Name: {name} DateValue: {datevalue} Value: {value} "
                #     f"LastValue: {lastValue} LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} "
                #     f"tendence_count  {tendence_count} min_value {min_value} max_value {max_value} min_acu {min_acu} max_acu {max_acu}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error getLastValueWithName while working with SQLite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

        return res

    def getAll(self):
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE from MARKET"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                # print("id: ",id)
                # print("name: ",name)
                # print("datevalue: ", datevalue)
                # print("value: ",value)
                # print("lastValue: ",lastValue)
                # print("lastdif: ",lastdif)
                # print("acumulate: ",acumulate)
                # print("")

                print(f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} LastDif: {lastdif} Accumulate: {acumulate}" )


            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 2", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

    def getAllWithNameForXdays(self, name, days):
        sqliteConnection = None
        ids = []
        dates = []
        values = []
        actions = []
        change_actions = []
        eval_names = []
        data = {}
        try:

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            # days = days-1
            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT, MIN_VALUE, MAX_VALUE, MIN_ACU, MAX_ACU, ACTION, CHANGE_ACTION, EVAL_NAME from MARKET where name =? and datevalue > date( julianday(date('now'))-?)"""
            data_tuple = (name, days)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                min_value = row[9]
                max_value = row[10]
                min_acu = row[11]
                max_acu = row[12]
                action = row[13]
                change_action = row[14]
                eval_name = row[15]
                ids.append(id)
                dates.append(datevalue)
                values.append(value)
                actions.append(action)
                change_actions.append(change_action)
                eval_names.append(eval_name)

                # print(
                #     f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} "
                #     f"LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} "
                #     f"tendence_count {tendence_count} min_value {min_value} max_value {max_value} min_acu {min_acu} max_acu {max_acu}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 3", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")


            data["date"]=dates
            data["value"] = values
            data["action"] = actions
            data["change_action"] = change_actions
            data["eval_name"] = eval_names
            data["id"] = ids
            df = pd.DataFrame(data)

            return df

    def getAllWithNameForXdaysSpecial(self, name, days):
        sqliteConnection = None
        dates = []
        values = []
        actions = []
        global_max = []
        relative_min = []
        relative_max = []
        global_min = []
        week_flows = []
        week_flow_stds = []
        week_flow_meds = []
        rel_fcsts = []
        rel_fcst_stds = []
        rel_fcst_meds = []
        rel_fcst_mins = []
        rel_fcst_maxs = []
        rel_fcst_percents = []
        close_nxt_ups = []
        close_nxt_downs = []
        change_actions = []
        data = {}
        week_dirs = []
        week_min_dirs = []
        week_max_dirs = []
        month_dir_bot_dsts = []
        week_dir_bot_dsts = []
        week_dir_bot_dst_news = []

        opens = []
        profits = []
        qtys = []
        protects = []

        sqliteConnection= None
        try:

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            # days = days-1
            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT, 
            MIN_VALUE, MAX_VALUE, MIN_ACU, MAX_ACU, ACTION, CHANGE_ACTION, GLOBAL_MIN, GLOBAL_MAX, MOTION_MIN, MOTION_MAX,
            WEEK_FLOW, WEEK_FLOW_STD, WEEK_FLOW_MED, REL_FCST, REL_FCST_STD,REL_FCST_MED, REL_FCST_MIN, REL_FCST_MAX, REL_FCST_PERCENT, 
            CLOSE_NXT_UP, CLOSE_NXT_DOWN, WEEK_DIR, WEEK_MIN_DIR, WEEK_MAX_DIR,MONTH_DIR_BOT_DST, WEEK_DIR_BOT_DST, WEEK_DIR_BOT_DST_NEW, PROFIT, OPENVALUE, QTY, PROTECT
            from MARKET where name =? and datevalue > date( julianday(date('now'))-?)"""
            data_tuple = (name, days)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                min_value = row[9]
                max_value = row[10]
                min_acu = row[11]
                max_acu = row[12]
                action = row[13]
                change_action = row[14]
                glob_min = row[15]
                glob_max = row[16]
                mot_min = row[17]
                mot_max = row[18]
                week_flow = row[19]
                week_flow_std = row[20]
                week_flow_med = row[21]
                rel_fcst = row[22]
                rel_fcst_std = row[23]
                rel_fcst_med = row[24]
                rel_fcst_min = row[25]
                rel_fcst_max = row[26]
                rel_fcst_percent = row[27]
                close_nxt_up = row[28]
                close_nxt_down = row[29]
                week_dir = row[30]
                week_min_dir = row[31]
                week_max_dir = row[32]
                month_dir_bot_dst = row[33]
                week_dir_bot_dst = row[34]
                week_dir_bot_dst_new = row[35]

                profit = row[36]
                open = row[37]
                qty = row[38]
                protect = row[39]
                dates.append(datevalue)
                values.append(value)
                actions.append(action)
                change_actions.append(change_action)
                global_min.append(glob_min)
                global_max.append(glob_max)
                relative_min.append(mot_min)
                relative_max.append(mot_max)
                week_flows.append(week_flow)
                week_flow_stds.append(week_flow_std)
                week_flow_meds.append(week_flow_med)
                rel_fcsts.append(rel_fcst)
                rel_fcst_stds.append(rel_fcst_std)
                rel_fcst_meds.append(rel_fcst_med)
                rel_fcst_mins.append(rel_fcst_min)
                rel_fcst_maxs.append(rel_fcst_max)
                rel_fcst_percents.append(rel_fcst_percent)
                close_nxt_ups.append(close_nxt_up)
                close_nxt_downs.append(close_nxt_down)
                week_dirs.append(week_dir)
                week_min_dirs.append(week_min_dir)
                week_max_dirs.append(week_max_dir)

                month_dir_bot_dsts.append(month_dir_bot_dst)
                week_dir_bot_dsts.append(week_dir_bot_dst)
                week_dir_bot_dst_news.append(week_dir_bot_dst_new)

                profits.append(profit)
                opens.append(open)
                qtys.append(qty)
                protects.append(protect)
                # print(
                #     f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} "
                #     f"LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} "
                #     f"tendence_count {tendence_count} min_value {min_value} max_value {max_value} min_acu {min_acu} max_acu {max_acu}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 4", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            data["date"]=dates
            data["value"] = values
            data["action"] = actions
            data["change_action"] = change_actions
            data["global_min"] = global_min
            data["global_max"] = global_max
            data["relative_min"] = relative_min
            data["week_flow"] = week_flows
            data["week_flow_std"] = week_flow_stds
            data["week_flow_med"] = week_flow_meds
            data["rel_fcst"] = rel_fcsts
            data["rel_fcst_std"] = rel_fcst_stds
            data["rel_fcst_med"] = rel_fcst_meds
            data["rel_fcst_min"] = rel_fcst_mins
            data["rel_fcst_max"] = rel_fcst_maxs
            data["relative_max"] = relative_max
            data["rel_fcst_percent"] = rel_fcst_percents
            data["close_nxt_up"] = close_nxt_ups
            data["close_nxt_down"] = close_nxt_downs
            data["week_dir"] = week_dirs
            data["week_min_dir"] = week_min_dirs
            data["week_max_dir"] = week_max_dirs
            data["month_dir_bot_dst"] = month_dir_bot_dsts
            data["week_dir_bot_dst"] = week_dir_bot_dsts
            data["week_dir_bot_dst_new"] = week_dir_bot_dst_news

            data["profit"] = profits
            data["open"] = opens
            data["qty"] = qtys
            data["protect"] = protects
            df = pd.DataFrame(data)

            return df


    def getAllWithNameForXdaysRangeDatesExactdays(self, name, start, end):
        sqliteConnection = None
        dates = []
        values = []
        actions = []
        global_max = []
        relative_min = []
        relative_max = []
        global_min = []
        change_actions = []
        month_dir_bot_dsts = []
        week_dir_bot_dsts = []
        week_dir_bot_dst_news = []
        data = {}


        try:

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            # days = days-1
            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT, 
            MIN_VALUE, MAX_VALUE, MIN_ACU, MAX_ACU, ACTION, CHANGE_ACTION, GLOBAL_MIN, GLOBAL_MAX, MOTION_MIN, MOTION_MAX, MONTH_DIR_BOT_DST, WEEK_DIR_BOT_DST, WEEK_DIR_BOT_DST_NEW  from MARKET where name =? and datevalue >= DATETIME( ?) and datevalue <= DATETIME( ?)"""
            data_tuple = (name, start, end)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                min_value = row[9]
                max_value = row[10]
                min_acu = row[11]
                max_acu = row[12]
                action = row[13]
                change_action = row[14]
                glob_min = row[15]
                glob_max = row[16]
                mot_min = row[17]
                mot_max = row[18]
                month_dir_bot_dst = row[19]
                week_dir_bot_dst = row[20]
                week_dir_bot_dst_new = row[21]
                dates.append(datevalue)
                values.append(value)
                actions.append(action)
                change_actions.append(change_action)
                global_min.append(glob_min)
                global_max.append(glob_max)
                relative_min.append(mot_min)
                relative_max.append(mot_max)
                month_dir_bot_dsts.append(month_dir_bot_dst)
                week_dir_bot_dsts.append(week_dir_bot_dst)
                week_dir_bot_dst_news.append(week_dir_bot_dst_new)

                # print(
                #     f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} "
                #     f"LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} "
                #     f"tendence_count {tendence_count} min_value {min_value} max_value {max_value} min_acu {min_acu} max_acu {max_acu}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 5", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            data["date"]=dates
            data["value"] = values
            data["action"] = actions
            data["change_action"] = change_actions
            data["global_min"] = global_min
            data["global_max"] = global_max
            data["relative_min"] = relative_min
            data["relative_max"] = relative_max
            data["month_dir_bot_dst"] = month_dir_bot_dsts
            data["week_dir_bot_dst"] = week_dir_bot_dsts
            data["week_dir_bot_dst_new"] = week_dir_bot_dst_news
            df = pd.DataFrame(data)

            return df

    def getAllWithNameForXdaysRangeDates(self, name, start, end):
        sqliteConnection = None
        ids = []
        dates = []
        values = []
        actions = []
        global_max = []
        relative_min = []
        relative_max = []
        global_min = []
        week_flows = []
        week_flow_stds = []
        week_flow_meds = []
        rel_fcsts = []
        rel_fcst_stds = []
        rel_fcst_meds = []
        rel_fcst_mins = []
        rel_fcst_maxs = []
        rel_fcst_percents = []
        close_nxt_ups = []
        close_nxt_downs = []
        close_nxt_middles = []
        change_actions = []
        week_dirs = []
        week_min_dirs = []
        week_max_dirs = []
        week_dir_flows = []
        angle_imas = []
        angle_ima_counters = []
        angles = []
        angle_counters = []

        month_dir_bot_dsts= []
        week_dir_bot_dsts = []
        week_dir_bot_dst_news = []
        eval_names = []
        profits = []
        openvalues = []
        qtys = []
        protects = []
        data = {}


        try:

            end_date_time = None
            #FIX para tomar end date como parte de la busqueda
            try:
                end_date_time = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as error:
                # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
                end_date_time = datetime.datetime.strptime(end, "%Y-%m-%d")

            if end_date_time:
                end_date_timeplus = end_date_time + datetime.timedelta(days=+1)
                end = end_date_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            # days = days-1
            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT, 
            MIN_VALUE, MAX_VALUE, MIN_ACU, MAX_ACU, ACTION, CHANGE_ACTION, GLOBAL_MIN, GLOBAL_MAX, MOTION_MIN, MOTION_MAX,
             WEEK_FLOW,  WEEK_FLOW_STD, WEEK_FLOW_MED, REL_FCST, REL_FCST_STD,REL_FCST_MED, REL_FCST_MIN, REL_FCST_MAX, REL_FCST_PERCENT,
             CLOSE_NXT_UP, CLOSE_NXT_DOWN, CLOSE_NXT_MIDDLE, WEEK_DIR, WEEK_MIN_DIR, WEEK_MAX_DIR, WEEK_DIR_FLOW, ANGLE_IMA, ANGLE_IMA_COUNTER, ANGLE, ANGLE_COUNTER,
             MONTH_DIR_BOT_DST,WEEK_DIR_BOT_DST,WEEK_DIR_BOT_DST_NEW, EVAL_NAME, PROFIT, OPENVALUE, QTY, PROTECT
             from MARKET where name =? and datevalue >= DATETIME( ?) and datevalue <= DATETIME( ?)"""
            data_tuple = (name, start, end)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                min_value = row[9]
                max_value = row[10]
                min_acu = row[11]
                max_acu = row[12]
                action = row[13]
                change_action = row[14]
                glob_min = row[15]
                glob_max = row[16]
                mot_min = row[17]
                mot_max = row[18]
                week_flow = row[19]
                week_flow_std = row[20]
                week_flow_med = row[21]
                rel_fcst = row[22]
                rel_fcst_std = row[23]
                rel_fcst_med = row[24]
                rel_fcst_min = row[25]
                rel_fcst_max = row[26]
                rel_fcst_percent = row[27]
                close_nxt_up = row[28]
                close_nxt_down = row[29]
                close_nxt_middle = row[30]
                week_dir = row[31]
                week_min_dir = row[32]
                week_max_dir = row[33]
                week_dir_flow = row[34]
                angle_ima = row[35]
                angle_ima_counter = row[36]
                angle = row[37]
                angle_counter = row[38]
                month_dir_bot_dst = row[39]
                week_dir_bot_dst = row[40]
                week_dir_bot_dst_new = row[41]
                eval_name = row[42]

                profit = row[43]
                openvalue = row[44]
                qty = row[45]
                protect = row[46]

                dates.append(datevalue)
                values.append(value)
                actions.append(action)
                change_actions.append(change_action)
                global_min.append(glob_min)
                global_max.append(glob_max)
                relative_min.append(mot_min)
                relative_max.append(mot_max)
                week_flows.append(week_flow)
                week_flow_stds.append(week_flow_std)
                week_flow_meds.append(week_flow_med)
                rel_fcsts.append(rel_fcst)
                rel_fcst_stds.append(rel_fcst_std)
                rel_fcst_meds.append(rel_fcst_med)
                rel_fcst_mins.append(rel_fcst_min)
                rel_fcst_maxs.append(rel_fcst_max)
                rel_fcst_percents.append(rel_fcst_percent)
                close_nxt_ups.append(close_nxt_up)
                close_nxt_downs.append(close_nxt_down)
                close_nxt_middles.append(close_nxt_middle)
                week_dirs.append(week_dir)
                week_min_dirs.append(week_min_dir)
                week_max_dirs.append(week_max_dir)
                week_dir_flows.append(week_dir_flow)
                angle_imas.append(angle_ima)
                angle_ima_counters.append(angle_ima_counter)
                angles.append(angle)
                angle_counters.append(angle_counter)
                ids.append(id)
                month_dir_bot_dsts.append(month_dir_bot_dst)
                week_dir_bot_dsts.append(week_dir_bot_dst)
                week_dir_bot_dst_news.append(week_dir_bot_dst_new)
                eval_names.append(eval_name)

                profits.append(profit)
                openvalues.append(openvalue)
                qtys.append(qty)
                protects.append(protect)
                # print(
                #     f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} "
                #     f"LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} "
                #     f"tendence_count {tendence_count} min_value {min_value} max_value {max_value} min_acu {min_acu} max_acu {max_acu}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 6", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")


            data["date"]=dates
            data["value"] = values
            data["action"] = actions
            data["change_action"] = change_actions
            data["global_min"] = global_min
            data["global_max"] = global_max
            data["relative_min"] = relative_min
            data["week_flow"] = week_flows
            data["week_flow_std"] = week_flow_stds
            data["week_flow_med"] = week_flow_meds
            data["rel_fcst"] = rel_fcsts
            data["rel_fcst_std"] = rel_fcst_stds
            data["rel_fcst_med"] = rel_fcst_meds
            data["rel_fcst_min"] = rel_fcst_mins
            data["rel_fcst_max"] = rel_fcst_maxs
            data["relative_max"] = relative_max
            data["rel_fcst_percent"] = rel_fcst_percents
            data["close_nxt_up"] = close_nxt_ups
            data["close_nxt_down"] = close_nxt_downs
            data["close_nxt_middle"] = close_nxt_middles
            data["week_dir"] = week_dirs
            data["week_min_dir"] = week_min_dirs
            data["week_max_dir"] = week_max_dirs
            data["week_dir_flow"] = week_dir_flows
            data["angle_ima"] = angle_imas
            data["angle_ima_counter"] = angle_ima_counters
            data["angle"] = angles
            data["angle_counter"] = angle_counters
            data["id"] = ids
            data["month_dir_bot_dst"] = month_dir_bot_dsts
            data["week_dir_bot_dst"] = week_dir_bot_dsts
            data["week_dir_bot_dst_new"] = week_dir_bot_dst_news
            data["eval_name"] = eval_names

            data["profit"] = profits
            data["openvalue"] = openvalues
            data["qty"] = qtys
            data["protect"] = protects
            df = pd.DataFrame(data)

            return df

    def getMinMaxFor3days(self, name, dateValue):
        sqliteConnection = None
        dates = []
        values = []
        actions = []
        change_actions = []
        global_minList = []
        global_maxList = []
        data = {}


        try:
            start_date_time = None
            try:
                current_date_time = datetime.datetime.strptime(dateValue, "%Y-%m-%d %H:%M:%S.%f")
                # current_date = current_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                start_date_time = current_date_time + datetime.timedelta(days=-1)
                # start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                #1verificar que dia ha caido
                if start_date_time.weekday()>4:
                    days = 2
                    #ha caido un fin de semana
                    if start_date_time.weekday()==6:
                        days = 3
                    start_date_time = current_date_time + datetime.timedelta(days=-days)

                start = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

                # start_query_time = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f")



            except Exception as error:
                nada=""
                # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
                # end_date_time = datetime.datetime.strptime(end, "%Y-%m-%d")

            if start:
                end_date_timeplus = start_date_time + datetime.timedelta(days=+1)
                end = end_date_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            # days = days-1
            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT, 
            MIN_VALUE, MAX_VALUE, MIN_ACU, MAX_ACU, ACTION, CHANGE_ACTION, GLOBAL_MIN, GLOBAL_MAX from MARKET where name =? and datevalue >= DATETIME( ?) and datevalue <= DATETIME( ?)"""
            data_tuple = (name, start, end)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                min_value = row[9]
                max_value = row[10]
                min_acu = row[11]
                max_acu = row[12]
                action = row[13]
                change_action = row[14]
                global_min = row[15]
                global_max = row[16]

                dates.append(datevalue)
                values.append(value)
                actions.append(action)
                change_actions.append(change_action)
                global_minList.append(global_min)
                global_maxList.append(global_max)

                # print(
                #     f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} "
                #     f"LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} "
                #     f"tendence_count {tendence_count} min_value {min_value} max_value {max_value} min_acu {min_acu} max_acu {max_acu}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 7", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            data["date"]=dates
            data["value"] = values
            data["action"] = actions
            data["change_action"] = change_actions
            data["global_min"] = global_minList
            data["global_max"] = global_maxList
            df = pd.DataFrame(data)

            return df

    def getMinWithCountForXdays(self, name, days, count, tend_acu):
        sqliteConnection = None
        date = []
        values = []
        data = {}
        lastdif = []
        try:

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT from MARKET where name =? and datevalue > date( julianday(date('now'))-?) and tendence_count >=? and tendence_acu<=?"""
            data_tuple = (name, days, count, tend_acu)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                date.append(datevalue)
                values.append(value)

                print(
                    f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} tendence_count {tendence_count}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 8", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            data["date"] = date
            data["value"] = values
            data["LastDif"] = lastdif
            df = pd.DataFrame(data)
            df
            return df

    def getCriticsWithNameForXdays(self, name, days, value):
        sqliteConnection = None
        date = []
        values = []
        data = {}

        lastdif=[]

        try:

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT from MARKET where name =? and datevalue > date( julianday(date('now'))-?) and lastdif <=?"""
            data_tuple = (name, days, value)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                date.append(datevalue)
                values.append(value)

                print(
                    f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} tendence_count {tendence_count}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 9", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            data["date"]=date
            data["value"] = values
            data["LastDif"] = lastdif
            df = pd.DataFrame(data)
            df
            return df

    def getMaxWithNameForXdays(self, name, days, value):
        sqliteConnection = None
        date = []
        values = []
        data = {}
        lastdif=[]
        try:

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE, TENDENCE_ACU, TENDENCE_COUNT from MARKET where name =? and datevalue > date( julianday(date('now'))-?) and lastdif >=?"""
            data_tuple = (name, days, value)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]
                tendence_acu = row[7]
                tendence_count = row[8]
                date.append(datevalue)
                values.append(value)

                print(
                    f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} LastDif: {lastdif} Accumulate: {acumulate} tendence_acu {tendence_acu} tendence_count {tendence_count}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 10", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            data["date"]=date
            data["value"] = values
            data["LastDif"] = lastdif
            df = pd.DataFrame(data)
            df
            return df

    def getResumeForRangeDates(self, start, end):
        sqliteConnection = None
        dates = []
        values = []
        names = []
        data = {}

        try:

            end_date_time = None
            # FIX para tomar end date como parte de la busqueda
            try:
                end_date_time = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as error:
                # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
                end_date_time = datetime.datetime.strptime(end, "%Y-%m-%d")

            if end_date_time:
                end_date_timeplus = end_date_time + datetime.timedelta(days=+1)
                end = end_date_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")

            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            # days = days-1
            # get developer detail
            sqlite_select_query = """SELECT SUM(profit), NAME from MARKET where datevalue >= DATETIME( ?) and datevalue <= DATETIME( ?) and action='CLOSE' group by name order by sum(profit) asc"""
            data_tuple = (start, end)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                value = row[0]
                name = row[1]

                # dates.append(datevalue)
                values.append(value)
                names.append(name)


            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 11", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            # data["date"] = dates
            data["value"] = values
            data["name"] = names

            df = pd.DataFrame(data)

            return df

    def getResumeForRangeDatesExact(self, start, end):
        sqliteConnection = None
        dates = []
        values = []
        names = []
        data = {}

        try:


            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            # days = days-1
            # get developer detail
            sqlite_select_query = """SELECT SUM(profit), NAME from MARKET where datevalue >= DATETIME( ?) and datevalue <= DATETIME( ?) and action='CLOSE' group by name order by sum(profit) asc"""
            data_tuple = (start, end)
            cursor.execute(sqlite_select_query, data_tuple)
            records = cursor.fetchall()

            for row in records:
                value = row[0]
                name = row[1]

                # dates.append(datevalue)
                values.append(value)
                names.append(name)


            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 12", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

            # data["date"] = dates
            data["value"] = values
            data["name"] = names

            df = pd.DataFrame(data)

            return df

    def getAllWithName(self,name):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, DATEVALUE, VALUE, LASTVALUE, LASTDIF, ACUMULATE from MARKET where name =?"""
            cursor.execute(sqlite_select_query,(name,))
            records = cursor.fetchall()

            for row in records:
                id = row[0]
                name = row[1]
                datevalue = row[2]
                value = row[3]
                lastValue = row[4]
                lastdif = row[5]
                acumulate = row[6]

                print(f"id: {id} Name: {name} DateValue: {datevalue} Value: {value} LastValue: {lastValue} LastDif: {lastdif} Accumulate: {acumulate}")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 13", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")



    def inserValue(self,name,value,lastvalue,lastdif,acumulate, tendence_acu, tendence_count, min_value, max_value,
                   min_acu, max_acu, direction,min_dir,max_dir,indi_dir, motion_min, motion_max,
                   global_min, global_max,action_acum,action_count,
                   week_flow,week_flow_std, week_flow_med, rel_fcst, rel_fcst_std, rel_fcst_med, rel_fcst_min, rel_fcst_max,rel_fcst_percent,
                   close_nxt_up, close_nxt_down, close_nxt_middle, week_dir, week_min_dir, week_max_dir,week_dir_flow,angle_ima, angle_ima_counter, angle, angle_counter,
                   month_dir_bot_dst, week_dir_bot_dst, week_dir_bot_dst_new, profit, open, qty, protect, revenue,
                   action="WAIT",dateValue = None):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            if dateValue is None:
                dateValue = datetime.datetime.now()

            # insert developer detail
            sqlite_insert_with_param = """INSERT INTO 'MARKET'
                                  ('NAME', 'DATEVALUE', 'VALUE', 'LASTVALUE','LASTDIF','ACUMULATE', 'TENDENCE_ACU', 
                                  'TENDENCE_COUNT', 'MIN_VALUE','MAX_VALUE', 'MIN_ACU', 'MAX_ACU', 'ACTION', 'DIRECTION',
                                   'MIN_DIR', 'MAX_DIR','INDI_DIR', 'MOTION_MIN', 'MOTION_MAX', 'GLOBAL_MIN', 'GLOBAL_MAX', 'ACTION_ACUM', 'ACTION_COUNT',
                                   'WEEK_FLOW', 'WEEK_FLOW_STD','WEEK_FLOW_MED', 'REL_FCST', 'REL_FCST_STD', 'REL_FCST_MED', 'REL_FCST_MIN', 'REL_FCST_MAX', 'REL_FCST_PERCENT',
                                   'CLOSE_NXT_UP','CLOSE_NXT_DOWN','CLOSE_NXT_MIDDLE','WEEK_DIR','WEEK_MIN_DIR','WEEK_MAX_DIR', 'WEEK_DIR_FLOW',
                                   'ANGLE_IMA', 'ANGLE_IMA_COUNTER', 'ANGLE', 'ANGLE_COUNTER','MONTH_DIR_BOT_DST', 'WEEK_DIR_BOT_DST','WEEK_DIR_BOT_DST_NEW' , 'PROFIT', 'OPENVALUE', 'QTY', 'PROTECT', 'REVENUE') 
                                  VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?, ?,?,?,?,?, ?,?);"""

            data_tuple = (name, dateValue,value,lastvalue,lastdif,acumulate, tendence_acu, tendence_count, min_value,
                          max_value, min_acu, max_acu, action, direction, min_dir, max_dir, indi_dir, motion_min, motion_max,
                          global_min, global_max, action_acum, action_count, week_flow, week_flow_std, week_flow_med, rel_fcst, rel_fcst_std,
                          rel_fcst_med, rel_fcst_min, rel_fcst_max, rel_fcst_percent, close_nxt_up, close_nxt_down,close_nxt_middle, week_dir, week_min_dir, week_max_dir, week_dir_flow,
                          angle_ima, angle_ima_counter, angle, angle_counter, month_dir_bot_dst, week_dir_bot_dst, week_dir_bot_dst_new, profit, open, qty, protect, revenue)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            # print("Developer added successfully \n")


            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 14", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()




    def updateSimulationValues(self,results):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            name = results['NAME']
            id = float(results['DBID'])
            min_value = 0
            max_value = 0
            min_acu= 0
            max_acu= 0
            # if 'ACTION_MIN' in results:
            #     min_value = results['ACTION_MIN']
            #
            # if 'ACTION_MAX' in results:
            #     max_value = results['ACTION_MAX']
            # if 'ACTION_MIN_DIST' in results:
            #     min_acu = results['ACTION_MIN_DIST']
            # if 'ACTION_MAX_DIST' in results:
            #     max_acu = results['ACTION_MAX_DIST']
            # action = results['CURRENT_ACTION']
            # action_count = results['ACTION_COUNT']
            # action_count = int(action_count) +1
            # acumulate = results['ACUMULADO']
            # tendence = results['FLUJO']
            # tendence_count = results['FLUJOCOUNT']
            # indicator = results['INDICATOR']
            # imaNew = results['IMA_NEW']
            # market_tendence = results['MARKET_TENDENCE']

            # changeAction = results['CHANGE_ACTION']
            # revenue = results['REVENUE']
            # direction = results['DIRECTION']
            # min_dir = results['MIN_DIR']
            # max_dir = results['MAX_DIR']
            # motion_min = results['RELATIVE_MIN']
            # motion_max = results['RELATIVE_MAX']
            # global_min = results['RELATIVE_PREV_MIN']
            # global_max = results['RELATIVE_PREV_MAX']
            # action_acum = results['ACTION_ACUM']
            # eval_name = results['EVAL_NAME']
            # WEEK_FLOW = results['WEEK_FLOW']
            # WEEK_FLOW_STD = results['WEEK_FLOW_STD']
            # WEEK_FLOW_MED = results['WEEK_FLOW_MED']
            # REL_FCST = results['IND_REL_FCST']
            # REL_FCST_STD = results['IND_REL_FCST_STD']
            # REL_FCST_MED = results['IND_REL_FCST_MED']
            # REL_FCST_MIN = results['IND_REL_FCST_MIN']
            # REL_FCST_MAX = results['IND_REL_FCST_MAX']
            # REL_FCST_PERCENT = results['IND_REL_FCST_PERCENT']
            # CLOSE_NXT_UP = results['CLOSE_NXT_UP']
            # CLOSE_NXT_DOWN = results['CLOSE_NXT_DOWN']
            # WEEK_DIR = results['WEEK_DIR']
            # WEEK_MIN_DIR = results['WEEK_MIN_DIR']
            # WEEK_MAX_DIR = results['WEEK_MAX_DIR']
            # WEEK_DIR_FLOW = results['WEEK_DIR_FLOW_PREV']
            # ANGLE_IMA1 = results['ANGLE_IMA1']
            # ANGLE_IMA1_COUNTER = results['ANGLE_IMA1_COUNTER']
            # ANGLE = results['ANGLE']
            # ANGLE_COUNTER = results['ANGLE_COUNTER']
            MONTH_DIR_BOT_DST = float(results.get('MONTH_DIR_BOT_DST', 0))
            WEEK_DIR_BOT_DST = float(results.get('WEEK_DIR_BOT_DST', 0))
            WEEK_DIR_BOT_DST_NEW = float(results.get('WEEK_DIR_BOT_DST_NEW', 0))

            # Informacion de depuracion
            print(f"Intentando actualizar registro con ID: {id}")
            print(
                f"MONTH_DIR_BOT_DST: {MONTH_DIR_BOT_DST}, WEEK_DIR_BOT_DST: {WEEK_DIR_BOT_DST}, WEEK_DIR_BOT_DST_NEW: {WEEK_DIR_BOT_DST_NEW}")

            # Ejecutar consulta
            sqlite_update_with_param = """UPDATE MARKET 
                       SET MONTH_DIR_BOT_DST = ?, WEEK_DIR_BOT_DST = ?, WEEK_DIR_BOT_DST_NEW = ? 
                       WHERE ID = ?"""
            data_tuple = (MONTH_DIR_BOT_DST, WEEK_DIR_BOT_DST, WEEK_DIR_BOT_DST_NEW, id)
            cursor.execute(sqlite_update_with_param, data_tuple)
            sqliteConnection.commit()

            # Verificar filas afectadas
            if cursor.rowcount == 0:
                print(f"No rows updated for ID {id}. Please verify the record exists.")
            else:
                print(f"Successfully updated record with ID {id}.")

            cursor.close()

        except sqlite3.Error as error:
            print("Error inserValueWithData while working with SQLite", error)
        finally:
            if cursor:
                cursor.close()
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")

    def updateValueWithData(self,results):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            name = results['NAME']
            min_value = 0
            max_value = 0
            min_acu= 0
            max_acu= 0
            if 'ACTION_MIN' in results:
                min_value = results['ACTION_MIN']

            if 'ACTION_MAX' in results:
                max_value = results['ACTION_MAX']
            if 'ACTION_MIN_DIST' in results:
                min_acu = results['ACTION_MIN_DIST']
            if 'ACTION_MAX_DIST' in results:
                max_acu = results['ACTION_MAX_DIST']
            action = results['CURRENT_ACTION']
            action_count = results['ACTION_COUNT']
            action_count = int(action_count) +1
            acumulate = results['ACUMULADO']
            tendence = results['FLUJO']
            tendence_count = results['FLUJOCOUNT']
            indicator = results['INDICATOR']
            imaNew = results['IMA_NEW']
            market_tendence = results['MARKET_TENDENCE']
            id = results['DBID']
            changeAction = results['CHANGE_ACTION']
            revenue = results['REVENUE']
            direction = results['DIRECTION']
            min_dir = results['MIN_DIR']
            max_dir = results['MAX_DIR']
            motion_min = results['RELATIVE_MIN']
            motion_max = results['RELATIVE_MAX']
            global_min = results['RELATIVE_PREV_MIN']
            global_max = results['RELATIVE_PREV_MAX']
            action_acum = results['ACTION_ACUM']
            eval_name = results['EVAL_NAME']
            WEEK_FLOW = results['WEEK_FLOW']
            WEEK_FLOW_STD = results['WEEK_FLOW_STD']
            WEEK_FLOW_MED = results['WEEK_FLOW_MED']
            REL_FCST = results['IND_REL_FCST']
            REL_FCST_STD = results['IND_REL_FCST_STD']
            REL_FCST_MED = results['IND_REL_FCST_MED']
            REL_FCST_MIN = results['IND_REL_FCST_MIN']
            REL_FCST_MAX = results['IND_REL_FCST_MAX']
            REL_FCST_PERCENT = results['IND_REL_FCST_PERCENT']
            CLOSE_NXT_UP = results['CLOSE_NXT_UP']
            CLOSE_NXT_DOWN = results['CLOSE_NXT_DOWN']
            WEEK_DIR = results['WEEK_DIR']
            WEEK_MIN_DIR = results['WEEK_MIN_DIR']
            WEEK_MAX_DIR = results['WEEK_MAX_DIR']
            WEEK_DIR_FLOW = results['WEEK_DIR_FLOW_PREV']
            ANGLE_IMA1 = results['ANGLE_IMA1']
            ANGLE_IMA1_COUNTER = results['ANGLE_IMA1_COUNTER']
            ANGLE = results['ANGLE']
            ANGLE_COUNTER = results['ANGLE_COUNTER']

            MONTH_DIR_BOT_DST = results['MONTH_DIR_BOT_DST']
            WEEK_DIR_BOT_DST = results['WEEK_DIR_BOT_DST']
            WEEK_DIR_BOT_DST_NEW = results['WEEK_DIR_BOT_DST_NEW']
            PROFIT = results['PROFIT']
            PROTECT = results['PROTECT']


            # insert developer detail
            # sqlite_update_with_param = """UPDATE MARKET SET NAME= ?, DATEVALUE=?, VALUE=?, LASTVALUE=?,'LASTDIF','ACUMULATE', 'TENDENCE_ACU', 'TENDENCE_COUNT', 'MIN_VALUE','MAX_VALUE', 'MIN_ACU', 'MAX_ACU', 'ACTION')
            #                       WHERE ID =?"""

            sqlite_update_with_param = """UPDATE MARKET SET MIN_VALUE=?, MAX_VALUE=?,MIN_ACU=?, MAX_ACU=?,ACTION =?, 
            ACUMULATE=?, TENDENCE=?,TENDENCE_COUNT=?,
            INDICATOR=?, IMA_NEW=?,MARKET_TENDENCE=?, CHANGE_ACTION =?, REVENUE =?, DIRECTION =?, MIN_DIR=?, MAX_DIR =?, 
            MOTION_MIN=?, MOTION_MAX=?, GLOBAL_MIN=?, GLOBAL_MAX=?, ACTION_COUNT=?, ACTION_ACUM=?, EVAL_NAME=?,
            WEEK_FLOW=?, WEEK_FLOW_STD=?, WEEK_FLOW_MED=?, REL_FCST=?, REL_FCST_STD=?, REL_FCST_MED=?, REL_FCST_MIN=?, REL_FCST_MAX=?, REL_FCST_PERCENT=?,
            CLOSE_NXT_UP=?,CLOSE_NXT_DOWN=?, WEEK_DIR=?, WEEK_MIN_DIR=?,WEEK_MAX_DIR=?, WEEK_DIR_FLOW=?, ANGLE_IMA=?, ANGLE_IMA_COUNTER=?, ANGLE=?, ANGLE_COUNTER=?, MONTH_DIR_BOT_DST=?,WEEK_DIR_BOT_DST=?,WEEK_DIR_BOT_DST_NEW=?,PROTECT=?, PROFIT=?
            WHERE ID =?"""

            data_tuple = (min_value, max_value, min_acu, max_acu, action, acumulate,tendence, tendence_count,indicator,
                          imaNew,market_tendence, changeAction,revenue, direction,min_dir, max_dir, motion_min, motion_max,
                          global_min, global_max,action_count, action_acum, eval_name,
                          WEEK_FLOW, WEEK_FLOW_STD, WEEK_FLOW_MED, REL_FCST, REL_FCST_STD, REL_FCST_MED, REL_FCST_MIN, REL_FCST_MAX, REL_FCST_PERCENT,
                          CLOSE_NXT_UP, CLOSE_NXT_DOWN, WEEK_DIR, WEEK_MIN_DIR,WEEK_MAX_DIR,WEEK_DIR_FLOW,ANGLE_IMA1, ANGLE_IMA1_COUNTER,ANGLE, ANGLE_COUNTER,MONTH_DIR_BOT_DST, WEEK_DIR_BOT_DST, WEEK_DIR_BOT_DST_NEW, PROTECT, PROFIT,
                          id )
            cursor.execute(sqlite_update_with_param, data_tuple)
            sqliteConnection.commit()
            # print("Developer added successfully \n")


            # cursor.close()

        except sqlite3.Error as error:
            print("Error inserValueWithData while working with SQLite", error)
        finally:
            if cursor:
                cursor.close()
                # print("sqlite connection is closed")



    ##CONTROL
    def updateControls(self,ids):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """UPDATE CONTROL SET ACTIVE = 0 WHERE ID =?"""
            cursor.execute(sqlite_select_query, ids)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print("Error in updateControls  with SQLite", error)
        finally:
            if cursor:
                cursor.close()
                # print("sqlite connection is closed")

    ##CONTROL
    def updateIntervalForActive(self, activename, interval, counter):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """UPDATE CONTROLTIME SET interval = ?, counter=? WHERE active =?"""
            cursor.execute(sqlite_select_query, (interval, counter, activename,))
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print("Error in updateControls  with SQLite", error)
        finally:
            if cursor:
                cursor.close()
                # print("sqlite connection is closed")

    def updatePredictForActive(self, activename, initialPredict, finalPredict):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """UPDATE CONTROLTIME SET INITIALPREDICT = ?, FINALPREDICT=? WHERE active =?"""
            cursor.execute(sqlite_select_query, (initialPredict, finalPredict, activename,))
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print("Error in updateControls  with SQLite", error)
        finally:
            if cursor:
                cursor.close()
                # print("sqlite connection is closed")

    def getPredictForActive(self,activename):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            # sqlite_select_query = """"""
            # get developer detail
            sqlite_select_query = """SELECT ID, ACTIVE,FINALPREDICT, INITIALPREDICT from CONTROLTIME where active =?"""
            cursor.execute(sqlite_select_query, (activename,))
            records = cursor.fetchall()
            res = list()
            for row in records:
                result = {}
                id = row[0]
                active = row[1]
                finalpredict = row[2]
                initialpredict = row[3]
                result["id"] = id
                result["active"] = active
                result["finalPredict"] = finalpredict
                result["initialPredict"] = initialpredict

                res.append(result)

                # print(f"id: {id} Name: {active} Value: {value} Flujo: {flujo} Active: {active} ")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 16", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")
        return res



    def getControlValuesForName(self,name):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, NAME, VALUE, FLUJO, ACTIVE from CONTROL where name =? and ACTIVE =1"""
            cursor.execute(sqlite_select_query,(name,))
            records = cursor.fetchall()
            res = list()
            for row in records:
                result = {}
                id = row[0]
                name = row[1]
                value = row[2]
                flujo = row[3]
                active = row[4]
                result["id"] = id
                result["name"] = name
                result["value"] = value
                result["flujo"] = flujo
                result["active"] = active

                res.append(result)

                print(f"id: {id} Name: {name} Value: {value} Flujo: {flujo} Active: {active} ")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 15", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")
        return res


    def getActivesforInterval(self,interval):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            # sqlite_select_query = """"""
            cursor.execute('SELECT ID, ACTIVE, INTERVAL from CONTROLTIME where interval IN (%s)' % ','.join('?'*len(interval)), interval)
            records = cursor.fetchall()
            res = list()
            for row in records:
                result = {}
                id = row[0]
                active = row[1]
                interval = row[2]
                result["id"] = id
                result["active"] = active
                result["interval"] = interval

                res.append(result)

                # print(f"id: {id} Name: {active} Value: {value} Flujo: {flujo} Active: {active} ")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 16", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")
        return res

    def getALLActivesControlTime(self):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            sqlite_select_query = """SELECT ID, ACTIVE, INTERVAL, COUNTER, INITIAL from CONTROLTIME"""
            cursor.execute(sqlite_select_query,())
            records = cursor.fetchall()
            res = list()
            for row in records:
                result = {}
                id = row[0]
                active = row[1]
                interval = row[2]
                counter = row[3]
                default = row[4]
                result["id"] = id
                result["active"] = active
                result["interval"] = interval
                result["counter"] = counter
                result["initial"] = default

                res.append(result)

                # print(f"id: {id} Name: {active} Value: {value} Flujo: {flujo} Active: {active} ")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 17", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")
        return res

    def getResumeForXdaysPast(self, start, days):

        end_date_time = None
        try:
            eval_date_time = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
        except Exception as error:
            # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
            eval_date_time = datetime.datetime.strptime(start, "%Y-%m-%d")

        # quitamos los segundos y milisegundos
        # eval_date_time = eval_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
        eval_date_time = eval_date_time.replace(hour=0, minute=0, second=0, microsecond=0)

        for x in range(1,days):
            end_date = eval_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            start_date_time = eval_date_time + datetime.timedelta(days=-x)
            start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

            if days > 1:
                end_date_time = eval_date_time + datetime.timedelta(days=-x + 1)
                end_date = end_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            res = self.getResumeForRangeDatesExact(start_date, end_date)
            if res is not None and len(res):
                messages = f"RESULTADOS DEL DIA {start_date}\n"
                for i in range(len(res)):
                    value =res.iloc[i]['value']
                    name =res.iloc[i]['name']
                    messages = messages + f" <b>{name}</b> : {value} \n"

                print(messages)
    def getCurrentRevenues(self):
        try:
            res = list()
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()


            # Ejecutar la consulta SQL
            cursor.execute('''
                SELECT name, value, datevalue, revenue, action, week_flow, week_flow_med, week_flow_std, tendence_count, change_action
                FROM (
                    SELECT name, value, datevalue, revenue, action, week_flow, week_flow_med, week_flow_std, tendence_count, change_action,
                           ROW_NUMBER() OVER (PARTITION BY name ORDER BY datevalue DESC) AS row_num
                    FROM MARKET
                ) AS subquery
                WHERE row_num = 1 AND action != 'CLOSE'
            ''')

            # Obtener los resultados
            results = cursor.fetchall()

            # Imprimir los resultados
            val = {}
            for row in results:

                value = row[3]
                if value is None:
                    value = 0
                val[row[0]] = value
                # res.append(val)
                print(row)

        except sqlite3.Error as error:
            print("Error while working with SQLite getCurrentRevenues", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")
        return val

    def getResumeCSVForXdaysPast(self, start, days):

        end_date_time = None
        try:
            eval_date_time = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
        except Exception as error:
            # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
            eval_date_time = datetime.datetime.strptime(start, "%Y-%m-%d")

        # quitamos los segundos y milisegundos
        # eval_date_time = eval_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
        eval_date_time = eval_date_time.replace(hour=0, minute=0, second=0, microsecond=0)

        for x in range(0,days):
            end_date = eval_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            start_date_time = eval_date_time + datetime.timedelta(days=-x)
            start_date = start_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

            if days >= 1:
                end_date_time = eval_date_time + datetime.timedelta(days=-x + 1)
                end_date = end_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            res = self.getResumeForRangeDatesExact(start_date, end_date)
            if res is not None and len(res):
                total = 0
                messages = f"RESULTADOS DEL DIA; {start_date} ;"
                actives = self.prepareList()
                for act in actives:
                    findres = res.loc[res['name'].str.contains(act)]
                    if findres.empty == False:
                        value =findres['value'].values[0]
                        name =act
                        total = total+float(value)
                        messages = messages + f" {name}; {value};"
                    else:
                        value = 0
                        name = act
                        total = total + float(value)
                        messages = messages + f" {name}; {value};"

                messages = messages + f"total:; {total}"

                print(messages)

    def getControlMinMaxForActive(self, activename):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            # get developer detail
            # sqlite_select_query = """"""
            # get developer detail
            sqlite_select_query = """SELECT ID, ACTIVE,MINWEEK, MAXWEEK,MINMONTH, MAXMONTH from CONTROLMINMAX where active =?"""
            cursor.execute(sqlite_select_query, (activename,))
            records = cursor.fetchall()
            res = list()
            for row in records:
                result = {}
                id = row[0]
                active = row[1]
                minweek = row[2]
                maxweek = row[3]
                minmonth = row[4]
                maxmonth = row[5]
                result["id"] = id
                result["active"] = active
                result["minweek"] = minweek
                result["maxweek"] = maxweek
                result["minmonth"] = minmonth
                result["maxmonth"] = maxmonth

                res.append(result)

                # print(f"id: {id} Name: {active} Value: {value} Flujo: {flujo} Active: {active} ")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite 16", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("sqlite connection is closed")
        return res

    def deleteControlMinMaxByActive(self, active_name):
        try:
            # Conectar a la base de datos SQLite
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()

            # Definir la consulta SQL para eliminar la fila
            sqlite_delete_query = """DELETE FROM CONTROLMINMAX WHERE ACTIVE = ?"""

            # Ejecutar la consulta con el valor de active_name
            cursor.execute(sqlite_delete_query, (active_name,))

            # Confirmar los cambios
            sqliteConnection.commit()
            # print(f"Registro con ACTIVE='{active_name}' eliminado correctamente.")

            # Cerrar el cursor
            cursor.close()

        except sqlite3.Error as error:
            print("Error al trabajar con SQLite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                # print("Conexion SQLite cerrada.")

    def insertControlMinMaxWithData(self,results):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            name = results['NAME']
            minweek = results['MIN_WEEK']
            maxweek = results['MAX_WEEK']
            minmonth = results['MIN_MONTH']
            maxmonth = results['MAX_MONTH']
            fecha = results['DATE'].values[0]

            # insert developer detail
            sqlite_insert_with_param = """INSERT INTO 'CONTROLMINMAX'
                                              ('ACTIVE', 'MINWEEK', 'MAXWEEK', 'MINMONTH','MAXMONTH','LASTUPDATE') 
                                              VALUES (?, ?, ?,?,?,?);"""

            data_tuple = (
            name, minweek, maxweek, minmonth, maxmonth, fecha)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            # print("Developer added successfully \n")

            cursor.close()

        except sqlite3.Error as error:
            print("Error inserValueWithData while working with SQLite", error)
        finally:
            if cursor:
                cursor.close()
                # print("sqlite connection is closed")

    def updateControlMinMaxWithData(self,results):
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")
            name = results['NAME']
            minweek = results['MIN_WEEK']
            maxweek = results['MAX_WEEK']
            minmonth = results['MIN_MONTH']
            maxmonth = results['MAX_MONTH']
            fecha = results['DATE'].values[0]


            sqlite_update_with_param = """UPDATE CONTROLMINMAX SET MINWEEK=?, MAXWEEK=?,MINMONTH=?, MAXMONTH=?, LASTUPDATE=?
            WHERE ACTIVE =?"""

            data_tuple = (minweek, maxweek, minmonth, maxmonth, fecha, name)
            cursor.execute(sqlite_update_with_param, data_tuple)
            sqliteConnection.commit()



            cursor.close()

        except sqlite3.Error as error:
            print("Error inserValueWithData while working with SQLite", error)
        finally:
            if cursor:
                cursor.close()
                # print("sqlite connection is closed")

    def get_active_assets(self):
        """
        Returns a list of distinct asset names available in the MARKET table.
        Used by the public API to expose available instruments.
        """
        sqliteConnection = None
        assets = []
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            sqlite_select_query = """SELECT DISTINCT NAME FROM MARKET ORDER BY NAME"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            assets = [row[0] for row in records if row[0] is not None]
            cursor.close()
        except sqlite3.Error as error:
            print("Error get_active_assets while working with SQLite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
        return assets

    def get_asset_summary(self, name: str):
        """
        Returns the latest state of a given asset with key decision-making fields.
        Designed to be consumed by external services via the public API.

        Returns a dict with:
          - name, timestamp, price (current value)
          - action (BUY/SELL/WAIT/CLOSE), action_acum, action_count
          - tendence, direction, week_flow, week_dir
          - close_nxt_up, close_nxt_down, close_nxt_middle
          - rel_fcst, rel_fcst_percent, rel_fcst_std, rel_fcst_med
          - week_flow_med, week_flow_std
          - angle, angle_ima, angle_counter
          - global_min, global_max, motion_min, motion_max (relative range)
          - week_dir_bot_dst, month_dir_bot_dst
          - profit, protect
        """
        sqliteConnection = None
        result = {}
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()

            sqlite_select_query = """
                SELECT NAME, max(DATEVALUE), VALUE, ACTION, ACTION_COUNT, ACTION_ACUM,
                       TENDENCE, DIRECTION, WEEK_FLOW, WEEK_DIR,
                       CLOSE_NXT_UP, CLOSE_NXT_DOWN, CLOSE_NXT_MIDDLE,
                       REl_FCST, REl_FCST_PERCENT, REl_FCST_STD, REl_FCST_MED,
                       WEEK_FLOW_MED, WEEK_FLOW_STD,
                       ANGLE, ANGLE_IMA, ANGLE_COUNTER,
                       GLOBAL_MIN, GLOBAL_MAX, MOTION_MIN, MOTION_MAX,
                       WEEK_DIR_BOT_DST, MONTH_DIR_BOT_DST,
                       PROFIT, PROTECT,
                       LASTDIF, ACUMULATE, OPENVALUE
                FROM MARKET
                WHERE NAME = ?
            """
            cursor.execute(sqlite_select_query, (name,))
            row = cursor.fetchone()

            if row and row[0] is not None:
                result = {
                    "name":               row[0],
                    "timestamp":          row[1],
                    "price":              row[2],
                    "action":             row[3],
                    "action_count":       row[4],
                    "action_acum":        row[5],
                    "tendence":           row[6],
                    "direction":          row[7],
                    "week_flow":          row[8],
                    "week_dir":           row[9],
                    "close_nxt_up":       row[10],
                    "close_nxt_down":     row[11],
                    "close_nxt_middle":   row[12],
                    "rel_fcst":           row[13],
                    "rel_fcst_percent":   row[14],
                    "rel_fcst_std":       row[15],
                    "rel_fcst_med":       row[16],
                    "week_flow_med":      row[17],
                    "week_flow_std":      row[18],
                    "angle":              row[19],
                    "angle_ima":          row[20],
                    "angle_counter":      row[21],
                    "global_min":         row[22],
                    "global_max":         row[23],
                    "motion_min":         row[24],
                    "motion_max":         row[25],
                    "week_dir_bot_dst":   row[26],
                    "month_dir_bot_dst":  row[27],
                    "profit":             row[28],
                    "protect":            row[29],
                    "last_dif":           row[30],
                    "acumulate":          row[31],
                    "open_value":         row[32],
                }
            cursor.close()
        except sqlite3.Error as error:
            print("Error get_asset_summary while working with SQLite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
        return result

    def get_asset_history(self, name: str, days: int = 5):
        """
        Returns recent daily data points for an asset.
        Used by the public API /asset/{name}/history endpoint.
        """
        sqliteConnection = None
        rows_list = []
        try:
            sqliteConnection = sqlite3.connect(self.db)
            cursor = sqliteConnection.cursor()
            sqlite_select_query = """
                SELECT DATEVALUE, VALUE, ACTION, TENDENCE, DIRECTION,
                       WEEK_FLOW, ANGLE, PROFIT, LASTDIF, ACUMULATE
                FROM MARKET
                WHERE NAME = ?
                  AND DATEVALUE > date(julianday(date('now')) - ?)
                ORDER BY DATEVALUE ASC
            """
            cursor.execute(sqlite_select_query, (name, days))
            records = cursor.fetchall()
            for row in records:
                rows_list.append({
                    "timestamp":  row[0],
                    "price":      row[1],
                    "action":     row[2],
                    "tendence":   row[3],
                    "direction":  row[4],
                    "week_flow":  row[5],
                    "angle":      row[6],
                    "profit":     row[7],
                    "last_dif":   row[8],
                    "acumulate":  row[9],
                })
            cursor.close()
        except sqlite3.Error as error:
            print("Error get_asset_history while working with SQLite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
        return rows_list

    def prepareList(self):
        data = list()
        data.append("AAPL")
        data.append("AMD")
        data.append("AMZN")
        data.append("BABA")
        data.append("BTCUSD")
        data.append("DIS")
        data.append("ETHUSD")
        data.append("GOOG")
        data.append("INTC")
        data.append("MCD")
        data.append("META")
        data.append("MSFT")
        data.append("NFLX")
        data.append("NVDA")
        data.append("SBUX")
        data.append("SONY")
        data.append("TSLA")
        data.append("VTI")
        return data

def main():
    market = MarketSQLManager()
    # market.inserValue("TEST",1010.34,100.0,50,340)
    # res = market.getValueWithID(1)
    # res = market.getLastValueWithName("ETH")
    # print("OK")
    # market.getAll()
    # market.getAllWithName("ETH")
    # data = market.getAllWithNameForXdays("EURUSD",1)
    #
    start = '2024-02-04'
    # end = '2023-10-02'
    # # data = market.getResumeForRangeDates(start,end)
    # # data = market.getResumeForXdaysPast(start,10)
    # data = market.getResumeCSVForXdaysPast(start,10)
    active = 'TSLA'

    market.updatePredictForActive(active,'1','0')
    data = market.getPredictForActive(active)
    print(data)
    # interval = []
    # interval.append(5)
    # interval.append(10)

    # actives = market.getActivesforInterval(interval)
    # print(actives)
    #print("hola")
    # market.getAllWithNameForXdays("ETH",2)
    # market.getControlValuesForName("EURUSD")
    # market.resetLastByname("ETH")
if __name__ == "__main__":
    main()
