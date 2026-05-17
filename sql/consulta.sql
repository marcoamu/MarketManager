SELECT SUM(REVENUE), NAME from MARKET where datevalue >= '2026-03-30 00:00:00' and datevalue <= '2026-03-30 23:00:00' and action='CLOSE' group by name order by sum(revenue) asc

SELECT SUM(profit), NAME from MARKET where datevalue >= '2026-03-30 00:00:00' and datevalue <= '2026-03-30 23:00:00' and action='CLOSE' group by name order by sum(profit) asc



