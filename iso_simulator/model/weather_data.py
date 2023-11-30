class WeatherData:

    def __init__(self,
                 year, month, day, hour, minute, datasource, drybulb_C, dewpoint_C, relhum_percent,
                 atmos_Pa, exthorrad_Whm2, extdirrad_Whm2, horirsky_Whm2, glohorrad_Whm2,
                 dirnorrad_Whm2, difhorrad_Whm2, glohorillum_lux, dirnorillum_lux, difhorillum_lux,
                 zenlum_lux, winddir_deg, windspd_ms, totskycvr_tenths, opaqskycvr_tenths, visibility_km,
                 ceiling_hgt_m, presweathobs, presweathcodes, precip_wtr_mm, aerosol_opt_thousandths,
                 snowdepth_cm, days_last_snow, Albedo, liq_precip_depth_mm, liq_precip_rate_Hour,
                 ):

        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.datasource = datasource
        self.drybulb_C = drybulb_C
        self.dewpoint_C = dewpoint_C
        self.relhum_percent = relhum_percent
        self.atmos_Pa = atmos_Pa
        self.exthorrad_Whm2 = exthorrad_Whm2
        self.extdirrad_Whm2 = extdirrad_Whm2
        self.horirsky_Whm2 = horirsky_Whm2
        self.glohorrad_Whm2 = glohorrad_Whm2
        self.dirnorrad_Whm2 = dirnorrad_Whm2
        self.difhorrad_Whm2 = difhorrad_Whm2
        self.glohorillum_lux = glohorillum_lux
        self.dirnorillum_lux = dirnorillum_lux
        self.difhorillum_lux = difhorillum_lux
        self.zenlum_lux = zenlum_lux
        self.winddir_deg = winddir_deg
        self.windspd_ms = windspd_ms
        self.totskycvr_tenths = totskycvr_tenths
        self.opaqskycvr_tenths = opaqskycvr_tenths
        self.visibility_km = visibility_km
        self.ceiling_hgt_m = ceiling_hgt_m
        self.presweathobs = presweathobs
        self.presweathcodes = presweathcodes
        self.precip_wtr_mm = precip_wtr_mm
        self.aerosol_opt_thousandths = aerosol_opt_thousandths
        self.snowdepth_cm = snowdepth_cm
        self.days_last_snow = days_last_snow
        self.Albedo = Albedo
        self.liq_precip_depth_mm = liq_precip_depth_mm
        self.liq_precip_rate_Hour = liq_precip_rate_Hour
