"""Price data methods for MarketManager - data module."""

    def search_pricesYahoo(self, active):
        data = None
        try:
            nada = ""
            # data = yf.download(tickers=active.parameters.name, period='2d', interval='15m')

        except Exception as e:

            print(f"ERROR search_pricesYahoo {str(e)}")

        return data

    def search_pricesDB(self, active):

        data = None
        try:

            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            print(f" hora : {current_time_h} minutos: {current_time_min}")

            current_value, day_value = self.alpaca.getCurrentPrice(active.parameters.name)
            invested,profit, open, qty = self.alpaca.is_investedComplete(active.parameters.name)
            weekno = datetime.datetime.today().weekday()
            days = 4
            if weekno == 0 or weekno == 1:
                days = 6

            dif = 0
            acu = 0
            acumulate = 0
            tendence_acu = 0
            tendence_count = 0
            oldvalue = 0
            min_value = 999
            min_acu = 0
            max_value = 0
            max_acu = 0
            direction = Constants.DIR_WAIT
            min_dir = 99999
            max_dir = 0
            indi_dir = ''
            motion_min = 0
            motion_max = 0
            global_min = 0
            global_max = 0
            action_acum = 0
            week_flow = ''
            week_flow_med = 0
            week_flow_std = 0
            rel_fcst = ''
            rel_fcst_std = 0
            rel_fcst_med = 0
            rel_fcst_min = 0
            rel_fcst_max = 0
            action_count = 0
            rel_fcst_percent = 0
            close_nxt_up = 0
            close_nxt_down = 0
            close_nxt_middle = 0
            week_dir = Constants.DIR_WAIT
            week_min_dir = 99999
            week_max_dir = 0
            week_dir_flow = 0
            protect = 0
            revenue =  profit

            action = Constants.ACTION_WAIT
            oldDBvalue = self.dataBDMan.getLastValueWithName(active.parameters.name)
            if oldDBvalue is not None:
                oldvalue = oldDBvalue[0]["value"]

                acumulate = oldDBvalue[0]["acumulate"]
                tendence_acu = oldDBvalue[0]["tendence_acu"]
                tendence_count = oldDBvalue[0]["tendence_count"]
                min_value = oldDBvalue[0]["min_value"]
                min_acu = oldDBvalue[0]["min_acu"]
                max_value = oldDBvalue[0]["max_value"]
                max_acu = oldDBvalue[0]["max_acu"]
                action = oldDBvalue[0]["action"]
                if "CLOSE-SELL" in action:
                    action  = "SELL"
                if "CLOSE-BUY" in action:
                    action  = "BUY"
                if "CLOSE" in action:
                    if invested==True:
                        action = 'BUY'
                else:
                    nada = ""
                    # if invested==False:
                    #     action = 'CLOSE'



                action_count = oldDBvalue[0]["action_count"]
                direction = oldDBvalue[0]["direction"]
                min_dir = oldDBvalue[0]["min_dir"]
                max_dir = oldDBvalue[0]["max_dir"]
                indi_dir = oldDBvalue[0]["indi_dir"]
                motion_min = oldDBvalue[0]["motion_min"]
                motion_max = oldDBvalue[0]["motion_max"]
                global_min = oldDBvalue[0]["global_min"]
                global_max = oldDBvalue[0]["global_max"]
                action_acum = oldDBvalue[0]["action_acum"]
                week_flow = oldDBvalue[0]["week_flow"]
                week_flow_std = oldDBvalue[0]["week_flow_std"]
                week_flow_med = oldDBvalue[0]["week_flow_med"]
                rel_fcst = oldDBvalue[0]["rel_fcst"]
                rel_fcst_std = oldDBvalue[0]["rel_fcst_std"]
                rel_fcst_med = oldDBvalue[0]["rel_fcst_med"]
                rel_fcst_min = oldDBvalue[0]["rel_fcst_min"]
                rel_fcst_max = oldDBvalue[0]["rel_fcst_max"]
                rel_fcst_percent = oldDBvalue[0]["rel_fcst_percent"]
                close_nxt_up = oldDBvalue[0]["close_nxt_up"]
                close_nxt_down = oldDBvalue[0]["close_nxt_down"]
                close_nxt_middle = oldDBvalue[0]["close_nxt_middle"]
                week_dir = oldDBvalue[0]["week_dir"]
                week_min_dir = oldDBvalue[0]["week_min_dir"]
                week_max_dir = oldDBvalue[0]["week_max_dir"]
                week_dir_flow = oldDBvalue[0]["week_dir_flow"]
                angle_ima = oldDBvalue[0]["angle_ima"]
                angle_ima_counter = oldDBvalue[0]["angle_ima_counter"]
                angle = oldDBvalue[0]["angle"]
                angle_counter = oldDBvalue[0]["angle_counter"]

                month_dir_bot_dst = oldDBvalue[0]["month_dir_bot_dst"]
                week_dir_bot_dst = oldDBvalue[0]["week_dir_bot_dst"]
                week_dir_bot_dst_new = oldDBvalue[0]["week_dir_bot_dst_new"]
                protect = oldDBvalue[0]["protect"]
                if "CLOSE" == action:
                    protect = 0
                previous_entry_price = oldDBvalue[0]["openValue"]
                previous_qty = oldDBvalue[0]["qty"]
                # correccion estado por si cerro por stop loss o take profit
                if not invested and action != 'CLOSE':
                    action = 'CLOSE'
                    protect = 0
                    # Posición cerrada, calcular PnL
                    pnl, closed_price = self.alpaca.get_closed_pnl(active.parameters.name, previous_entry_price, previous_qty)
                    if pnl is not None:
                        # Registrar PnL en tu historial
                        self.log.info(f"{active.parameters.name} cerró en {closed_price} con PnL {pnl}")
                        revenue = pnl
                        profit = pnl


            self.dataBDMan.inserValue(active.parameters.name, current_value, oldvalue, dif, acumulate, tendence_acu,
                                      tendence_count, min_value,
                                      max_value, min_acu, max_acu, direction, min_dir, max_dir, indi_dir, motion_min,
                                      motion_max, global_min, global_max, action_acum, action_count,
                                      week_flow, week_flow_std, week_flow_med, rel_fcst, rel_fcst_std, rel_fcst_med,
                                      rel_fcst_min, rel_fcst_max, rel_fcst_percent, close_nxt_up, close_nxt_down,close_nxt_middle,
                                      week_dir, week_min_dir, week_max_dir,week_dir_flow,angle_ima, angle_ima_counter,angle, angle_counter,
                                      month_dir_bot_dst, week_dir_bot_dst, week_dir_bot_dst_new, profit, open, qty, protect, revenue, action )

            data = self.dataBDMan.getAllWithNameForXdaysSpecial(active.parameters.name, days)

            # Verificacion de que hay almenos 3 dias recuperados para procesar
            faltan = self.verify3DaysInData(data)
            start_date_time = None
            if faltan > 0:

                days = days + faltan
                data = self.dataBDMan.getAllWithNameForXdaysSpecial(active.parameters.name, days)


        except Exception as e:
            print(f"ERROR search_pricesDB {str(e)}")

        return data

    def filterActives(self, actives, interval):

        activesFiletered = list();

        dbActives = self.dataBDMan.getActivesforInterval(interval)
        for active in actives:
            if self.findActiveInDB(dbActives, active.parameters.name):
                activesFiletered.append(active)

        return activesFiletered

    def getfirstValueForToday(self,  data, results=None):
        # print(f"getfirstValueForToday")
        today = time.strftime("%Y-%m-%d")
        from datetime import datetime
        if self.simulation:

            temp = results[Constants.DATE].values[0]
            todayDate = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            # todayCeros = todayDate.replace(hour=0, minute=0, second=0, microsecond=0)
            today = todayDate.strftime("%Y-%m-%d")


        df = data.loc[(data['date'] >= today)]

        first = df['date'].iloc[0]
        t = datetime.strptime(first, '%Y-%m-%d %H:%M:%S.%f')
        current_time_h = t.hour * 100
        current_time_min = t.minute
        startTimeForToday = int(current_time_h + current_time_min)
        # print(f"START DATE IS : {startTimeForToday}")
        return startTimeForToday

    def updateTimeZoneValues(self, results=None):
        timedelta = None
        try:
            if self.simulation:
                from datetime import datetime
                temp = results[Constants.DATE].values[0]
                # if np.issubdtype(temp.dtype, np.datetime64):#para los valores de yahoo
                #     t = datetime.strptime(str(temp), '%Y-%m-%dT%H:%M:%S.%f000')
                #     timedelta = int(t.astimezone().utcoffset().seconds / 3600)
                # else:
                t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')

                timedelta = int(t.astimezone().utcoffset().seconds / 3600)

            else:
                timedelta = -time.timezone / 3600

            if timedelta and timedelta == 1:
                # print(f"TIMEZONE ES INVIERNO {timedelta}")
                self.prepareInvierno()
            else:
                # print(f"TIMEZONE ES VERANO {timedelta}")
                self.prepareVerano()
        except Exception as e:
            message = f"{self.name}  fallo timedelta "
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(f"ERROR updateTimeZoneValues {str(e)}")

    def prepare1430(self):
        self.closeStart = 2040
        self.closeEnd = 2100

        # caluclos iniciales
        self.iniStart = 1430
        self.iniEnd = 1500

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2040
        self.closeAnalisisIntervalEnd = 2100

        # prepare relative values
        self.prepRelStart = 1430
        self.prepRelEnd = 1500
    def prepareInvierno(self):
        self.closeStart = 2140
        self.closeEnd = 2200

        # caluclos iniciales
        self.iniStart = 1530
        self.iniEnd = 1600

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200

        # prepare relative values
        self.prepRelStart = 1530
        self.prepRelEnd = 1535

    def prepareVerano(self):
        self.closeStart = 2140
        self.closeEnd = 2200

        # caluclos iniciales
        self.iniStart = 1530
        self.iniEnd = 1550

        # retornar intervalo
        self.normalIntervalStart = 1600
        self.normalIntervalEnd = 1605

        self.closeAnalisisIntervalStart = 2140
        self.closeAnalisisIntervalEnd = 2200

        # prepare relative values
        self.prepRelStart = 1530
        self.prepRelEnd = 1550

    def updateIntervalForAll(self, actives):

        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)

        intervalo5MIn = 10
        intervalo10MIn = 10



        mensaje = None
        if (currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd)):
            # cambiamoa a 5 minutos
            for active in actives:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    return
                self.dataBDMan.updateIntervalForActive(active.parameters.name, intervalo5MIn, 3)
            mensaje = f"updateIntervalForAll {self.name} intervalo de 5 MIN"

        if (currentTime >= int(self.normalIntervalStart) and currentTime < int(self.normalIntervalEnd)):
            # cambiamoa a 10 minutos
            for active in actives:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    return
                self.dataBDMan.updateIntervalForActive(active.parameters.name, self.intervalTime, -1)
            mensaje = f"updateIntervalForAll {self.name} intervalo de: {self.intervalTime} MIN"

        if (currentTime >= int(self.closeAnalisisIntervalStart) and currentTime < int(self.closeAnalisisIntervalEnd)):
            # cambiamoa a 10 minutos
            for active in actives:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    return
                self.dataBDMan.updateIntervalForActive(active.parameters.name, intervalo10MIn, 5)
            mensaje = f"updateIntervalForAll {self.name} intervalo de 10 MIN"

        if mensaje is not None:
            self.telegram.enviarMensaje(mensaje, self.telegram.tokenBot, self.importanteslTelegroup)

        enb = True

    def updateCounterForAll(self):
        actives = self.dataBDMan.getALLActivesControlTime()

        for active in actives:
            counter = active['counter']
            name = active['active']
            interval = active['interval']
            initial = active['initial']
            if counter != -1:
                if counter > 1:
                    counter = counter - 1
                    self.dataBDMan.updateIntervalForActive(name, interval, counter)
                elif counter == 1:
                    self.dataBDMan.updateIntervalForActive(name, initial, -1)
        enb = True

    def findActiveInDB(self, dbactives, value):
        for active in dbactives:
            if value == active['active']:
                return True
        return False

    def search_prices_list_local(self, actives):
        interval = self.getInterval(None)
        # if len(interval)>0:
        # actives = self.filterActives(actives, interval)
        for active in actives:
            results = {}

            # if active.parameters.verifyMarketOpen:
            #     if self.alpaca.ismarketOpen() == False:
            #         print(f"market is closed for {active.parameters.name}")
            #         continue

            if self.isDBData:
                data = self.search_pricesDB(active)
            else:
                data = self.search_pricesYahoo(active)
            # self.reviewControls(data, active)
            if data is not None and not data.empty and len(data) > 0:
                fastReview = self.evaluateActions(data, results, active)


            if 'ALERT' in results and results['ALERT']:
                self.processAlerts(True, results, active)
                if self.isDBData:
                    self.drawActiveAction(active)
                else:
                    active.drawInfo(data)

    def search_prices_list(self, actives):
        interval = self.getInterval(None)
        # if len(interval)>0:
        actives = self.filterActives(actives, interval)
        for active in actives:
            results = {}

            if active.parameters.verifyMarketOpen:
                if self.alpaca.ismarketOpen() == False:
                    print(f"market is closed for {active.parameters.name}")
                    continue

            if self.isDBData:
                data = self.search_pricesDB(active)
            else:
                data = self.search_pricesYahoo(active)
            # self.reviewControls(data, active)
            if data.empty == False and len(data) > 0:
                fastReview = self.evaluateActions(data, results, active)
                #en real se añade un start de 5 minutos
                # if fastReview == True:
                #     self.evaluateActions(data, results, active,True)
            if 'ALERT' in results and results['ALERT']:
                self.processAlerts(True, results, active)
                if self.isDBData:
                    self.drawActiveAction(active)
                else:
                    active.drawInfo(data)



    def sendResultsEndDay(self, sendResults=False):
        # grafico
        groupTelegram = self.resultsTelegroup
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        # print(f" gettime hora sistema: {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)

        # if (currentTime >= 2200 and currentTime <= 2204) or \
        #         (currentTime >= 1600 and currentTime <= 1604) or \
        #         (currentTime >= 1800 and currentTime <= 1804) or \
        #         (currentTime >= 2000 and currentTime <= 2004) or sendResults:
        if (currentTime >= 2200 and currentTime <= 2204) or \
                (currentTime >= 900 and currentTime <= 904) or \
                (currentTime >= 1100 and currentTime <= 1104) or \
                (currentTime >= 1600 and currentTime <= 1604) or \
                (currentTime >= 1800 and currentTime <= 1804) or \
                (currentTime >= 2000 and currentTime <= 2004) or sendResults:
            start = datetime.datetime.today()
            start_time = start.replace(hour=0, minute=0, second=0, microsecond=0)

            if start:
                end_timeplus = start + datetime.timedelta(days=+1)
                start = start_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                end = end_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")
            # start_string = datetime.datetime.strptime(start, "%Y-%m-%d")
            # start_string = str(start)

            # end =  start_string
            # start_string =  '2023-07-20'
            # end = '2023-07-20'
            #recuperar los valores abiertos
            onlyOpen = self.dataBDMan.getCurrentRevenues()
            res = self.dataBDMan.getResumeForRangeDatesExact(start, end)
            print(res)

            if res is not None and len(res):
                total = 0
                messages = f"{self.name} RESULTADOS DEL DIA \n"
                for i in range(len(res)):
                    value = res.iloc[i]['value']
                    if value is None:
                        value =0
                    name = res.iloc[i]['name']
                    total = total + float(value)
                    abierto = None
                    if name in onlyOpen:
                        abierto = f" {str(onlyOpen[name])}"
                        onlyOpen.pop(name)
                    messages = messages + f" <b>{name}</b> : {value}  \n"
                    if abierto is not None:
                        messages = messages + f"        <b>Abierto</b> : {abierto}  \n"
                messages = messages + f"total: {total}"


            if len(onlyOpen) >0:
                for clave, valor in onlyOpen.items():
                    messages = messages + f" <b>{clave}</b> open: {valor}  \n"
            self.telegram.enviarMensaje(messages, self.telegram.tokenBot, groupTelegram)

    def drawActiveAction(self, active, send=True):
        days = 2
        weekno = datetime.datetime.today().weekday()
        if weekno == 0:
            days = 3
        data = None
        if self.start is not None and self.end is not None:
            data = self.dataBDMan.getAllWithNameForXdaysRangeDates(active.parameters.name, self.start, self.end)
        else:
            data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, days)

        # Verificacion de que hay almenos 3 dias recuperados para procesar
        faltan = self.verify3DaysInData(data)
        start_date_time = None
        if faltan > 0:
            if self.start is not None and self.end is not None:
                try:
                    start_date_time = datetime.datetime.strptime(self.start, "%Y-%m-%d %H:%M:%S.%f")
                except Exception as error:
                    # print("Error getAllWithNameForXdaysRangeDates  date format using second change", error)
                    start_date_time = datetime.datetime.strptime(self.start, "%Y-%m-%d")

                if start_date_time:
                    start_date_timeplus = start_date_time + datetime.timedelta(days=-faltan + 1)
                    start = start_date_timeplus.strftime("%Y-%m-%d %H:%M:%S.%f")

                data = self.dataBDMan.getAllWithNameForXdaysRangeDates(active.parameters.name, self.start, self.end)
            else:
                days = days + faltan-1
                data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, days)

        rangehours = active.parameters.rangehours
        if active.parameters.name == 'BTCUSD' or active.parameters.name == 'ETHUSD':
            rangehours = None
        buyData = data[((data['action'] == 'BUY') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-BUY') & (data['change_action'] == 1))]
        closeData = data[((data['action'] == 'CLOSE') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-BUY') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-SELL') & (data['change_action'] == 1))]
        sellData = data[((data['action'] == 'SELL') & (data['change_action'] == 1)) | ((data['action'] == 'CLOSE-SELL') & (data['change_action'] == 1))]
        active.drawDataDBActions(data, buyData, sellData, closeData, send, rangehours, self.simulation)

    def addmessages(self, message, results):
        messages = ""
        if Constants.MESSAGES in results:
            messages = results[Constants.MESSAGES]
            messages = messages + "\n"
            messages = messages + message
        else:
            messages = message
        results[Constants.MESSAGES] = messages

    # @mide_tiempo
    def evaluateNewAction(self, results, active, isFastReview=False, isfcst=False):
        fastReview = isFastReview

        try:
            revenue = 0
            winvalue = 0
            res = None
            if self.simulation == False:
                if (results[Constants.CURRENT_ACTION] != Constants.ACTION_CLOSE):
                    try:
                        # if active.parameters.name == 'BTCUSD':
                        #     res, revenue = self.alpaca.is_invested(active.parameters.second_name)
                        # else:
                        res, revenue = self.alpaca.is_invested(active.parameters.name)
                        print(f" evaluateNewAction  paso1 ")
                        results[Constants.REVENUE] = revenue
                        revenue = float(revenue)
                        tp_step = float(active.parameters.profit)
                        last_tp = float(results.get(Constants.PROTECT, 0))
                        needProfit = False

                        # 1 Solo trabajamos si hay beneficio
                        if revenue > 0:
                            # 2 Si no hay TP aún, o se ha superado el objetivo inicial
                            if last_tp == 0:
                                if revenue >= tp_step:
                                    needProfit = True
                            else:
                                # 3 Solo subir TP si ha aumentado al menos X desde el último TP
                                if revenue >= last_tp + tp_step:
                                    needProfit = True

                            # 4 Nunca permitir que el TP baje
                            if revenue <= last_tp:
                                needProfit = False
                                #poner take profit

                            if needProfit:
                                results[Constants.PROTECT] = revenue
                                if active.parameters.name == 'BTCUSD':
                                    print(f" evaluateNewAction  paso2 ")
                                    data = self.alpaca.add_smart_stop_usd_crypto(active.parameters.name, active.parameters.second_name,max_loss_usd=active.parameters.max_loss_usd,protect_profit_usd=active.parameters.protect_profit_usd)
                                    print(f" evaluateNewAction  paso3 ")
                                elif active.parameters.name == 'ETHUSD':
                                    print(f" evaluateNewAction  paso2 ")
                                    data= self.alpaca.add_smart_stop_usd_crypto(active.parameters.name, active.parameters.second_name,max_loss_usd=active.parameters.max_loss_usd,protect_profit_usd=active.parameters.protect_profit_usd)
                                    print(f" evaluateNewAction  paso3 ")
                                else:
                                    nada = ""
                                    data= self.alpaca.add_smart_stop_usd_stock(active.parameters.name, max_loss_usd=active.parameters.max_loss_usd,
                                                                          protect_profit_usd=active.parameters.protect_profit_usd)
                                message = (
                                    f"🛑 STOP LOSS actualizado\n"
                                    f"Activo: {active.parameters.name}\n\n"
                                    f"📥 Entrada: {data['entry_price']}\n"
                                    f"📊 Precio actual: {data['current_price']}\n"
                                    f"⛔ Stop Loss: {data['stop_price']}\n\n"
                                    f"📦 Cantidad: {data['qty']}\n"
                                    f"💸 Pérdida máxima: {data['max_loss_usd']}$\n"
                                    f"🛡️ Protección beneficio: {data['protect_profit_usd']}$"
                                )

                                self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                        else:
                            #control para negativos
                            if abs(float(revenue)) >= float(active.parameters.profit):
                                #cerramos
                                results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                            # else:
                            #     needProfit = True
                            #     if results[Constants.PROTECT] !=0:
                            #         if abs(float(revenue)) < float(results[Constants.PROTECT]):
                            #             #ya hay un profit puesto
                            #             needProfit = False
                            #     #poner take profit
                            #     if needProfit:
                            #         results[Constants.PROTECT] = revenue
                            #         if active.parameters.name == 'BTCUSD':
                            #             print(f" evaluateNewAction  paso2 ")
                            #             self.alpaca.add_smart_stop_usd_crypto(active.parameters.second_name,max_loss_usd=3,protect_profit_usd=3)
                            #             print(f" evaluateNewAction  paso3 ")
                            #         elif active.parameters.name == 'ETHUSD':
                            #             print(f" evaluateNewAction  paso2 ")
                            #             self.alpaca.add_smart_stop_usd_crypto(active.parameters.name,max_loss_usd=3,protect_profit_usd=3)
                            #             print(f" evaluateNewAction  paso3 ")
                            #         else:
                            #             nada = ""
                            #             self.alpaca.add_smart_stop_usd_stock(active.parameters.name, max_loss_usd=3,
                            #                                                   protect_profit_usd=3)
                        # actionAcum = results[Constants.ACTION_ACUM]
                        # if results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                        #     if actionAcum < 0:
                        #         actionAcum = abs(actionAcum)
                        #     elif actionAcum > 0:
                        #         actionAcum = actionAcum * (-1)
                        # results[Constants.REVENUE] = revenue
                        # minimunactionAcum = self.minimunActionAcum
                        # # Control ganancias cerramos si el valor es superior a X
                        # if active.parameters.controlWin or self.enableControlWIN:
                        if isFastReview == True:
                           self.dataBDMan.updateIntervalForActive(active.parameters.name, 5, 1)
                                # self.addmessages(message, results)
                                # self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                                # print(message)
                    except Exception as e:
                        message = f"{self.name} fallo revenue {results[Constants.CURRENT_ACTION]} para {active.parameters.name} ganancia {str(revenue)} error: {str(e)}"
                        self.addmessages(message, results)
                        self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
                        print(f"ERROR1 evaluateNewAction {str(e)}")
                        print(
                            f"fallo en revenue for {active.parameters.name} second: {active.parameters.second_name}")

            elif self.simulation == True and isFastReview == True and self.disableCloseEndRevenue == False:
                nada = ""
                if (results[Constants.CURRENT_ACTION] != Constants.ACTION_CLOSE):
                    try:
                        revenue = results[Constants.ACTION_ACUM]
                        if results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                            if revenue < 0:
                                revenue = abs(revenue)
                            elif revenue > 0:
                                revenue = revenue * (-1)
                        minimunactionAcum = self.minimunActionAcum
                        # Control ganancias cerramos si el valor es superior a X
                        if active.parameters.controlWin or self.enableControlWIN:
                            if isFastReview == True:
                                if float(revenue) >= float(minimunactionAcum):
                                    fastReview = False
                                    message = f"{self.name} Cerramos por regla de ahorro accion: {results[Constants.CURRENT_ACTION]}  para {active.parameters.name} ganancia {str(revenue)}"
                                    results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
                                    # self.addmessages(message, results)
                                    # self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                                    print(message)
                    except Exception as e:
                        message = f"{self.name} fallo revenue {results[Constants.CURRENT_ACTION]} para {active.parameters.name} ganancia {str(revenue)} error: {str(e)}"
                        self.addmessages(message, results)
                        self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
                        print(f"ERROR2 evaluateNewAction {str(e)}")
                        print(
                            f"fallo en revenue for {active.parameters.name} second: {active.parameters.second_name}")

            if Constants.NEW_ACTION in results:
                currentAction = results[Constants.CURRENT_ACTION]

                if results[Constants.NEW_ACTION] == results[Constants.CURRENT_ACTION] and fastReview == False:
                    # NO CAMBIO DE ACCION
                    same = True
                    print(f"no cambio el estado")
                else:
                    isSell = False
                    isBuy = False
                    isClose = False
                    results[Constants.CHANGE_ACTION] = 1
                    amount = 1000
                    newAction = results[Constants.NEW_ACTION]
                    # print(f"changeStatus for {active.parameters.name} second: {active.parameters.second_name} "
                    #       f"current {results[Constants.CURRENT_ACTION]} newAction {newAction}")

                    results[Constants.CURRENT_ACTION] = newAction
                    if Constants.ACTION_BUY == newAction:
                        # self.operations.currentTupla['START'] = results[Constants.VALUE]
                        # self.operations.currentTupla['START_DATE'] = results[Constants.DATE].values[0]

                        isBuy = True
                        self.addStartValues(results, isBuy, active)
                        self.updateMinMaxValues(results=results)
                    elif Constants.ACTION_SELL == newAction:
                        # self.operations.currentTupla['START'] = results[Constants.VALUE]
                        # self.operations.currentTupla['START_DATE'] = results[Constants.DATE].values[0]
                        isSell = True
                        self.addStartValues(results, False, active)
                        self.updateMinMaxValues(results=results)
                    elif Constants.ACTION_CLOSE in newAction:
                        isClose = True
                        wasBuy = True
                        if active.parameters.reevaluateAction:
                            fastReview = True
                        if Constants.ACTION_SELL == currentAction:
                            wasBuy = False
                        self.addStopValues(results, wasBuy, active)

                        results[Constants.ACTION_COUNT] = 0
                        results[Constants.ACTION_ACUM] = 0

                        # if isfcst == False:
                        # self.dataBDMan.updateIntervalForActive(active.parameters.name, 5, 2)

                        self.updateMinMaxValues(results=results)
                    else:
                        print(f"otra accion no esperada !! {results[Constants.CURRENT_ACTION]}")

                    results['ALERT'] = True

                    # ===================== OPERAR MERCADO =====================
                    if self.simulation == False:
                        try:
                            if self.operate and active.parameters.operate:
                                action_map = {
                                    Constants.ACTION_BUY: "LONG",
                                    Constants.ACTION_SELL: "SHORT",
                                    Constants.ACTION_CLOSE: "FLAT"
                                }

                                target_side = action_map.get(results[Constants.CURRENT_ACTION], None)

                                if target_side is not None:
                                    mess = " "
                                    if target_side == "FLAT":
                                        mess = self.alpaca.close_all_positions_and_orders(active.parameters.name)

                                    else:

                                        mess = self.alpaca.execute_target_position(
                                            active.parameters.name,
                                            target_side,
                                            amount
                                        )
                                    print(
                                        f"Operación {results[Constants.CURRENT_ACTION]} ejecutada en {active.parameters.name}: {mess}")

                                    error_keywords = [
                                        "failed",
                                        "error",
                                        "exception",
                                        "insufficient",
                                        "denied",
                                        "rejected"
                                    ]

                                    if any(k in mess.lower() for k in error_keywords):
                                        self.telegram.enviarMensaje(mess, self.telegram.tokenBot,
                                                                    self.errorTelegroup)

                                    # Obtener ganancia si es cierre o cambio de posición
                                    # revenue = 0
                                    if target_side == "FLAT":
                                        invested, revenue = self.alpaca.is_invested(active.parameters.name)
                                        results[Constants.REVENUE] = revenue



                                    # Obtener ganancia actual
                                    # revenue = 0
                                    # invested, revenue = self.alpaca.is_invested(active.parameters.name)
                                    # results[Constants.REVENUE] = revenue

                                    # # Colocar stop inteligente solo si no estamos FLAT
                                    # if target_side != "FLAT" and invested:
                                    #     # Determinar tipo de stop según activo (crypto o stock)
                                    #     if active.parameters.is_crypto:
                                    #         stop_info = self.alpaca.add_smart_stop_usd_crypto(
                                    #             symbol=active.parameters.name,
                                    #             max_loss_usd=active.parameters.max_loss_usd,
                                    #             protect_profit_usd=active.parameters.protect_profit_usd
                                    #         )
                                    #     else:
                                    #         stop_info = self.alpaca.add_smart_stop_usd_stock(
                                    #             symbol=active.parameters.name,
                                    #             max_loss_usd=active.parameters.max_loss_usd,
                                    #             protect_profit_usd=active.parameters.protect_profit_usd
                                    #         )
                                    #
                                    #     print(f"Stop inteligente colocado: {stop_info}")
                                    #     mess += f" | Stop: {stop_info['stop_price']}"

                                    # Mensaje unificado para Telegram
                                    message = (
                                        f"{self.name} operación en ALPACA: {results[Constants.CURRENT_ACTION]} "
                                        f"para {active.parameters.name}, invertido {amount}, "
                                        f"ganancia {revenue}, mensaje: {mess}"
                                    )
                                    self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.newTelegroup)
                                    self.addmessages(message, results)
                                else:
                                    print(f"Acción desconocida: {results[Constants.CURRENT_ACTION]}")
                        except Exception as e:
                            # Captura de errores general
                            revenue = results.get(Constants.REVENUE, 0)
                            message = (
                                f"{self.name} ERROR en operación {results[Constants.CURRENT_ACTION]} "
                                f"para {active.parameters.name}, ganancia {revenue}, error: {str(e)}"
                            )
                            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
                            self.addmessages(message, results)
                            print(f"ERROR3 evaluateNewAction {str(e)}")
                            print(
                                f"{self.name} operate for {active.parameters.name}, second: {active.parameters.second_name}")



                    # ACUMULAR VALORES PARA DIBUJAR SIMULACION
                    if self.simulation:
                        dataTemp = {}

                        dataTemp['date'] = results[Constants.DATE].values[0]
                        dataTemp['value'] = results[Constants.VALUE]
                        if isSell:
                            self.operations.sellData.append(dataTemp)
                        elif isBuy:
                            self.operations.buyData.append(dataTemp)
                        elif isClose:
                            self.operations.closeData.append(dataTemp)
            else:
                #para guardar logs para analisis
                if self.simulation:
                        if self.allAnalysLogs:
                            nada =""
                            self.addNormaValues(results, active)

        except Exception as e:
            message = f"{self.name}  fallo change state {results[Constants.CURRENT_ACTION]} para {active.parameters.name} ganancia {str(winvalue)} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(f"ERROR evaluateNewAction {str(e)}")
            print(f"fallo change state for {active.parameters.name} second: {active.parameters.second_name}")

        return fastReview

    def printAnalisis(self, results, active):
        # if self.simulation:
        #     # acumular distancias
        #     # self.prepareBESTDISTANCE(results)
        # print(f"PRINT ANALISIS  {results[Constants.DATE].values[0]} ACCION: {results[Constants.CURRENT_ACTION]} RELAT: {results[Constants.RELATIVE]} ACUM: {results[Constants.ACUMULADO]} ACT_ACUM: {results[Constants.ACTION_ACUM]} FLUJO: {results[Constants.FLUJO]} contador {results[Constants.FLUJO_COUNT]} difference: {active.parameters.difference} INDICATOR_MED_MOMENT {results[Constants.INDICATOR_MED_MOMENT]} MED {results[Constants.INDICATOR_MED]} MED_STD {results[Constants.INDICATOR_MED_STD]} ")
        print(
            f"PRINT ANALISIS  {results[Constants.DATE].values[0]}  ACUM: {results[Constants.ACUMULADO]} \tFLOW_DIFF: {results[Constants.FLOW_DIFF]} \tPREVIUS: {results[Constants.PREVIOUS_DIST]} \tACCION: {results[Constants.CURRENT_ACTION]}  \tRELAT: {results[Constants.RELATIVE]}   ")
        print(
            f"PRINT0 ANALISIS  {results[Constants.DATE].values[0]} ACTION_ACUM: {results[Constants.ACTION_ACUM]} \tACTION_DISTANCE: {results[Constants.ACTION_DISTANCE]} \tACTION_COUNT: {results[Constants.ACTION_COUNT]} \tFLUJO: {results[Constants.FLUJO]} \tFLUJO_COUNT: {results[Constants.FLUJO_COUNT]}  ")

        print(
            f"PRINT00 ANALISIS  {results[Constants.DATE].values[0]} ACTION_ACUM: {results[Constants.ACTION_ACUM]} \tACTION_MIN_DIST: {results[Constants.ACTION_MIN_DIST]} \tACTION_MAX_DIST: {results[Constants.ACTION_MAX_DIST]} \tACTION_MIN: {results[Constants.ACTION_MIN]} \tACTION_MAX: {results[Constants.ACTION_MAX]}  ")

        print(
            f"PRINT1 ANALISIS  {results[Constants.DATE].values[0]} INDICATOR_MED_MOMENT: {results[Constants.INDICATOR_MED_MOMENT]} \tINDICATOR_MED_MOMENT_VALUE: {results[Constants.INDICATOR_MED_MOMENT_VALUE]} \t STD_MOMENT: {results[Constants.STD_MOMENT]}")
        print(
            f"PRINT2 ANALISIS  {results[Constants.DATE].values[0]} IMA1: {results[Constants.IMA1]} \tIMA5MA20: {results[Constants.IMA5MA20]} \tIMA_NEW: {results[Constants.IMA_NEW]} \tIMA1_DIS :{results[Constants.IMA1_DISTANCE]}")
        print(
            f"PRINT3 ANALISIS  {results[Constants.DATE].values[0]} MARKET_TENDENCE: {results[Constants.MARKET_TENDENCE]} \tIND_MED: {results[Constants.INDICATOR_MED]} \tDIRECTION: {results[Constants.DIRECTION]}  \tINDICATOR: {results[Constants.INDICATOR]} \tINDICATOR_TENDENCE: {results[Constants.INDICATOR_TENDENCE]} ")
        print(
            f"PRINT4 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_FLOW_STD: {results[Constants.WEEK_FLOW_STD]}  \tWEEK_FLOW_MED: {results[Constants.WEEK_FLOW_MED]} \tWEEK_FLOW_MED_LEVEL: {results[Constants.WEEK_FLOW_MED_LEVEL]}")
        print(
            f"PRINT41 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_FLOW_DIFF: {results[Constants.WEEK_FLOW_DIFF]} \tWEEK_FLOW_MED: {results[Constants.WEEK_FLOW_MED]} \tWEEK_FLOW_PREV_MED: {results[Constants.WEEK_FLOW_PREV_MED]} \tWEEK_FLOW_PREV: {results[Constants.WEEK_FLOW_PREV]} ")
        print(
            f"PRINT42 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR: {results[Constants.WEEK_DIR]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]} \tWEEK_DIR_TOP_DST: {results[Constants.WEEK_DIR_TOP_DST]}  \tWEEK_MIN_DIR: {results[Constants.WEEK_MIN_DIR]} \tWEEK_MAX_DIR: {results[Constants.WEEK_MAX_DIR]} ")

        print(
            f"PRINT43 ANALISIS  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR: {results[Constants.WEEK_DIR]} \tWEEK_DIR_FLOW_DIFF: {results[Constants.WEEK_DIR_FLOW_DIFF]}  \tWEEK_DIR_FLOW: {results[Constants.WEEK_DIR_FLOW]} \tWEEK_DIR_FLOW_PREV: {results[Constants.WEEK_DIR_FLOW_PREV]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]}   ")

        print(
            f"PRINT5 ANALISIS  {results[Constants.DATE].values[0]} IND_PROB_FLOW: {results[Constants.IND_PROB_FLOW]} \tIND_REL_FCST_PERCENT: {results[Constants.IND_REL_FCST_PERCENT]} \tIND_REL_FCST: {results[Constants.IND_REL_FCST]} \tIND_REL_FCST_STD: {results[Constants.IND_REL_FCST_STD]}  \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")
        print(
            f"PRINT6 ANALISIS  {results[Constants.DATE].values[0]} INDICATOR_MED: {results[Constants.INDICATOR_MED]} \tIND_MED_STD: {results[Constants.INDICATOR_MED_STD]} \tMED: {results[Constants.MEDIA]} \tSTDDESV: {results[Constants.STDDESV]}")
        print(
            f"PRINT7 ANALISIS  {results[Constants.DATE].values[0]} IND_REL_FCST_PERCENT: {results[Constants.IND_REL_FCST_PERCENT]} \tIND_REL_FCST_PREV_PERCENT: {results[Constants.IND_REL_FCST_PREV_PERCENT]} \tIND_REL_FCST: {results[Constants.IND_REL_FCST]} \tIND_REL_FCST_STD: {results[Constants.IND_REL_FCST_STD]}  \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")

        print(
            f"PRINT7.1 ANALISIS  {results[Constants.DATE].values[0]} IND_REL_FCST_STD: {results[Constants.IND_REL_FCST_STD]}  \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")

        print(
            f"PRINT8 ANALISIS  {results[Constants.DATE].values[0]} IND_REL_PERCENT_MED: {results[Constants.IND_REL_PERCENT_MED]} \tIND_REL_PERCENT_STD: {results[Constants.IND_REL_PERCENT_STD]} \tIND_REL_FCST_PERCENT: {results[Constants.IND_REL_FCST_PERCENT]} \tIND_REL_FCST_PREV_PERCENT: {results[Constants.IND_REL_FCST_PREV_PERCENT]}")

        print(
            f"PRINT9 ANALISIS  {results[Constants.DATE].values[0]} VALUE: {results[Constants.VALUE]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} RELATIVE_MIN: {results[Constants.RELATIVE_MIN]} \tRELATIVE_MAX: {results[Constants.RELATIVE_MAX]} ")

        print(
            f"PRINT10 ANALISIS  {results[Constants.DATE].values[0]} \tDIRECTION: {results[Constants.DIRECTION]} \tMIN_DIR: {results[Constants.MIN_DIR]} \tMAX_DIR: {results[Constants.MAX_DIR]} ")
        print(
            f"PRINT11 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_MED_STD: {results[Constants.INDICATOR_MED_STD]}  \tMEDSTDDIFF: {results[Constants.MEDSTDDIFF]} \tMEDIA: {results[Constants.MEDIA]} \tSTDDESV: {results[Constants.STDDESV]} ")
        print(
            f"PRINT12 ANALISIS  {results[Constants.DATE].values[0]} \tRELATIVE: {results[Constants.RELATIVE]} \tIND_REL_FCST_MED: {results[Constants.IND_REL_FCST_MED]} \tIND_REL_FCST_MIN: {results[Constants.IND_REL_FCST_MIN]} \tIND_REL_FCST_MAX: {results[Constants.IND_REL_FCST_MAX]} ")

        print(
            f"PRINT13 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_MED_DAY: {results[Constants.INDICATOR_MED_DAY]} \tINDICATOR_STD_DAY: {results[Constants.INDICATOR_STD_DAY]} \tINDICATOR_MED_DAYS: {results[Constants.INDICATOR_MED_DAYS]} \tINDICATOR_STD_DAYS: {results[Constants.INDICATOR_STD_DAYS]} ")

        print(
            f"PRINT14 ANALISIS  {results[Constants.DATE].values[0]} \tIND_MED_DAY: {results[Constants.IND_MED_DAY]} \t VALUE_DIFFMED: {results[Constants.VALUE_DIFFMED]} \t VALUE: {results[Constants.VALUE]}  \tIND_SUM_UP: {results[Constants.IND_SUM_UP]} \tIND_NUM_UP: {results[Constants.IND_NUM_UP]} \tIND_SUM_DOWN: {results[Constants.IND_SUM_DOWN]} \tIND_NUM_DOWN: {results[Constants.IND_NUM_DOWN]} ")
        print(
            f"PRINT15 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_DISTANCE: {results[Constants.INDICATOR_DISTANCE]} \tINDICATOR: {results[Constants.INDICATOR]} \tIMA5MA20: {results[Constants.IMA5MA20]} ")
        print(
            f"PRINT16 ANALISIS  {results[Constants.DATE].values[0]} \tIND_MED_DAY: {results[Constants.IND_MED_DAY]} \tIND_SUM_UP_DAYS: {results[Constants.IND_SUM_UP_DAYS]} \tIND_NUM_UP_DAYS: {results[Constants.IND_NUM_UP_DAYS]} \tIND_SUM_DOWN_DAYS: {results[Constants.IND_SUM_DOWN_DAYS]} \tIND_NUM_DOWN_DAYS: {results[Constants.IND_NUM_DOWN_DAYS]} ")
        print(
            f"PRINT17 ANALISIS  {results[Constants.DATE].values[0]} \tINDICATOR_EMA: {results[Constants.INDICATOR_EMA]} \tEMA_DST: {results[Constants.EMA_DST]} \tINDICATOR_EMA_CHECK: {results[Constants.INDICATOR_EMA_CHECK]}")
        print(
            f"PRINT18 ANALISIS  {results[Constants.DATE].values[0]} \tIND_BLG: {results[Constants.IND_BLG]} \tIND_BLG_MED_DST: {results[Constants.IND_BLG_MED_DST]} \tIND_BLG_UPPER_DST: {results[Constants.IND_BLG_UPPER_DST]} \tIND_BLG_LOWER_DST: {results[Constants.IND_BLG_LOWER_DST]} \tCLOSE_NXT_UP: {results[Constants.CLOSE_NXT_UP]} \tCLOSE_NXT_DOWN: {results[Constants.CLOSE_NXT_DOWN]}")
        print(
            f"PRINT19 ANALISIS  {results[Constants.DATE].values[0]} \tIND_BLG: {results[Constants.IND_BLG]} \tIND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]}  \tIND_BLG_MIDDLE_DST_PERCENT: {results[Constants.IND_BLG_MIDDLE_DST_PERCENT]} \tANGLE: {results[Constants.ANGLE]} \tANGLEm1: {results[Constants.ANGLEm1]}")

        print(
            f"PRINT20 ANALISIS  {results[Constants.DATE].values[0]} \tINTERVAL: {results[Constants.INTERVAL]} \tANGLE: {results[Constants.ANGLE]}  \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_EMA: {results[Constants.ANGLE_EMA]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE_EMA_FLOW: {results[Constants.ANGLE_EMA_FLOW]}\tANGLEm1: {results[Constants.ANGLEm1]} \tANGLEm21: {results[Constants.ANGLEm21]}\tMARKET_ANGLE_TANG: {results[Constants.MARKET_ANGLE_TANG]}\tMARKET_ANGLE: {results[Constants.MARKET_ANGLE]}\tIND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} ")

        print(
            f"PRINT21 ANALISIS  {results[Constants.DATE].values[0]} \tCLOSE_NXT_UP: {results[Constants.CLOSE_NXT_UP]} \tCLOSE_NXT_DOWN: {results[Constants.CLOSE_NXT_DOWN]} \tCLOSE_NXT_MIDDLE: {results[Constants.CLOSE_NXT_MIDDLE]} \tINTERVAL: {results[Constants.INTERVAL]}")

        print(
            f"PRINT22 ANALISIS  {results[Constants.DATE].values[0]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]} \tWEEK_DIR_TOP_DST: {results[Constants.WEEK_DIR_TOP_DST]}  \tIND_BLG_UPPER_DST_PERCENT: {results[Constants.IND_BLG_UPPER_DST_PERCENT]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]}  \tIND_BLG_MIDDLE_DST_PERCENT: {results[Constants.IND_BLG_MIDDLE_DST_PERCENT]} ")


        print(
            f"PRINTCUSTOM ANALISIS  {results[Constants.DATE].values[0]} IMA1: {results[Constants.IMA1]} \tANGLE: {results[Constants.ANGLE]} \tANGLEm1: {results[Constants.ANGLEm1]} \tINDICATOR_MED_MOMENT: {results[Constants.INDICATOR_MED_MOMENT]} \tINDICATOR: {results[Constants.INDICATOR]} \tIND_MED: {results[Constants.INDICATOR_MED]}  \tDIRECTION: {results[Constants.DIRECTION]} \tIMA1_DIS :{results[Constants.IMA1_DISTANCE]}")

        print(
            f"PRINTCUSTOM ANALISIS01  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR_FLOW_DIFF: {results[Constants.WEEK_DIR_FLOW_DIFF]} \tANGLE: {results[Constants.ANGLE]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]}  \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_EMA_FLOW: {results[Constants.ANGLE_EMA_FLOW]} \tANGLEm1: {results[Constants.ANGLEm1]} \tANGLE_EMA: {results[Constants.ANGLE_EMA]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tDIRECTION: {results[Constants.DIRECTION]} \tIMA1_DIS :{results[Constants.IMA1_DISTANCE]}")

        print(
            f"PRINTCUSTOM ANALISISFLOW01  {results[Constants.DATE].values[0]} WEEK_FLOW: {results[Constants.WEEK_FLOW]} \tWEEK_DIR: {results[Constants.WEEK_DIR]} \tWEEK_DIR_FLOW_DIFF: {results[Constants.WEEK_DIR_FLOW_DIFF]}  \tWEEK_DIR_FLOW: {results[Constants.WEEK_DIR_FLOW]} \tANGLE: {results[Constants.ANGLE]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]}  \tWEEK_DIR_BOT_DST_PREV: {results[Constants.WEEK_DIR_BOT_DST_PREV]} ")

        print(
            f"PRINTCUSTOM ANALISISFLOW02  {results[Constants.DATE].values[0]} \tIND_PROB_FLOW: {results[Constants.IND_PROB_FLOW]} \tIMA1EMADIFF: {results[Constants.IMA1EMADIFF]} \tANGLE_EMA20: {results[Constants.ANGLE_EMA20]} \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tIND_BLG_LOWER_DST_PERCENT: {results[Constants.IND_BLG_LOWER_DST_PERCENT]} \tWEEK_DIR_BOT_DST: {results[Constants.WEEK_DIR_BOT_DST]}  \tWEEK_DIR_BOT_DST_PREV: {results[Constants.WEEK_DIR_BOT_DST_PREV]} ")

        print(
            f"PRINTCUSTOM ANALISISFLOW03  {results[Constants.DATE].values[0]} \tANGLE: {results[Constants.ANGLE]} \tHOURLY_ANGLE: {results[Constants.HOURLY_ANGLE]} \tHOURLY_ANGLE_MED: {results[Constants.HOURLY_ANGLE_MED]}  \tHOURLY_ANGLE_MED_PREV: {results[Constants.HOURLY_ANGLE_MED_PREV]}\tANGLE_FLOW: {results[Constants.ANGLE_FLOW]} \tANGLE_COUNTER: {results[Constants.ANGLE_COUNTER]} \tANGLE_PREV: {results[Constants.ANGLE_PREV]} \tANGLE_IMA1: {results[Constants.ANGLE_IMA1]} \tANGLE_IMA1_PREV: {results[Constants.ANGLE_IMA1_PREV]} \tANGLE_IMA1_COUNTER: {results[Constants.ANGLE_IMA1_COUNTER]}")

    def prepareBESTDISTANCE(self, results):
        prev = results[Constants.ACUMULADO_ABS]
        if abs(prev) < 2 and abs(prev)!=0:
            self.diffValues.append(abs(prev))

    # @mide_tiempo
    def calculateBESTDISTANCE(self):
        # cambios = [valor - self.diffValues[-1] for valor in self.diffValues]
        print(f"{self.diffValues}")
        if len(self.diffValues) > 0:
            desviacion_estandar = np.std(self.diffValues)
            media = np.mean(self.diffValues)
            import statistics as stats
            median = stats.median_grouped(self.diffValues)
            print(f" PRINTDIFF ANALISIS DIFF_MED: {media}  DIFF_STD: {desviacion_estandar} median group: {median}")

    def applyNewAction(self, results, active, isFcst=False, doubleAction = False):
        fastReview = self.evaluateNewAction(results, active, False, isFcst)
        if self.useConfig == False:
            # update DATABASE
            if doubleAction==True:
                results[Constants.CURRENT_ACTION]= 'CLOSE-'+results[Constants.CURRENT_ACTION]
            self.dataBDMan.updateValueWithData(results)
        else:
            self.updateConfig(active, results)

    def closeAndNewAction(self, results, active, action, isFcst=False):
        try:
            self.closeAndNewActionRetry(results, active, action, isFcst)

        except Exception as e:
            print(f"ERROR closeAndNewAction {str(e)}")
            message = f"{self.name}  fallo closeAndNewAction  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            try:
                # time.sleep(2)
                self.closeAndNewActionRetry(results, active, action, isFcst)
            except Exception as e:
                print(f"ERROR closeAndNewAction {str(e)}")
                message = f"{self.name}  fallo closeAndNewAction  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"

    def closeAndNewActionRetry(self, results, active, action, isFcst=False):
        results[Constants.NEW_ACTION] = Constants.ACTION_CLOSE
        self.applyNewAction(results, active, isFcst)
        if self.simulation == False:
            nada = ""
            # time.sleep(4)
        results[Constants.NEW_ACTION] = action
        self.applyNewAction(results, active, isFcst, doubleAction=True)
        if self.simulation == False:
            message = f"{self.name}  EXITO closeAndNewAction  {results[Constants.CURRENT_ACTION]} para {active.parameters.name}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)

    # @mide_tiempo
    def evaluateFcstPROB(self, results, active):
        try:
            currentTime = self.gettime(results)
            fcst = results[Constants.IND_REL_FCST]
            msg = None
            probFlow = results[Constants.IND_PROB_FLOW]
            if currentTime and currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
                if "FINAL_"+ active.parameters.name in results:
                    if results["FINAL_"+ active.parameters.name] =='1':
                        results["FINAL_" + active.parameters.name] = '0'
                        results[Constants.INICIO_NAME] = "PROB_CLOSE_"+active.parameters.endProbDef
                        if (probFlow == Constants.DIR_UP or probFlow == Constants.DIR_PRE_UP):
                            # up

                            if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                if active.parameters.continueFlow== False:
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    print(f"ACTIVO FCST 1530 CLOSE-BUY!!!")
                                    msg = f"{self.name} ACTIVO FCST 2150 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.closeAndNewAction(results, active, Constants.ACTION_BUY)

                            elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(f"ACTIVO FCST 2150 BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 2150 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.closeAndNewAction(results, active, Constants.ACTION_BUY)
                            elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION] or results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(f"ACTIVO FCST 2150 BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 2150 BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.applyNewAction(results, active)
                        elif (probFlow == Constants.DIR_DOWN or probFlow == Constants.DIR_PRE_DOWN):
                            if active.parameters.name != 'BTCUSD' and active.parameters.name != 'ETHUSD':
                                # down
                                if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                    print(f"ACTIVO FCST 2150 SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 2150 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    self.closeAndNewAction(results, active, Constants.ACTION_SELL)
                                elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                    if active.parameters.continueFlow == False:
                                        print(f"ACTIVO FCST 1530 CLOSE-SELL!!!")
                                        msg = f"{self.name} ACTIVO FCST 2150 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                        self.closeAndNewAction(results, active, Constants.ACTION_SELL)

                                elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION] or results[Constants.CURRENT_ACTION] == Constants.ACTION_WAIT:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    print(f"ACTIVO FCST 2150 SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 2150 SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.applyNewAction(results, active)

            if currentTime and currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
                if "INIT_"+ active.parameters.name in results:
                    if results["INIT_"+ active.parameters.name] =='1':
                        results["INIT_" + active.parameters.name] = '0'
                        results[Constants.INICIO_NAME] = "PROB_START_"+active.parameters.startProbDef
                        if (probFlow == Constants.DIR_UP or probFlow == Constants.DIR_PRE_UP):
                            # up
                            if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                if active.parameters.continueFlow == False:
                                    # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                    print(f"ACTIVO FCST 1530 CLOSE-BUY!!!")
                                    msg = f"{self.name} ACTIVO FCST 1530 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.closeAndNewAction(results, active, Constants.ACTION_BUY)


                            elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                # results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(f"ACTIVO FCST 1530 CLOSE-BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 1530 CLOSE-BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.closeAndNewAction(results, active, Constants.ACTION_BUY)

                            elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION]:
                                results[Constants.NEW_ACTION] = Constants.ACTION_BUY
                                print(f"ACTIVO FCST 1530 BUY!!!")
                                msg = f"{self.name} ACTIVO FCST 1530 BUY for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                self.applyNewAction(results, active)

                        elif (probFlow == Constants.DIR_DOWN or probFlow == Constants.DIR_PRE_DOWN):
                            # down
                            if active.parameters.name != 'BTCUSD' and active.parameters.name != 'ETHUSD':
                                if results[Constants.CURRENT_ACTION] == Constants.ACTION_BUY:
                                    print(f"ACTIVO FCST 1530 CLOSE-SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 1530 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.closeAndNewAction(results, active, Constants.ACTION_SELL)

                                elif results[Constants.CURRENT_ACTION] == Constants.ACTION_SELL:
                                    if active.parameters.continueFlow == False:
                                        print(f"ACTIVO FCST 1530 CLOSE-SELL!!!")
                                        msg = f"{self.name} ACTIVO FCST 1530 CLOSE-SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                        self.closeAndNewAction(results, active, Constants.ACTION_SELL)

                                elif Constants.ACTION_CLOSE in results[Constants.CURRENT_ACTION]:
                                    results[Constants.NEW_ACTION] = Constants.ACTION_SELL
                                    print(f"ACTIVO FCST 1530 SELL!!!")
                                    msg = f"{self.name} ACTIVO FCST 1530 SELL for {active.parameters.name} action: {results[Constants.IND_PROB_FLOW]}"
                                    self.applyNewAction(results, active)

            if msg is not None and self.simulation == False:
                self.telegram.enviarMensaje(msg, self.telegram.tokenBot, active.parameters.tele_group)
        except Exception as e:
            print(f"ERROR evaluateFcstPROB {str(e)}")
            message = f"{self.name}  fallo enevaluateFcst  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(e)
            print(f"fallo change state for {active.parameters.name} second: {active.parameters.second_name}")

    def evaluateCloseAction(self, active, results):
        fastReview = False
        currentTime = self.gettime(results)

        if currentTime and currentTime >= int(self.closeStart) and currentTime < int(self.closeEnd):
                #solo si no ha hecho predicciones
                active.parameters.controlWin = True
                fastReview = True
        elif currentTime and currentTime >= int(self.iniStart) and currentTime < int(self.iniEnd):
                #solo si no ha hecho predicciones
                active.parameters.controlWin = True
                fastReview = True


        return fastReview

    def isHour(self, results):
        res = False
        currentTime = None
        from datetime import datetime
        if results[Constants.SIMULATION]:
            temp = results[Constants.DATE].values[0]
            t = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
            current_time_h = t.hour * 100
            current_time_min = t.minute
            # print(f" gettime hora : {current_time_h} minutos: {current_time_min}")
            currentTime = int(current_time_h + current_time_min)
        else:
            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            if current_time_min == 0:
                isHour = True
            currentTime = int(current_time_min)
        # Definir un rango de tolerancia en minutos
        tolerancia_minutos = 5

        # Verificar si el valor de t está cerca de una hora en punto
        minutos = t.minute
        segundos = t.second

        # Calcular la diferencia en minutos y segundos con la hora exacta
        if minutos <= tolerancia_minutos:
            res = True
            # print(f"isHour current time hour: {current_time_h} minutes :{current_time_min}")

        return res

    # @mide_tiempo
    def calculateHourlyFlow(self, data, results, active):
        data2 = data
        if not isinstance(data2.index, pd.DatetimeIndex):
            data2.index = pd.to_datetime(data2['date'])
        df_hourly = data.resample('1H').first()
        # df_half = data.resample('30T').first()
        df_hourly = df_hourly.dropna()



        # Boollinger
        boolinger = active.parameters.bollinger
        blgMA = df_hourly[self.closeValue].rolling(window=boolinger).mean()
        # EMA_10 = talib.EMA(df_hourly[self.closeValue], timeperiod=10)
        EMA_10 = df_hourly[self.closeValue].ewm(span=10, adjust=False).mean()

        blgMAm0 = EMA_10.iloc[[-1]]
        hourlyM0 = df_hourly.iloc[-1]
        hourlyM2 = None
        blgMAm2 = None
        blgMAm3 = None
        anlgeblgm0 = 0
        hourlyM1 = None
        interval = 30

        results[Constants.HOURLY_ANGLE] = 0
        results[Constants.HOURLY_ANGLE_MED] = 0
        results[Constants.HOURLY_ANGLE_MED_PREV] = 0
        # try:
        #     interval = abs(self.calcular_minutos_entre_fechas(df_hourly.iloc[-1]['date'], data.iloc[-2]['date']))
        #     # angleEMA20 = np.arctan(EMA_20.values[-1] - EMA_20.values[-2]) * (180 / np.pi)
        # except Exception as error:
        #     interval = 30

        # if interval > 60:
        #     interval = 1
        # elif interval < 30:
        #     if "BTCUSD" in active.parameters.name or "ETHUSD" in active.parameters.name:
        #         nada = ""
        #     else:
        #         if interval <= 15:
        #             if self.activeHelper.angleExclusion(results, active.parameters.name):
        #                 interval = interval / 1000
        #             else:
        #                 interval = interval / 100
        #         else:
        #             interval = 1

        # results[Constants.INTERVAL] = interval
        try:
            blgMAm1 = EMA_10.iloc[[-2]]
        except Exception as error:
            blgMAm1 = None

        try:
            blgMAm2 = EMA_10.iloc[[-3]]
        except Exception as error:
            blgMAm2 = None

        try:
            hourlyM1 = df_hourly.iloc[-2]
        except Exception as error:
            hourlyM1 = None



        if blgMAm1 is not None:
            if pd.isna(blgMAm1.values[0]) is not True:
                anlgeblgm0 = math.degrees(math.atan2(blgMAm0.values[0] - blgMAm1.values[0], 1))
                nada = ""
            if pd.isna(anlgeblgm0) is True:
                anlgeblgm0 = 0
            # print(f" angle m0 : {anlgeblgm0}")
            results[Constants.HOURLY_ANGLE_MED] = anlgeblgm0

        if blgMAm2 is not None:
            if pd.isna(blgMAm2.values[0]) is not True:
                anlgeblgm0 = math.degrees(math.atan2(blgMAm1.values[0] - blgMAm2.values[0], 1))
                nada = ""
            if pd.isna(anlgeblgm0) is True:
                anlgeblgm0 = 0
            # print(f" angle m0 : {anlgeblgm0}")
            results[Constants.HOURLY_ANGLE_MED_PREV] = anlgeblgm0

        if hourlyM1 is not None:
            if pd.isna(hourlyM1.values[0]) is not True:
                anlgeblgm0 = math.degrees(math.atan2(hourlyM0.values[1] - hourlyM1.values[1], 1))
                nada = ""
            if pd.isna(anlgeblgm0) is True:
                anlgeblgm0 = 0
            # print(f" angle m0 : {anlgeblgm0}")
            results[Constants.HOURLY_ANGLE] = anlgeblgm0

    def collectFlowAnalisis(self, data, results, active):
        dataTemp = {}
        dataTemp['date'] = results[Constants.DATE].values[0]
        dataTemp['value'] = results[Constants.VALUE]

        if self.showAnallisisFlow:
            if self.drawnEMA_UPDOWN:
                if results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_BUY:
                    self.operations.tendenceUP.append(dataTemp)
                elif results[Constants.INDICATOR_EMA] == Constants.INDICATOR_EMA_SELL:
                    self.operations.tendenceDOWN.append(dataTemp)
                else:
                    self.operations.tendenceWAIT.append(dataTemp)

    def postcalculation(self, data, results, active):

        # UPDATE COUNTER
        angleimaPrev = float(results[Constants.ANGLE_IMA1_PREV])
        angleIma1 = float(results[Constants.ANGLE_IMA1])
        angleImaCounter = int(float(results[Constants.ANGLE_IMA1_COUNTER]))
        angle = float(results[Constants.ANGLE])
        anglePrev = float(results[Constants.ANGLE_PREV])
        angleCounter = int(float(results[Constants.ANGLE_COUNTER]))
        if angleimaPrev != 0:
            if angleimaPrev > 0:
                if angleIma1 > 0:
                    angleImaCounter = angleImaCounter + 1
                else:
                    angleImaCounter = 1
            else:
                if angleIma1 < 0:
                    angleImaCounter = angleImaCounter + 1
                else:
                    angleImaCounter = 1

        if anglePrev != 0:
            if anglePrev > 0:
                if angle > 0:
                    angleCounter = angleCounter + 1
                else:
                    angleCounter = 1
            else:
                if angle < 0:
                    angleCounter = angleCounter + 1
                else:
                    angleCounter = 1
        results[Constants.ANGLE_IMA1_COUNTER] = angleImaCounter
        results[Constants.ANGLE_COUNTER] = angleCounter


    def evaluateActions(self, data, results, active, isFastReview=False):
        fastReview = isFastReview
        try:
            #init values
            results[Constants.SIMULATION] = self.simulation
            results[Constants.ISDBDATA] = self.isDBData
            results[Constants.ONLY_START_END] = self.onlyStartEnd




            self.evaluateIndicators(data, results, active)
            self.evaluateActiveIndicators(results,data, active)
            self.review_results(data, results, active)

            results[Constants.HOURLY_ANGLE] = 0
            results[Constants.HOURLY_ANGLE_MED] = 0
            results[Constants.HOURLY_ANGLE_MED_PREV] = 0
            # self.calculateHourlyFlow(data, results, active)
            # if self.isHour(results):
            #     self.calculateHourlyFlow(data, results, active)
            # else:
            self.collectFlowAnalisis(data,results,active)
            self.postcalculation(data,results,active)
            # if self.simulation:
            startTimeForToday= self.getfirstValueForToday(data,results)
            if startTimeForToday < 1500:

                self.prepare1430()
            else:
                self.updateTimeZoneValues(results)

            # self.calculatePrevRelativeValues(results,active)

            # calula la medi y desviacion para el dia y acumulado de dias
            self.calculatePredictionIndicator(data, results, active)

            if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                self.calculateSpecialIndicatorsBTCETH(results, active)
            else:
                self.calculateSpecialIndicators(results, active)

            self.calculateMinMax(results, data, active)
            self.executeAnalisisHelperMINMAXFlow(results, data, active)
            self.evaluateFinalIndicators(results, data, active)



            # calular los valores de probabilidad final
            try:
                probFlow = self.getPROBMEDSTD_NEWFlow(results, active)
                if probFlow:
                    results[Constants.IND_PROB_FLOW] = probFlow
            except Exception as e:
                print(f"error getPROBMEDSTD_NEWFlow {str(e)}")

            # LLAMA AL EVALUADOR
            active.evaluate(results)
            if self.simulation:
                self.prepareBESTDISTANCE(results)
                if self.needAnalsis:
                    self.printAnalisis(results, active)

            # activa cierres de ganancia puntual y evalua la prediccion a ciertas horas
            # isFastReview = self.evaluateCloseAction(active, results)

            fastReview = self.evaluateNewAction(results, active, isFastReview)

            if self.useConfig == False:
                # update DATABASE
                self.dataBDMan.updateValueWithData(results)
            else:
                self.updateConfig(active, results)
                if self.updateDBSimulation:
                    self.dataBDMan.updateSimulationValues(results)
                    # self.dataBDMan.update_market(results)
            # print(f"active {active.parameters.name} ingnoreProb es {active.parameters.ignoreProb}")
            # EJECUTA la nueva accion en caso de ser distinta a la actual lo hace en horarios
            if self.disableInitProb == False and active.parameters.ignoreProb == False:
                if active.parameters.name == "BTCUSD" or active.parameters.name == "ETHUSD":
                    nada = ""
                else:
                    self.evaluateFcstPROB(results, active)


        except Exception as e:
            fastReview = False
            print(f"ERROR evaluateActions {str(e)}")
            message = f"{self.name} fallo evaluateActions  {results[Constants.CURRENT_ACTION]} para {active.parameters.name} error: {str(e)}"
            self.telegram.enviarMensaje(message, self.telegram.tokenBot, self.errorTelegroup)
            self.addmessages(message, results)
            print(e)
            print(f"fallo change state for {active.parameters.name} second: {active.parameters.second_name}")

        return fastReview

    def inserDataPrices(self, value, active):
        data = None
        try:

            t = time.localtime()
            current_time_h = time.strftime("%H", t)
            current_time_min = time.strftime("%M", t)
            print(f" hora : {current_time_h} minutos: {current_time_min}")

            current_value = float(value[self.closeValue])
            fecha = value['date'].values[0]
            weekno = datetime.datetime.today().weekday()
            days = 2
            if weekno == 0:
                days = 3

            dif = 0
            acu = 0
            acumulate = 0
            tendence_acu = 0
            tendence_count = 0
            oldvalue = 0
            min_value = 999
            min_acu = 0
            max_value = 0
            max_acu = 0
            direction = Constants.DIR_WAIT
            min_dir = 99999
            max_dir = 0
            indi_dir = ''
            action = Constants.ACTION_WAIT
            oldDBvalue = self.dataBDMan.getLastValueWithName(active.parameters.name)
            if oldDBvalue is not None:
                oldvalue = oldDBvalue[0]["value"]

                acumulate = oldDBvalue[0]["acumulate"]
                tendence_acu = oldDBvalue[0]["tendence_acu"]
                tendence_count = oldDBvalue[0]["tendence_count"]
                min_value = oldDBvalue[0]["min_value"]
                min_acu = oldDBvalue[0]["min_acu"]
                max_value = oldDBvalue[0]["max_value"]
                max_acu = oldDBvalue[0]["max_acu"]
                action = oldDBvalue[0]["action"]
                direction = oldDBvalue[0]["direction"]
                min_dir = oldDBvalue[0]["min_dir"]
                max_dir = oldDBvalue[0]["max_dir"]
                indi_dir = oldDBvalue[0]["indi_dir"]
                action_acum = oldDBvalue[0]["action_acum"]
                action_count = oldDBvalue[0]["action_count"]

            self.dataBDMan.inserValue(active.parameters.name, current_value, oldvalue, dif, acumulate, tendence_acu,
                                      tendence_count, min_value,
                                      max_value, min_acu, max_acu, direction, min_dir, max_dir, indi_dir, action_acum,
                                      action_count, action, dateValue=fecha)

            data = self.dataBDMan.getAllWithNameForXdays(active.parameters.name, days)
            # if data is not None:
            # self.log.info(data)
            # oldvalue = oldDBvalue[0]["value"]

        except Exception as e:
            print(f"ERROR inserDataPrices {str(e)}")

        return data

    def search_prices_list_data_simulation(self, actives, data):
        res = None
        for active in actives:
            results = {}

            if data.empty == False and len(data) > 0:
                fastReview = self.evaluateActions(data, results, active)
                # if fastReview == True:
                #     self.evaluateActions(data, results, active,True)
            res = results
        return res

    def search_prices_list_data_simulation_INSERT(self, actives, dataSimulate):

        for active in actives:
            results = {}
            # self.reviewControls(data, active)
            data = self.inserDataPrices(dataSimulate, active)
            if data and len(data) > 0:
                self.evaluateActions(data, results, active)
                if active.parameters.reevaluateAction:
                    self.evaluateActions(data, results, active)

