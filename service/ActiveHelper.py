import datetime
import time

from evaluators.Evaluator01 import Evaluator01
from evaluators.Evaluator02 import Evaluator02
from evaluators.Evaluator03 import Evaluator03
from evaluators.Evaluator04 import Evaluator04
from evaluators.EvaluatorBOLLINGER_00 import EvaluatorBOLLINGER_00
from evaluators.EvaluatorBOLLINGER_01 import EvaluatorBOLLINGER_01
from evaluators.EvaluatorBOLLINGER_02 import EvaluatorBOLLINGER_02
from evaluators.EvaluatorBOLLINGER_03 import EvaluatorBOLLINGER_03
from evaluators.EvaluatorBOLLINGER_04 import EvaluatorBOLLINGER_04
from evaluators.EvaluatorBOLLINGER_05 import EvaluatorBOLLINGER_05
from evaluators.EvaluatorBOLLINGER_05_IMP_01 import EvaluatorBOLLINGER_05_IMP_01
from evaluators.EvaluatorBOLLINGER_06 import EvaluatorBOLLINGER_06
from evaluators.EvaluatorBOLLINGER_07 import EvaluatorBOLLINGER_07
from evaluators.EvaluatorBOLLINGER_08 import EvaluatorBOLLINGER_08
from evaluators.EvaluatorBOLLINGER_09 import EvaluatorBOLLINGER_09
from evaluators.EvaluatorBOLLINGER_LARGE_01 import EvaluatorBOLLINGER_LARGE_01
from evaluators.EvaluatorBOLLINGER_LARGE_02 import EvaluatorBOLLINGER_LARGE_02
from evaluators.EvaluatorBOLLINGER_LARGE_03 import EvaluatorBOLLINGER_LARGE_03
from evaluators.EvaluatorBOLLINGER_ONLY_UP_01 import EvaluatorBOLLINGER_ONLY_UP_01
from evaluators.EvaluatorBOLLINGER_ONLY_UP_02 import EvaluatorBOLLINGER_ONLY_UP_02
from evaluators.EvaluatorBOLLINGER_ONLY_UP_03 import EvaluatorBOLLINGER_ONLY_UP_03
from evaluators.EvaluatorBOLLINGER_ONLY_UP_03_01 import EvaluatorBOLLINGER_ONLY_UP_03_01
from evaluators.EvaluatorDIRECTION_CLEAN_Opt01 import EvaluatorDIRECTION_CLEAN_Opt01
from evaluators.EvaluatorDIRECTION_CLEAN_Opt02 import EvaluatorDIRECTION_CLEAN_Opt02
from evaluators.EvaluatorDIRECTION_CLEAN_Opt03 import EvaluatorDIRECTION_CLEAN_Opt03
from evaluators.EvaluatorDIRECTION_CLEAN_Opt03_MEDDIFF_01 import EvaluatorDIRECTION_CLEAN_Opt03_MEDDIFF_01
from evaluators.EvaluatorDIRECTION_CLEAN_Opt04 import EvaluatorDIRECTION_CLEAN_Opt04
from evaluators.EvaluatorDIRECTION_CLEAN_Opt05 import EvaluatorDIRECTION_CLEAN_Opt05
from evaluators.EvaluatorDIRECTION_MEDSTD_01 import EvaluatorDIRECTION_MEDSTD_01
from evaluators.EvaluatorDIRECTION_MEDSTD_02 import EvaluatorDIRECTION_MEDSTD_02
from evaluators.EvaluatorDIRECTION_MEDSTD_03 import EvaluatorDIRECTION_MEDSTD_03
from evaluators.EvaluatorDIRECTION_MEDSTD_03_MEDDIFF import EvaluatorDIRECTION_MEDSTD_03_MEDDIFF
from evaluators.EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_01 import EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_01
from evaluators.EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_02 import EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_02
from evaluators.EvaluatorDIRECTION_MEDSTD_04 import EvaluatorDIRECTION_MEDSTD_04
from evaluators.EvaluatorDIRECTION_PROB_Opt01 import EvaluatorDIRECTION_PROB_Opt01
from evaluators.EvaluatorDIRECTION_PROB_Opt02 import EvaluatorDIRECTION_PROB_Opt02
from evaluators.EvaluatorDirectionMEDSTD01 import EvaluatorDirectionMEDSTD01
from evaluators.EvaluatorDirectionMEDSTD02 import EvaluatorDirectionMEDSTD02
from evaluators.EvaluatorDirectionMEDSTD03 import EvaluatorDirectionMEDSTD03
from evaluators.EvaluatorDirectionMEDSTD03_01 import EvaluatorDirectionMEDSTD03_01
from evaluators.EvaluatorDirectionMEDSTD04 import EvaluatorDirectionMEDSTD04
from evaluators.EvaluatorDirectionMEDSTD_MEDDIFF_01 import EvaluatorDirectionMEDSTD_MEDDIFF_01
from evaluators.EvaluatorDistIndicatorTenOnlyUp01 import EvaluatorDistIndicatorTenOnlyUp01
from evaluators.EvaluatorDistIndicatorTendence01 import EvaluatorDistIndicatorTendence01
from evaluators.EvaluatorDistIndicatorTendence02 import EvaluatorDistIndicatorTendence02
# from evaluators.EvaluatorDistIndicatorTendence03 import EvaluatorDistIndicatorTendence03
from evaluators.EvaluatorDistIndicatorTendence03 import EvaluatorDistIndicatorTendence03
from evaluators.EvaluatorDistMarketTenOnlyUp01 import EvaluatorDistMarketTenOnlyUp01
from evaluators.EvaluatorDistMarketTenOptimiz00 import EvaluatorDistMarketTenOptimiz00
from evaluators.EvaluatorDistMarketTenOptimiz01 import EvaluatorDistMarketTenOptimiz01
from evaluators.EvaluatorDistMarketTenOptimiz02 import EvaluatorDistMarketTenOptimiz02
from evaluators.EvaluatorDistMarketTenOptimiz03 import EvaluatorDistMarketTenOptimiz03
from evaluators.EvaluatorDistMarketTendence01 import EvaluatorDistMarketTendence01
from evaluators.EvaluatorDistMarketTendence02 import EvaluatorDistMarketTendence02
from evaluators.EvaluatorDistMarketTendence03 import EvaluatorDistMarketTendence03
from evaluators.EvaluatorDistMarketTendence04 import EvaluatorDistMarketTendence04
from evaluators.EvaluatorDistMarketTendence05 import EvaluatorDistMarketTendence05
from evaluators.EvaluatorDistMarketTendence06 import EvaluatorDistMarketTendence06
from evaluators.EvaluatorDistMarketTendence07 import EvaluatorDistMarketTendence07
from evaluators.EvaluatorDistMarketTendence08 import EvaluatorDistMarketTendence08
from evaluators.EvaluatorDistMarketTendence09 import EvaluatorDistMarketTendence09
from evaluators.EvaluatorDistMarketTendence10 import EvaluatorDistMarketTendence10
from evaluators.EvaluatorDistMarketTendence11 import EvaluatorDistMarketTendence11
from evaluators.EvaluatorDistMarketTendence12 import EvaluatorDistMarketTendence12
from evaluators.EvaluatorDistance01 import EvaluatorDistance01
from evaluators.EvaluatorDistance02 import EvaluatorDistance02
from evaluators.EvaluatorDistance03 import EvaluatorDistance03
from evaluators.EvaluatorEMA_01 import EvaluatorEMA_01
from evaluators.EvaluatorEMA_02 import EvaluatorEMA_02
from evaluators.EvaluatorEMA_03 import EvaluatorEMA_03
from evaluators.EvaluatorEMA_04 import EvaluatorEMA_04
from evaluators.EvaluatorEMA_IA_01 import EvaluatorEMA_IA_01
from evaluators.EvaluatorEMA_IA_02 import EvaluatorEMA_IA_02
from evaluators.EvaluatorEMA_IA_LONG import EvaluatorEMA_IA_LONG
from evaluators.EvaluatorEMA_IA_LONG_01 import EvaluatorEMA_IA_LONG_01
from evaluators.EvaluatorEMA_IA_LONG_02 import EvaluatorEMA_IA_LONG_02
from evaluators.EvaluatorEMA_IA_LONG_ONLY_UP import EvaluatorEMA_IA_LONG_ONLY_UP
from evaluators.EvaluatorEMA_IA_LONG_ONLY_UP_CROSS import EvaluatorEMA_IA_LONG_ONLY_UP_CROSS
from evaluators.EvaluatorEMA_IA_ONLY_UP_01 import EvaluatorEMA_IA_ONLY_UP_01
from evaluators.EvaluatorEMA_IA_ONLY_UP_02 import EvaluatorEMA_IA_ONLY_UP_02
from evaluators.EvaluatorEMA_LONG_01 import EvaluatorEMA_LONG_01
from evaluators.EvaluatorEMA_LONG_02 import EvaluatorEMA_LONG_02
from evaluators.EvaluatorEMA_LONG_02_01 import EvaluatorEMA_LONG_02_01
from evaluators.EvaluatorEMA_LONG_02_02 import EvaluatorEMA_LONG_02_02
from evaluators.EvaluatorEMA_LONG_03 import EvaluatorEMA_LONG_03
from evaluators.EvaluatorEMA_LONG_03_01 import EvaluatorEMA_LONG_03_01
from evaluators.EvaluatorEMA_LONG_03_02 import EvaluatorEMA_LONG_03_02
from evaluators.EvaluatorEMA_LONG_03_03 import EvaluatorEMA_LONG_03_03
from evaluators.EvaluatorEMA_LONG_03_04 import EvaluatorEMA_LONG_03_04
from evaluators.EvaluatorEMA_LONG_03_05 import EvaluatorEMA_LONG_03_05
from evaluators.EvaluatorEMA_LONG_03_06 import EvaluatorEMA_LONG_03_06
from evaluators.EvaluatorEMA_LONG_03_06_01 import EvaluatorEMA_LONG_03_06_01
from evaluators.EvaluatorEMA_LONG_03_06_02 import EvaluatorEMA_LONG_03_06_02
from evaluators.EvaluatorEMA_LONG_03_07 import EvaluatorEMA_LONG_03_07
from evaluators.EvaluatorEMA_LONG_03_08 import EvaluatorEMA_LONG_03_08
from evaluators.EvaluatorEMA_LONG_03_09 import EvaluatorEMA_LONG_03_09
from evaluators.EvaluatorEMA_LONG_ONLY_UP_01 import EvaluatorEMA_LONG_ONLY_UP_01
from evaluators.EvaluatorEMA_LONG_ONLY_UP_02 import EvaluatorEMA_LONG_ONLY_UP_02
from evaluators.EvaluatorEMA_LONG_ONLY_UP_03 import EvaluatorEMA_LONG_ONLY_UP_03
from evaluators.EvaluatorEMA_LONG_ONLY_UP_03_01 import EvaluatorEMA_LONG_ONLY_UP_03_01
from evaluators.EvaluatorEMA_LONG_ONLY_UP_04 import EvaluatorEMA_LONG_ONLY_UP_04
from evaluators.EvaluatorEMA_LONG_ONLY_UP_04_01 import EvaluatorEMA_LONG_ONLY_UP_04_01
from evaluators.EvaluatorEMA_LONG_ONLY_UP_04_02 import EvaluatorEMA_LONG_ONLY_UP_04_02
from evaluators.EvaluatorETHUSD_ONLY_BUY_02 import EvaluatorETHUSD_ONLY_BUY_02
from evaluators.EvaluatorIBLG_ANGLE_FLOW_01 import EvaluatorIBLG_ANGLE_FLOW_01
from evaluators.EvaluatorIBLG_ANGLE_FLOW_02 import EvaluatorIBLG_ANGLE_FLOW_02
from evaluators.EvaluatorIBLG_ANGLE_FLOW_LONG_01 import EvaluatorIBLG_ANGLE_FLOW_LONG_01
from evaluators.EvaluatorIBLG_ANGLE_FLOW_LONG_02 import EvaluatorIBLG_ANGLE_FLOW_LONG_02
from evaluators.EvaluatorIBLG_ANGLE_FLOW_LONG_03 import EvaluatorIBLG_ANGLE_FLOW_LONG_03
from evaluators.EvaluatorIBLG_ANGLE_FLOW_LONG_04 import EvaluatorIBLG_ANGLE_FLOW_LONG_04
from evaluators.EvaluatorIBLG_ANGLE_FLOW_LONG_05 import EvaluatorIBLG_ANGLE_FLOW_LONG_05
from evaluators.EvaluatorIBLG_ANGLE_FLOW_LONG_06 import EvaluatorIBLG_ANGLE_FLOW_LONG_06
from evaluators.EvaluatorIBLG_ANGLE_FLOW_ONLY_UP_01 import EvaluatorIBLG_ANGLE_FLOW_ONLY_UP_01
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_00 import EvaluatorIBLG_ANGLE_ONLY_UP_00
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_02 import EvaluatorIBLG_ANGLE_ONLY_UP_02
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_03 import EvaluatorIBLG_ANGLE_ONLY_UP_03
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_04 import EvaluatorIBLG_ANGLE_ONLY_UP_04
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test01 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test01
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test02 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test02
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test03 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test03
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test04 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test04
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test05 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test05
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test06 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test06
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test07 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test07
from evaluators.EvaluatorIBLG_ANGLE_ONLY_UP_05_test08 import EvaluatorIBLG_ANGLE_ONLY_UP_05_test08
from evaluators.EvaluatorIBLG_LONG_00 import EvaluatorIBLG_LONG_00
from evaluators.EvaluatorIBLG_LONG_01 import EvaluatorIBLG_LONG_01
from evaluators.EvaluatorIBLG_LONG_02 import EvaluatorIBLG_LONG_02
from evaluators.EvaluatorIBLG_LONG_03 import EvaluatorIBLG_LONG_03
from evaluators.EvaluatorIBLG_LONG_04 import EvaluatorIBLG_LONG_04
from evaluators.EvaluatorIBLG_LONG_05 import EvaluatorIBLG_LONG_05
from evaluators.EvaluatorIBLG_LONG_06 import EvaluatorIBLG_LONG_06
from evaluators.EvaluatorIBLG_LONG_07 import EvaluatorIBLG_LONG_07
from evaluators.EvaluatorIBLG_LONG_08 import EvaluatorIBLG_LONG_08
from evaluators.EvaluatorIBLG_LONG_09 import EvaluatorIBLG_LONG_09
from evaluators.EvaluatorIBLG_LONG_ANGLE_ONLY_UP_01 import EvaluatorIBLG_LONG_ANGLE_ONLY_UP_01
from evaluators.EvaluatorIBLG_LONG_ANGLE_ONLY_UP_02 import EvaluatorIBLG_LONG_ANGLE_ONLY_UP_02
from evaluators.EvaluatorIBLG_LONG_ANGLE_ONLY_UP_03 import EvaluatorIBLG_LONG_ANGLE_ONLY_UP_03
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_00 import EvaluatorIBLG_LONG_ONLY_UP_00
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_01 import EvaluatorIBLG_LONG_ONLY_UP_01
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_02 import EvaluatorIBLG_LONG_ONLY_UP_02
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_03 import EvaluatorIBLG_LONG_ONLY_UP_03
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_04 import EvaluatorIBLG_LONG_ONLY_UP_04
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_05 import EvaluatorIBLG_LONG_ONLY_UP_05
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_07 import EvaluatorIBLG_LONG_ONLY_UP_07
from evaluators.EvaluatorIBLG_LONG_ONLY_UP_08 import EvaluatorIBLG_LONG_ONLY_UP_08
from evaluators.EvaluatorIBLG_MID_LONG_01 import EvaluatorIBLG_MID_LONG_01
from evaluators.EvaluatorIBLG_MID_LONG_02 import EvaluatorIBLG_MID_LONG_02
from evaluators.EvaluatorIBLG_MID_LONG_ONLY_UP_01 import EvaluatorIBLG_MID_LONG_ONLY_UP_01
from evaluators.EvaluatorIBLG_PROB_FLOW_01 import EvaluatorIBLG_PROB_FLOW_01
from evaluators.EvaluatorIBLG_PROB_FLOW_02 import EvaluatorIBLG_PROB_FLOW_02
from evaluators.EvaluatorIBLG_START_CLOSE_01 import EvaluatorIBLG_START_CLOSE_01
from evaluators.EvaluatorIBLG_START_CLOSE_02 import EvaluatorIBLG_START_CLOSE_02
from evaluators.EvaluatorIBLG_START_CLOSE_03 import EvaluatorIBLG_START_CLOSE_03
from evaluators.EvaluatorIBLG_START_CLOSE_03_01 import EvaluatorIBLG_START_CLOSE_03_01
from evaluators.EvaluatorIBLG_START_CLOSE_04 import EvaluatorIBLG_START_CLOSE_04
from evaluators.EvaluatorIBLG_START_CLOSE_05 import EvaluatorIBLG_START_CLOSE_05
from evaluators.EvaluatorIBLG_WEEK_FLOW_01 import EvaluatorIBLG_WEEK_FLOW_01
from evaluators.EvaluatorIBLG_WEEK_FLOW_02 import EvaluatorIBLG_WEEK_FLOW_02
from evaluators.EvaluatorIBLG_WEEK_FLOW_03 import EvaluatorIBLG_WEEK_FLOW_03
from evaluators.EvaluatorIBLG_WEEK_FLOW_ONLY_UP_01 import EvaluatorIBLG_WEEK_FLOW_ONLY_UP_01
from evaluators.EvaluatorIBLG_WEEK_FLOW_ONLY_UP_02 import EvaluatorIBLG_WEEK_FLOW_ONLY_UP_02
from evaluators.EvaluatorIBLG_WEEK_TOP_ONLY_UP_01 import EvaluatorIBLG_WEEK_TOP_ONLY_UP_01
from evaluators.EvaluatorIBLG_WEEK_TOP_ONLY_UP_02 import EvaluatorIBLG_WEEK_TOP_ONLY_UP_02
from evaluators.EvaluatorIBLG_WEEK_TOP_ONLY_UP_03 import EvaluatorIBLG_WEEK_TOP_ONLY_UP_03
from evaluators.EvaluatorIBLG_WEEK_TOP_ONLY_UP_04 import EvaluatorIBLG_WEEK_TOP_ONLY_UP_04
from evaluators.EvaluatorIMA1Optimiz_MEDDIFF_01 import EvaluatorIMA1Optimiz_MEDDIFF_01
from evaluators.EvaluatorIMA1Optimiz_MEDDIFF_02 import EvaluatorIMA1Optimiz_MEDDIFF_02
from evaluators.EvaluatorIMA1_ANGLE_01 import EvaluatorIMA1_ANGLE_01
from evaluators.EvaluatorIMA1_ANGLE_02 import EvaluatorIMA1_ANGLE_02
from evaluators.EvaluatorIMA1_ANGLE_03 import EvaluatorIMA1_ANGLE_03
from evaluators.EvaluatorIMA1_CLEAN_BLG_01 import EvaluatorIMA1_CLEAN_BLG_01
from evaluators.EvaluatorIMA1_CLEAN_BLG_02 import EvaluatorIMA1_CLEAN_BLG_02
from evaluators.EvaluatorIMA1_CLEAN_BLG_03 import EvaluatorIMA1_CLEAN_BLG_03
from evaluators.EvaluatorIMA1_CLEAN_BLG_04 import EvaluatorIMA1_CLEAN_BLG_04
from evaluators.EvaluatorIMA1_CLEAN_BLG_04_ONLY_DOWN_01 import EvaluatorIMA1_CLEAN_BLG_04_ONLY_DOWN_01
from evaluators.EvaluatorIMA1_CLEAN_BLG_04_ONLY_UP_01 import EvaluatorIMA1_CLEAN_BLG_04_ONLY_UP_01
from evaluators.EvaluatorIMA1_CLEAN_BLG_05 import EvaluatorIMA1_CLEAN_BLG_05
from evaluators.EvaluatorIMA1_CLEAN_BLG_06 import EvaluatorIMA1_CLEAN_BLG_06
from evaluators.EvaluatorIMA1_CLEAN_BLG_EXTREMES_01 import EvaluatorIMA1_CLEAN_BLG_EXTREMES_01
from evaluators.EvaluatorIMA1_CLEAN_Optimiz01 import EvaluatorIMA1_CLEAN_Optimiz01

from evaluators.EvaluatorIMA1_CLEAN_Optimiz02 import EvaluatorIMA1_CLEAN_Optimiz02
from evaluators.EvaluatorIMA1_CLEAN_Optimiz03 import EvaluatorIMA1_CLEAN_Optimiz03
from evaluators.EvaluatorIMA1_CLEAN_Optimiz04 import EvaluatorIMA1_CLEAN_Optimiz04
from evaluators.EvaluatorIMA1_INDICATOR_MEDDIFF_01 import EvaluatorIMA1_INDICATOR_MEDDIFF_01
from evaluators.EvaluatorIMA1_STDMED_Optimiz01 import EvaluatorIMA1_STDMED_Optimiz01
from evaluators.EvaluatorIPROB_FLOW_ONLY_UP_01 import EvaluatorIPROB_FLOW_ONLY_UP_01
from evaluators.EvaluatorIWEEK_DIRECTION_01 import EvaluatorIWEEK_DIRECTION_01
from evaluators.EvaluatorMARKETTENDENCE_STDMED_01 import EvaluatorMARKETTENDENCE_STDMED_01
from evaluators.EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01 import EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01
from evaluators.EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01_ONLYUP import EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01_ONLYUP
from evaluators.EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_02 import EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_02
from evaluators.EvaluatorMEDMOMENT_01_MEDDIFF_INDDIST_01 import EvaluatorMEDMOMENT_01_MEDDIFF_INDDIST_01
from evaluators.EvaluatorMEDMOMENT_CLEAN_MEDDIFF_01 import EvaluatorMEDMOMENT_CLEAN_MEDDIFF_01

from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz01 import EvaluatorMEDMOMENT_CLEAN_Optimiz01
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz02 import EvaluatorMEDMOMENT_CLEAN_Optimiz02
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz03 import EvaluatorMEDMOMENT_CLEAN_Optimiz03
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF import EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF01 import EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF01
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz04 import EvaluatorMEDMOMENT_CLEAN_Optimiz04
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz05 import EvaluatorMEDMOMENT_CLEAN_Optimiz05
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz06 import EvaluatorMEDMOMENT_CLEAN_Optimiz06
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz06_MEDDIFF_01 import EvaluatorMEDMOMENT_CLEAN_Optimiz06_MEDDIFF_01
from evaluators.EvaluatorMEDMOMENT_CLEAN_Optimiz07_PERCENT import EvaluatorMEDMOMENT_CLEAN_Optimiz07_PERCENT
from evaluators.EvaluatorMEDSTDOptimiz01 import EvaluatorMEDSTDOptimiz01
from evaluators.EvaluatorMEDSTDOptimiz02 import EvaluatorMEDSTDOptimiz02
from evaluators.EvaluatorMEDSTDOptimiz03 import EvaluatorMEDSTDOptimiz03
from evaluators.EvaluatorMEDSTDOptimiz04 import EvaluatorMEDSTDOptimiz04
from evaluators.EvaluatorMEDSTDOptimiz04OnlyUp import EvaluatorMEDSTDOptimiz04OnlyUp
from evaluators.EvaluatorMEDSTDOptimiz04OnlyUp01 import EvaluatorMEDSTDOptimiz04OnlyUp01
from evaluators.EvaluatorMEDSTDOptimiz05 import EvaluatorMEDSTDOptimiz05
from evaluators.EvaluatorMEDSTDOptimiz06 import EvaluatorMEDSTDOptimiz06
from evaluators.EvaluatorMEDSTDOptimiz07 import EvaluatorMEDSTDOptimiz07
from evaluators.EvaluatorMEDSTDOptimiz08 import EvaluatorMEDSTDOptimiz08
from evaluators.EvaluatorMEDSTDOptimiz09 import EvaluatorMEDSTDOptimiz09
from evaluators.EvaluatorMEDSTDOptimiz10 import EvaluatorMEDSTDOptimiz10
from evaluators.EvaluatorMEDSTDOptimiz_MEDDIFF_07 import EvaluatorMEDSTDOptimiz_MEDDIFF_07
from evaluators.EvaluatorMEDSTDRelative01 import EvaluatorMEDSTDRelative01
from evaluators.EvaluatorMEDSTDRelative02 import EvaluatorMEDSTDRelative02
from evaluators.EvaluatorMEDSTDRelative03 import EvaluatorMEDSTDRelative03
from evaluators.EvaluatorMEDSTDRelative04 import EvaluatorMEDSTDRelative04
from evaluators.EvaluatorMEDSTDRelative04OnlyUP import EvaluatorMEDSTDRelative04OnlyUP
from evaluators.EvaluatorMEDSTD_WEEK_MEDDIFF_01 import EvaluatorMEDSTD_WEEK_MEDDIFF_01
from evaluators.EvaluatorMEDSTD_WEEK_Optimiz01 import EvaluatorMEDSTD_WEEK_Optimiz01
from evaluators.EvaluatorMEDSTD_WEEK_Optimiz02 import EvaluatorMEDSTD_WEEK_Optimiz02
from evaluators.EvaluatorMEDSTD_WEEK_Optimiz03 import EvaluatorMEDSTD_WEEK_Optimiz03
from evaluators.EvaluatorMED_MOMENTOptimiz01OnlyUp import EvaluatorMED_MOMENTOptimiz01OnlyUp
from evaluators.EvaluatorMED_WEEK_Optimiz01 import EvaluatorMED_WEEK_Optimiz01
from evaluators.EvaluatorMED_WEEK_Optimiz02 import EvaluatorMED_WEEK_Optimiz02

from evaluators.EvaluatorOnlyUp01 import EvaluatorOnlyUp01
from evaluators.EvaluatorOnlyUp02 import EvaluatorOnlyUp02
from evaluators.EvaluatorOnlyUp03 import EvaluatorOnlyUp03
from evaluators.EvaluatorOnlyUp04 import EvaluatorOnlyUp04
from evaluators.EvaluatorOnlyUp05 import EvaluatorOnlyUp05
from evaluators.EvaluatorOnlyUp06 import EvaluatorOnlyUp06
from evaluators.EvaluatorOnlyUp07 import EvaluatorOnlyUp07
from evaluators.EvaluatorOnlyUp08 import EvaluatorOnlyUp08
from evaluators.EvaluatorOnlyUp09 import EvaluatorOnlyUp09
from evaluators.EvaluatorOnlyUpMARKET01 import EvaluatorOnlyUpMARKET01
from evaluators.EvaluatorPROBMEDSTD_CLEAN_Opt01 import EvaluatorPROBMEDSTD_CLEAN_Opt01
from evaluators.EvaluatorPROBMEDSTD_CLEAN_Opt02 import EvaluatorPROBMEDSTD_CLEAN_Opt02
from evaluators.EvaluatorPROBMEDSTD_CLEAN_Opt03 import EvaluatorPROBMEDSTD_CLEAN_Opt03
from evaluators.EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01 import EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01
from evaluators.EvaluatorPROBMEDSTD_MEDDIFF_BLG_01 import EvaluatorPROBMEDSTD_MEDDIFF_BLG_01
from evaluators.EvaluatorPROBMEDSTD_MEDDIFF_BLG_02 import EvaluatorPROBMEDSTD_MEDDIFF_BLG_02
from evaluators.EvaluatorRELATIVE_MEDSTD_01 import EvaluatorRELATIVE_MEDSTD_01
from evaluators.EvaluatorRELATIVE_MEDSTD_02 import EvaluatorRELATIVE_MEDSTD_02
from evaluators.EvaluatorRELATIVE_MEDSTD_03 import EvaluatorRELATIVE_MEDSTD_03
from evaluators.EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01 import EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01
from evaluators.EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_02 import EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_02
from evaluators.EvaluatorRELATIVE_MEDSTD_ONLYUP_01 import EvaluatorRELATIVE_MEDSTD_ONLYUP_01
from evaluators.EvaluatorRSI_01 import EvaluatorRSI_01
from evaluators.EvaluatorRSI_ONLYUP_01 import EvaluatorRSI_ONLYUP_01
from evaluators.EvaluatorSTDMarketOptimiz01 import EvaluatorSTDMarketOptimiz01
from evaluators.EvaluatorSTDMarketOptimiz02 import EvaluatorSTDMarketOptimiz02
from evaluators.EvaluatorSUPERBOT_ALPHA_01 import EvaluatorSUPERBOT_ALPHA_01
from evaluators.EvaluatorBTCUSD_ONLY_BUY_01 import EvaluatorBTCUSD_ONLY_BUY_01
from evaluators.EvaluatorETHUSD_ONLY_BUY_01 import EvaluatorETHUSD_ONLY_BUY_01
from params.ParamAAPL01 import ParamAAPL01
from params.ParamAAPL02 import ParamAAPL02
from params.ParamAAPL03 import ParamAAPL03
from params.ParamAAPL04 import ParamAAPL04
from params.ParamAAPL05 import ParamAAPL05
from params.ParamAMD01 import ParamAMD01
from params.ParamAMD02 import ParamAMD02
from params.ParamAMD03 import ParamAMD03
from params.ParamAMD04 import ParamAMD04
from params.ParamAMD05 import ParamAMD05
from params.ParamAMD06 import ParamAMD06
from params.ParamAMZN01 import ParamAMZN01
from params.ParamAMZN02 import ParamAMZN02
from params.ParamAMZN03 import ParamAMZN03
from params.ParamAMZN04 import ParamAMZN04
from params.ParamAMZN05 import ParamAMZN05
from params.ParamAMZN06 import ParamAMZN06
from params.ParamBABA01 import ParamBABA01
from params.ParamBABA02 import ParamBABA02

from params.ParamBTC01 import ParamBTC01
from params.ParamBTC02 import ParamBTC02
from params.ParamBTC03 import ParamBTC03
from params.ParamBTC04 import ParamBTC04
from params.ParamBTC05 import ParamBTC05
from params.ParamBTC06 import ParamBTC06
from params.ParamDIS01 import ParamDIS01
from params.ParamDIS02 import ParamDIS02
from params.ParamDIS03 import ParamDIS03
from params.ParamDIS04 import ParamDIS04
from params.ParamDIS05 import ParamDIS05
from params.ParamDIS06 import ParamDIS06
from params.ParamDIS07 import ParamDIS07
from params.ParamDIS08 import ParamDIS08
from params.ParamDIS09 import ParamDIS09
from params.ParamETH01 import ParamETH01
from params.ParamETH02 import ParamETH02
from params.ParamETH03 import ParamETH03
from params.ParamETH04 import ParamETH04
from params.ParamETH05 import ParamETH05
from params.ParamGLD import ParamGLD
from params.ParamGOOG01 import ParamGOOG01
from params.ParamGOOG02 import ParamGOOG02
from params.ParamGOOG03 import ParamGOOG03
from params.ParamGOOG04 import ParamGOOG04
from params.ParamHD01 import ParamHD01
from params.ParamINTC01 import ParamINTC01
from params.ParamINTC02 import ParamINTC02
from params.ParamINTC03 import ParamINTC03
from params.ParamINTC04 import ParamINTC04
from params.ParamINTC05 import ParamINTC05
from params.ParamKO01 import ParamKO01
from params.ParamKO02 import ParamKO02
from params.ParamKO03 import ParamKO03
from params.ParamKO04 import ParamKO04
from params.ParamMCD01 import ParamMCD01
from params.ParamMCD02 import ParamMCD02
from params.ParamMETA01 import ParamMETA01
from params.ParamMSFT01 import ParamMSFT01
from params.ParamMSFT02 import ParamMSFT02
from params.ParamMSFT03 import ParamMSFT03
from params.ParamMSFT04 import ParamMSFT04
from params.ParamNFLX01 import ParamNFLX01
from params.ParamNFLX02 import ParamNFLX02
from params.ParamNFLX03 import ParamNFLX03
from params.ParamNFLX04 import ParamNFLX04
from params.ParamNFLX05 import ParamNFLX05
from params.ParamNVDA01 import ParamNVDA01
from params.ParamNVDA02 import ParamNVDA02
from params.ParamNVDA03 import ParamNVDA03
from params.ParamNVDA04 import ParamNVDA04
from params.ParamNVDA05 import ParamNVDA05
from params.ParamNVDA06 import ParamNVDA06
from params.ParamNVDA07 import ParamNVDA07
from params.ParamSBUX01 import ParamSBUX01
from params.ParamSBUX02 import ParamSBUX02
from params.ParamSBUX03 import ParamSBUX03
from params.ParamSONY01 import ParamSONY01
from params.ParamSONY02 import ParamSONY02
from params.ParamSONY03 import ParamSONY03
from params.ParamTSLA01 import ParamTSLA01
from params.ParamTSLA02 import ParamTSLA02
from params.ParamTSLA03 import ParamTSLA03
from params.ParamTSLA04 import ParamTSLA04
from params.ParamTSLA05 import ParamTSLA05
from params.ParamTSLA06 import ParamTSLA06
from params.ParamTSLA07 import ParamTSLA07
from params.ParamTSLA08 import ParamTSLA08
from params.ParamTSLA09 import ParamTSLA09
from params.ParamVTI01 import ParamVTI01
from params.ParamVTI02 import ParamVTI02
from params.ParamVTI03 import ParamVTI03
from service.Active import Active
from service.Parameters import Parameters
import copy

class ActiveHelper:

    def __init__(self,simulation= False, isDBData=False):
        self.simulation = simulation
        self.isDBData = isDBData

    def prepareActivesSimulation(self):
        actives = list()

        aapl = self.prepareAAPL()
        actives.append(aapl)
        return actives

    def prepareActiveForDraw(self):
        actives = list()


        aapl = self.prepareAAPL()
        actives.append(aapl)



        dis = self.prepareDIS()
        actives.append(dis)



        amzn = self.prepareAMZN()
        actives.append(amzn)

        ko = self.prepareKO()
        actives.append(ko)

        nflx = self.prepareNFLX()
        actives.append(nflx)

        tsla = self.prepareTSLA()
        actives.append(tsla)

        msft = self.prepareMSFT()
        actives.append(msft)
        nvda = self.prepareNVDA()
        actives.append(nvda)
        goog = self.prepareGOOG()
        actives.append(goog)
        intc = self.prepareINTC()
        actives.append(intc)
        mcd = self.prepareMCD()
        actives.append(mcd)

        sbux = self.prepareSBUX01()
        actives.append(sbux)
        meta = self.prepareMETA01()
        actives.append(meta)
        vti = self.prepareVTI01()
        actives.append(vti)
        sony = self.prepareSONY01()
        actives.append(sony)
        baba = self.prepareBABA01()
        actives.append(baba)
        amd = self.prepareAMD01()
        actives.append(amd)

        eth = self.prepareETH2()
        actives.append(eth)
        #
        btc = self.prepareBTC2()
        actives.append(btc)

        return actives


    def prepareActives(self, skipDayControl = False):
        actives = list()


        #OPTIMIZADOS
        intc = self.prepareINTC()
        nflx = self.prepareNFLX5()
        sony = self.prepareSONY03()
        baba = self.prepareBABA02()
        nvda = self.prepareNVDA06()
        sbux = self.prepareSBUX()
        amd = self.prepareAMD06()
        msft = self.prepareMSFT04()

        
        #PENDIENTES

        tsla = self.prepareTSLA02()
        aapl = self.prepareAAPL7()

        meta = self.prepareMETA02()


        goog = self.prepareGOOG5()
        mcd = self.prepareMCD02()
        dis = self.prepareDIS08()
        amzn = self.prepareAMZN4()



        ko = self.prepareKO3()

        vti = self.prepareVTI02()



        hd = self.prepareHD01()

        eth = self.prepareETH2()
        btc = self.prepareBTC3()

        gld = self.prepareGLD()


        weekno = datetime.datetime.today().weekday()
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        print(f" hora : {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)
        if weekno < 5 or skipDayControl==True:
            print("Weekday")

            if currentTime >= int(1400) and currentTime <= (2300) or skipDayControl==True:
                print("dentro del rango semana")
                # ------------KO-----------------
                actives.append(aapl)
                actives.append(nflx)
                actives.append(amzn)
                actives.append(ko)
                actives.append(msft)

                actives.append(intc)
                actives.append(mcd)

                # ------------OK-----------------
                actives.append(dis)
                actives.append(nvda)
                actives.append(tsla)
                # ------------WAIT-----------------
                actives.append(goog)
                actives.append(meta)
                actives.append(sbux)
                actives.append(vti)
                actives.append(sony)
                actives.append(baba)
                actives.append(amd)
                actives.append(hd)
                actives.append(gld)



            # if int(current_time_h) > 23 and int(current_time_h) <= 22:
            # actives.append(eurusd)
        else:  # 5 Sat, 6 Sun
            print("Weekend")
        # actives.append(eurusd)
        actives.append(eth)
        actives.append(btc)
        # actives.append(btc)
        # actives.append(aapl)
        return actives

    def prepareActivesSelected(self, skipDayControl = False):
        actives = list()


        #OPTIMIZADOS
        aapl = self.prepareAAPL6()
        meta = self.prepareMETA02()


        # UNITTEST BUENOS
        nflx = self.prepareNFLX5()

        msft = self.prepareMSFT04()
        goog = self.prepareGOOG5()
        mcd = self.prepareMCD02()


        #unitetest REGULAR
        dis = self.prepareDIS08()
        amzn = self.prepareAMZN4()
        intc = self.prepareINTC01()


        #UNITTEST MEJORAR
        #BLG LONG
        tsla = self.prepareTSLA()

        nvda = self.prepareNVDA06()

        eth = self.prepareETH2()
        btc = self.prepareBTC3()

        ko = self.prepareKO3()

        sbux = self.prepareSBUX()

        vti = self.prepareVTI02()
        sony = self.prepareSONY03()
        baba = self.prepareBABA01()
        amd = self.prepareAMD05()
        hd = self.prepareHD01()
        gld = self.prepareGLD()


        weekno = datetime.datetime.today().weekday()
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        print(f" hora : {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)
        if weekno < 5 or skipDayControl==True:
            print("Weekday")

            if currentTime >= int(1400) and currentTime <= (2300) or skipDayControl==True:
                print("dentro del rango semana")
                # ------------KO-----------------
                # actives.append(aapl)
                # actives.append(nflx)
                # actives.append(amzn)
                # actives.append(ko)
                # actives.append(msft)
                #
                actives.append(intc)
                # actives.append(mcd)
                #
                # # ------------OK-----------------
                # actives.append(dis)
                # actives.append(nvda)
                # actives.append(tsla)
                # # ------------WAIT-----------------
                # actives.append(goog)
                # actives.append(meta)
                # actives.append(sbux)
                # actives.append(gld)
                # actives.append(vti)
                # actives.append(sony)
                # actives.append(baba)
                # actives.append(amd)
                # actives.append(hd)



            # if int(current_time_h) > 23 and int(current_time_h) <= 22:
            # actives.append(eurusd)
        else:  # 5 Sat, 6 Sun
            print("Weekend")
        # actives.append(eurusd)
        # actives.append(eth)
        # actives.append(btc)
        # actives.append(btc)
        # actives.append(aapl)
        return actives

    def prepareActivesRealLocal(self, skipDayControl = False):
        actives = list()

        # OPTIMIZADOS
        intc = self.prepareINTC()
        nflx = self.prepareNFLX5()
        sony = self.prepareSONY03()
        baba = self.prepareBABA02()
        nvda = self.prepareNVDA06()
        sbux = self.prepareSBUX()
        amd = self.prepareAMD06()
        msft = self.prepareMSFT04()

        # PENDIENTES

        tsla = self.prepareTSLA02()
        aapl = self.prepareAAPL7()

        meta = self.prepareMETA02()

        goog = self.prepareGOOG5()
        mcd = self.prepareMCD02()
        dis = self.prepareDIS08()
        amzn = self.prepareAMZN4()

        ko = self.prepareKO3()

        vti = self.prepareVTI02()

        hd = self.prepareHD01()

        eth = self.prepareETH2()
        btc = self.prepareBTC3()
        gld = self.prepareGLD()


        weekno = datetime.datetime.today().weekday()
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        print(f" hora : {current_time_h} minutos: {current_time_min}")
        currentTime = int(current_time_h + current_time_min)
        if weekno < 5 or skipDayControl==True:
            print("Weekday")
        #
            if currentTime >= int(1400) and currentTime <= (2300) or skipDayControl==True:
                print("dentro del rango semana")
        #         # ------------KO-----------------
        #         actives.append(aapl)
        #         actives.append(nflx)
        #         actives.append(amzn)
        #         actives.append(ko)
        #         actives.append(msft)
        #
                # actives.append(intc)
                # actives.append(mcd)
        # #
        #         # ------------OK-----------------
        #         actives.append(dis)
                actives.append(nvda)
        #         actives.append(tsla)
        #         actives.append(gld)
                # ------------WAIT-----------------
                # actives.append(goog)
                # actives.append(meta)
                # actives.append(sbux)
                # actives.append(vti)
                # actives.append(sony)
                # actives.append(baba)
                # actives.append(amd)
                # actives.append(hd)

        #
        #
        #     # if int(current_time_h) > 23 and int(current_time_h) <= 22:
        #     # actives.append(eurusd)
        # else:  # 5 Sat, 6 Sun
        #     print("Weekend")
        # actives.append(eurusd)
        # actives.append(eth)
        # actives.append(btc)
        # actives.append(btc)
        # actives.append(aapl)
        return actives

    def prepareAAPL(self):

        #PARAMETERS
        param = ParamAAPL01(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"

        # evaluator = Evaluator03()
        # evaluator = EvaluatorDistance03()
        evaluator = EvaluatorDistMarketTendence06()
        # evaluator = EvaluatorDistIndicatorTendence02()
        # evaluator = EvaluatorDistance01()

        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl

    def prepareAAPL1(self):

        #PARAMETERS
        param = ParamAAPL03(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"

        # evaluator = Evaluator03()
        # evaluator = EvaluatorDistance01()
        # evaluator = EvaluatorDistMarketTendence02()
        evaluator = EvaluatorDistMarketTenOptimiz01()
        # evaluator = EvaluatorDistance01()

        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl

    def prepareAAPL2(self):

        #PARAMETERS
        param = ParamAAPL04(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"

        # evaluator = EvaluatorDistIndicatorTendence03()
        # evaluator = EvaluatorMEDSTDOptimiz03()
        evaluator = EvaluatorMEDSTDOptimiz07()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorDistMarketTendence09()

        # evaluator = Evaluator03()
        # evaluator = EvaluatorDistance01()

        # evaluator = EvaluatorDistance01()

        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl

    def prepareAAPL3(self):

        #PARAMETERS
        param = ParamAAPL05(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz01()


        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl

    def prepareAAPL4(self):

        #PARAMETERS
        param = ParamAAPL01(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz01()
        # evaluator = EvaluatorSTDMarketOptimiz01()
        # evaluator = EvaluatorMEDSTDOptimiz04()
        evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz04()


        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl

    def prepareAAPL5(self):

        #PARAMETERS
        param = ParamAAPL02(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz01()
        # evaluator = EvaluatorSTDMarketOptimiz01()
        # evaluator = EvaluatorMEDSTDOptimiz04()
        evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06()


        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl

    def prepareAAPL6(self):

        #PARAMETERS
        param = ParamAAPL03(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"


        # evaluator = EvaluatorIBLG_MID_LONG_02()
        evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_06()
        # evaluator = EvaluatorIBLG_START_CLOSE_04()


        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl

    def prepareAAPL7(self):

        #PARAMETERS
        param = ParamAAPL04(self.isDBData)
        param.name = "AAPL"
        param.second_name = "AAPL"

        # evaluator = EvaluatorEMA_LONG_02()
        # evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorRSI_01()
        evaluator = EvaluatorBOLLINGER_09()
        # evaluator = EvaluatorEMA_IA_01()
        # evaluator = EvaluatorBOLLINGER_05()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()


        aapl = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return aapl


    def prepareGLD(self):

        #PARAMETERS
        param = ParamGLD(self.isDBData)
        param.name = "GLD"
        param.second_name = "GLD"

        # evaluator = EvaluatorEMA_LONG_02()
        evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()


        gld = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return gld

    def prepareSBUX01(self):

        #PARAMETERS
        param = ParamSBUX01(self.isDBData)
        param.name = "SBUX"
        param.second_name = "SBUX"

        evaluator = EvaluatorMEDSTDOptimiz03()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz04()
        # evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03()
        #

        sbux = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return sbux

    def prepareSBUX02(self):

        #PARAMETERS
        param = ParamSBUX01(self.isDBData)
        param.name = "SBUX"
        param.second_name = "SBUX"

        # evaluator = EvaluatorMEDSTDOptimiz03()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt03()
        # evaluator = EvaluatorMARKETTENDENCE_STDMED_01()
        evaluator = EvaluatorDirectionMEDSTD03()


        sbux = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return sbux

    def prepareSBUX(self):

        #PARAMETERS
        param = ParamSBUX03(self.isDBData)
        param.name = "SBUX"
        param.second_name = "SBUX"


        # evaluator = EvaluatorEMA_LONG_02_01()
        # evaluator = EvaluatorEMA_LONG_03_03()
        evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()



        sbux = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return sbux

    def prepareMETA01(self):

        #PARAMETERS
        param = ParamMETA01(self.isDBData)
        param.name = "META"
        param.second_name = "META"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        evaluator = EvaluatorMEDSTDOptimiz03()


        meta = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return meta

    def prepareMETA02(self):

        #PARAMETERS
        param = ParamMETA01(self.isDBData)
        param.name = "META"
        param.second_name = "META"

        # evaluator = EvaluatorIMA1_ANGLE_01()
        evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()




        meta = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return meta

    def prepareVTI01(self):

        #PARAMETERS
        param = ParamVTI01(self.isDBData)
        param.name = "VTI"
        param.second_name = "VTI"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        evaluator = EvaluatorMEDSTDOptimiz03()


        vti = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return vti

    def prepareVTI02(self):
            # PARAMETERS
            param = ParamVTI02(self.isDBData)
            param.name = "VTI"
            param.second_name = "VTI"

            evaluator = EvaluatorEMA_LONG_03_05()
            # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
            # evaluator = EvaluatorIBLG_WEEK_FLOW_03()
            # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_05()


            vti = Active(param, evaluator)

            # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
            #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

            return vti

    def prepareVTI03(self):
        # PARAMETERS
        param = ParamVTI03(self.isDBData)
        param.name = "VTI"
        param.second_name = "VTI"

        evaluator = EvaluatorIMA1_INDICATOR_MEDDIFF_01()

        vti = Active(param, evaluator)

        return vti

    def prepareSONY01(self):

        #PARAMETERS
        param = ParamSONY01(self.isDBData)
        param.name = "SONY"
        param.second_name = "SONY"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        evaluator = EvaluatorMEDSTDOptimiz03()


        vti = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return vti

    def prepareSONY02(self):

        #PARAMETERS
        param = ParamSONY02(self.isDBData)
        param.name = "SONY"
        param.second_name = "SONY"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        evaluator = EvaluatorRELATIVE_MEDSTD_03()


        vti = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return vti

    def prepareSONY03(self):

        #PARAMETERS
        param = ParamSONY03(self.isDBData)
        param.name = "SONY"
        param.second_name = "SONY"


        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        # evaluator = EvaluatorIMA1_ANGLE_02()
        # evaluator = EvaluatorIMA1_ANGLE_01()
        evaluator = EvaluatorIBLG_START_CLOSE_03()
        # evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_02()
        # evaluator = EvaluatorIBLG_START_CLOSE_02()
        # evaluator = EvaluatorIBLG_WEEK_FLOW_03()



        vti = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return vti

    def prepareBABA01(self):

        #PARAMETERS
        param = ParamBABA01(self.isDBData)
        param.name = "BABA"
        param.second_name = "BABA"


        # evaluator = EvaluatorIBLG_PROB_FLOW_01()
        evaluator = EvaluatorIBLG_MID_LONG_01()



        vti = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return vti
    def prepareBABA02(self):

        #PARAMETERS
        param = ParamBABA02(self.isDBData)
        param.name = "BABA"
        param.second_name = "BABA"

        # evaluator = EvaluatorEMA_LONG_02()
        evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        # evaluator = EvaluatorIBLG_START_CLOSE_02()
        # evaluator = EvaluatorIBLG_WEEK_FLOW_03()


        baba = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return baba
    def prepareAMD01(self):

        #PARAMETERS
        param = ParamAMD01(self.isDBData)
        param.name = "AMD"
        param.second_name = "AMD"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        evaluator = EvaluatorMEDSTDOptimiz03()


        vti = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return vti

    def prepareAMD02(self):

        #PARAMETERS
        param = ParamAMD01(self.isDBData)
        param.name = "AMD"
        param.second_name = "AMD"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03()


        amd = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return amd

    def prepareAMD03(self):

        #PARAMETERS
        param = ParamAMD02(self.isDBData)
        param.name = "AMD"
        param.second_name = "AMD"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        # evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03()
        # evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorMEDSTDOptimiz_MEDDIFF_07()
        # evaluator = EvaluatorEMA_01()
        evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01()


        amd = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return amd

    def prepareAMD04(self):

        #PARAMETERS
        param = ParamAMD03(self.isDBData)
        param.name = "AMD"
        param.second_name = "AMD"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        # evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03()
        # evaluator = EvaluatorPROBMEDSTD_MEDDIFF_BLG_01()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorMEDSTDOptimiz_MEDDIFF_07()
        # evaluator = EvaluatorEMA_01()
        # evaluator = EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01()
        evaluator = EvaluatorBOLLINGER_07()
        # evaluator = Evaluator01()
        # evaluator = EvaluatorBOLLINGER_LARGE_01()



        amd = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return amd

    def prepareAMD05(self):

        #PARAMETERS
        param = ParamAMD04(self.isDBData)
        param.name = "AMD"
        param.second_name = "AMD"

        # evaluator = EvaluatorIBLG_MID_LONG_02()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_01()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_05()
        evaluator = EvaluatorIMA1_ANGLE_01()
        # evaluator = EvaluatorIBLG_WEEK_FLOW_03()
        # evaluator = EvaluatorIBLG_LONG_ONLY_UP_01()
        # evaluator = EvaluatorIBLG_PROB_FLOW_01()




        amd = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return amd

    def prepareAMD06(self):

        #PARAMETERS
        param = ParamAMD06(self.isDBData)
        param.name = "AMD"
        param.second_name = "AMD"



        # evaluator = EvaluatorEMA_LONG_02()
        # evaluator = EvaluatorEMA_LONG_03_03()
        # evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorEMA_LONG_02_01()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        # evaluator = EvaluatorIMA1_ANGLE_02()
        # evaluator = EvaluatorEMA_LONG_03_06_01()
        evaluator = EvaluatorEMA_LONG_02_02()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_05()
        # evaluator = EvaluatorIBLG_PROB_FLOW_02()
        # evaluator = EvaluatorBOLLINGER_08()





        amd = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return amd

    def prepareNFLX(self):

        #PARAMETERS
        param = ParamNFLX01(self.isDBData)
        param.name = "NFLX"
        param.second_name = "NFLX"




        # evaluator = EvaluatorDistance02()
        # evaluator = EvaluatorDistance01()
        # evaluator = Evaluator03()
        # evaluator = EvaluatorDistance03()
        evaluator = EvaluatorDistMarketTendence03()
        # evaluator = EvaluatorDistIndicatorTendence02()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNFLX1(self):

        #PARAMETERS
        param = ParamNFLX02(self.isDBData)
        param.name = "NFLX"
        param.second_name = "NFLX"




        # evaluator = EvaluatorDistance02()
        # evaluator = EvaluatorDistance01()
        # evaluator = Evaluator04()
        # evaluator = EvaluatorDistance03()
        # evaluator = EvaluatorDistMarketTendence09()
        evaluator = EvaluatorDistMarketTendence10()
        # evaluator = EvaluatorDistIndicatorTendence02()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNFLX2(self):

        #PARAMETERS
        param = ParamNFLX03(self.isDBData)
        param.name = "NFLX"
        param.second_name = "NFLX"




        # evaluator = EvaluatorDistance02()
        # evaluator = EvaluatorDistance01()
        # evaluator = Evaluator04()
        # evaluator = EvaluatorDistance03()
        # evaluator = EvaluatorDistMarketTendence09()
        # evaluator = EvaluatorDistMarketTenOptimiz02()
        # evaluator = EvaluatorSTDMarketOptimiz01()
        evaluator = EvaluatorMEDSTDOptimiz04()
        # evaluator = EvaluatorDistIndicatorTendence01()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNFLX3(self):

        #PARAMETERS
        param = ParamNFLX04(self.isDBData)
        param.name = "NFLX"
        param.second_name = "NFLX"

        # evaluator = EvaluatorDistMarketTenOptimiz03()
        evaluator = EvaluatorMEDSTDOptimiz07()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt02()

        element = Active(param,evaluator)

        return element

    def prepareNFLX4(self):

        #PARAMETERS
        param = ParamNFLX04(self.isDBData)
        param.name = "NFLX"
        param.second_name = "NFLX"

        evaluator = EvaluatorIBLG_LONG_03()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz01()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz04()

        element = Active(param,evaluator)

        return element

    def prepareNFLX5(self):

        #PARAMETERS
        param = ParamNFLX04(self.isDBData)
        param.name = "NFLX"
        param.second_name = "NFLX"


        # evaluator = EvaluatorEMA_LONG_02_01()
        evaluator = EvaluatorEMA_LONG_02()
        # evaluator = EvaluatorEMA_LONG_02_01()
        # evaluator = EvaluatorEMA_LONG_03_03()


        element = Active(param,evaluator)

        return element

    def prepareTSLA(self):

        # PARAMETERS
        param = ParamTSLA01(self.isDBData)
        param.name = "TSLA"
        param.second_name = "TSLA"

        # evaluator = EvaluatorIBLG_MID_LONG_02()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_03()
        # evaluator = EvaluatorIBLG_PROB_FLOW_02()
        # evaluator = EvaluatorIBLG_START_CLOSE_05()
        # evaluator = EvaluatorBOLLINGER_05()
        evaluator = EvaluatorBOLLINGER_LARGE_02()
        # evaluator = EvaluatorIMA1_ANGLE_01()

        element = Active(param, evaluator)

        return element

    def prepareTSLA02(self):

        # PARAMETERS
        param = ParamTSLA02(self.isDBData)
        param.name = "TSLA"
        param.second_name = "TSLA"



        # evaluator = EvaluatorIMA1_ANGLE_01()
        # evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        # evaluator = EvaluatorEMA_LONG_03_06_01()
        # evaluator = EvaluatorEMA_IA_01()
        # evaluator = EvaluatorEMA_LONG_03()
        # evaluator = EvaluatorEMA_IA_LONG()
        evaluator = EvaluatorEMA_IA_LONG_01()
        # evaluator = EvaluatorEMA_IA_02()


        element = Active(param, evaluator)

        return element


    def prepareDIS(self):

        #PARAMETERS
        param = ParamDIS01(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"



        evaluator = EvaluatorDistMarketTendence05()
        # evaluator = EvaluatorDistIndicatorTendence01()
        # evaluator = EvaluatorDistance03()
        # evaluator = Evaluator01()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS01(self):

        #PARAMETERS
        param = ParamDIS03(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"



        # evaluator = EvaluatorDistMarketTendence05()
        evaluator = EvaluatorDistIndicatorTendence01()
        # evaluator = EvaluatorDistance03()
        # evaluator = Evaluator01()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS02(self):

        #PARAMETERS
        param = ParamDIS04(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"

        # evaluator = EvaluatorMEDSTDOptimiz07()
        evaluator = EvaluatorMEDSTDRelative01()
        # evaluator = EvaluatorDistMarketTendence05()
        # evaluator = EvaluatorDistIndicatorTendence01()

        # evaluator = EvaluatorDistance03()
        # evaluator = Evaluator01()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS03(self):

        # PARAMETERS
        param = ParamDIS05(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"

        evaluator = EvaluatorMEDSTDOptimiz07()
        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS04(self):

        # PARAMETERS
        param = ParamDIS06(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"

        evaluator = EvaluatorMEDSTDOptimiz07()
        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS05(self):

        # PARAMETERS
        param = ParamDIS05(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"

        evaluator = EvaluatorMED_WEEK_Optimiz01()
        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS06(self):

        # PARAMETERS
        param = ParamDIS08(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"

        # evaluator = EvaluatorMED_WEEK_Optimiz02()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        evaluator = EvaluatorMEDSTDOptimiz04()
        # evaluator = EvaluatorDIRECTION_MEDSTD_04()
        # evaluator = EvaluatorMEDSTD_WEEK_Optimiz02()
        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS07(self):

        # PARAMETERS
        param = ParamDIS09(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"

        evaluator = EvaluatorMEDSTDOptimiz08()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS08(self):

        # PARAMETERS
        param = ParamDIS04(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"


        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()

        # evaluator = EvaluatorEMA_LONG_02()
        evaluator = EvaluatorRSI_01()
        # evaluator = EvaluatorIBLG_MID_LONG_01()
        # evaluator = EvaluatorIBLG_MID_LONG_02()
        # evaluator = EvaluatorIBLG_PROB_FLOW_01()
        # evaluator = EvaluatorIMA1_ANGLE_02()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareDIS09(self):

        # PARAMETERS
        param = ParamDIS01(self.isDBData)
        param.name = "DIS"
        param.second_name = "DIS"

        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF()
        evaluator = EvaluatorEMA_01()
        # evaluator = EvaluatorBOLLINGER_01()
        # evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01()
        # evaluator = EvaluatorIMA1_INDICATOR_MEDDIFF_01()

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareAMZN(self):

        #PARAMETERS
        param = ParamAMZN03(self.isDBData)
        param.name = "AMZN"
        param.second_name = "AMZN"



        # evaluator = Evaluator01()
        # evaluator = EvaluatorDistance02()
        evaluator = EvaluatorDistMarketTendence07()
        # evaluator = EvaluatorDistIndicatorTendence02()

        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareAMZN1(self):

        #PARAMETERS
        param = ParamAMZN03(self.isDBData)
        param.name = "AMZN"
        param.second_name = "AMZN"



        # evaluator = Evaluator01()
        # evaluator = EvaluatorDistance02()
        evaluator = EvaluatorDistMarketTendence09()
        # evaluator = EvaluatorDistMarketTenOptimiz02()
        # evaluator = EvaluatorDistIndicatorTendence02()

        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareAMZN2(self):

        #PARAMETERS
        param = ParamAMZN04(self.isDBData)
        param.name = "AMZN"
        param.second_name = "AMZN"

        # evaluator = EvaluatorMEDSTDOptimiz02()
        # evaluator = Evaluator01()
        # evaluator = EvaluatorDistance02()
        # evaluator = EvaluatorDistMarketTendence09()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorMEDSTDOptimiz05()
        evaluator = EvaluatorMEDSTDRelative01()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        # evaluator = EvaluatorDistIndicatorTendence02()

        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareAMZN3(self):

        #PARAMETERS
        param = ParamAMZN06(self.isDBData)
        param.name = "AMZN"
        param.second_name = "AMZN"


        # evaluator = EvaluatorDirectionMEDSTD03()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz04()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareAMZN4(self):

        #PARAMETERS
        param = ParamAMZN05(self.isDBData)
        param.name = "AMZN"
        param.second_name = "AMZN"


        # evaluator = EvaluatorIBLG_MID_LONG_02()
        # evaluator = EvaluatorEMA_LONG_02()
        # evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        # evaluator = EvaluatorEMA_LONG_02()
        # evaluator = EvaluatorEMA_LONG_03()
        # evaluator = EvaluatorRSI_01()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_06()
        # evaluator = EvaluatorIMA1_ANGLE_01()
        # evaluator = EvaluatorIBLG_START_CLOSE_02()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_05()
        # evaluator = EvaluatorIBLG_PROB_FLOW_02()
        # evaluator = EvaluatorBOLLINGER_08()

        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareAMZN05(self):

        #PARAMETERS
        param = ParamAMZN05(self.isDBData)
        param.name = "AMZN"
        param.second_name = "AMZN"


        # evaluator = EvaluatorIMA1_CLEAN_Optimiz02()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt03()
        evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06_MEDDIFF_01()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareKO(self):

        #PARAMETERS
        param = ParamKO02(self.isDBData)
        param.name = "KO"
        param.second_name = "KO"



        # evaluator = EvaluatorDistance01()
        # evaluator = Evaluator03()
        # evaluator = EvaluatorDistance03()
        evaluator = EvaluatorDistMarketTendence06()
        # evaluator = EvaluatorDistIndicatorTendence02()
        # evaluator = EvaluatorDistance01()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareKO1(self):

        #PARAMETERS
        param = ParamKO02(self.isDBData)
        param.name = "KO"
        param.second_name = "KO"


        # evaluator = EvaluatorDIRECTION_CLEAN_Opt02()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        evaluator = EvaluatorDIRECTION_CLEAN_Opt03()

        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareKO2(self):

        #PARAMETERS
        param = ParamKO03(self.isDBData)
        param.name = "KO"
        param.second_name = "KO"


        # evaluator = EvaluatorDIRECTION_CLEAN_Opt02()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        # evaluator = EvaluatorDIRECTION_MEDSTD_04()
        # evaluator = EvaluatorMEDSTDOptimiz03()
        evaluator = EvaluatorDirectionMEDSTD03()

        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareKO3(self):

        #PARAMETERS
        param = ParamKO04(self.isDBData)
        param.name = "KO"
        param.second_name = "KO"


        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        # evaluator = EvaluatorEMA_LONG_02()
        evaluator = EvaluatorEMA_LONG_03()
        # evaluator = EvaluatorIBLG_MID_LONG_02()
        # evaluator = EvaluatorIBLG_START_CLOSE_02()
        # evaluator = EvaluatorIBLG_PROB_FLOW_01()
        # evaluator = EvaluatorIMA1_ANGLE_03()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareMSFT(self):

        #PARAMETERS
        param = ParamMSFT01(self.isDBData)
        param.name = "MSFT"
        param.second_name = "MSFT"



        # evaluator = Evaluator01()
        # evaluator = EvaluatorDistance02()
        # evaluator = EvaluatorDistMarketTendence09()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        evaluator = EvaluatorMEDSTDOptimiz03()
        # evaluator = EvaluatorDistIndicatorTendence02()

        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareMSFT01(self):

        #PARAMETERS
        param = ParamMSFT01(self.isDBData)
        param.name = "MSFT"
        param.second_name = "MSFT"




        # evaluator = EvaluatorMEDSTDOptimiz04()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt01()
        # evaluator = EvaluatorMEDSTDOptimiz04()
        evaluator = EvaluatorMEDSTDOptimiz04()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)
        return element

    def prepareMSFT02(self):
        # PARAMETERS
        param = ParamMSFT02(self.isDBData)
        param.name = "MSFT"
        param.second_name = "MSFT"


        evaluator = EvaluatorDIRECTION_MEDSTD_03()
        # evaluator = EvaluatorMEDSTD_WEEK_Optimiz02()

        element = Active(param, evaluator)


        return element

    def prepareMSFT03(self):
        # PARAMETERS
        param = ParamMSFT03(self.isDBData)
        param.name = "MSFT"
        param.second_name = "MSFT"

        # evaluator = EvaluatorDIRECTION_MEDSTD_03()
        # evaluator = EvaluatorSTDMarketOptimiz02()
        # evaluator = EvaluatorEMA_01()
        evaluator = EvaluatorBOLLINGER_01()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt01()

        element = Active(param, evaluator)

        return element

    def prepareMSFT04(self):
        # PARAMETERS
        param = ParamMSFT04(self.isDBData)
        param.name = "MSFT"
        param.second_name = "MSFT"


        # evaluator = EvaluatorEMA_LONG_02()
        # evaluator = EvaluatorEMA_LONG_03_06()
        evaluator = EvaluatorEMA_IA_LONG()
        # evaluator = EvaluatorRSI_01()
        # evaluator = EvaluatorIMA1_ANGLE_01()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()



        element = Active(param, evaluator)

        return element

    def prepareINTC(self):

        # PARAMETERS
        param = ParamINTC01(self.isDBData)
        param.name = "INTC"
        param.second_name = "INTC"

        # evaluator = EvaluatorIMA1_ANGLE_02()
        # evaluator = EvaluatorBOLLINGER_05_IMP_01()
        # evaluator = EvaluatorEMA_LONG_03_01()
        # evaluator = EvaluatorEMA_LONG_03()
        # evaluator = EvaluatorRSI_01()
        # evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        evaluator = EvaluatorMEDSTD_WEEK_Optimiz01()
        # evaluator = EvaluatorEMA_IA_LONG_02()
        # evaluator = EvaluatorIBLG_WEEK_FLOW_03()
        # evaluator = EvaluatorIBLG_START_CLOSE_02()
        # evaluator = EvaluatorIBLG_PROB_FLOW_02()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_03()

        element = Active(param, evaluator)

        return element

    def prepareINTC01(self):

        # PARAMETERS
        param = ParamINTC04(self.isDBData)
        param.name = "INTC"
        param.second_name = "INTC"



        evaluator = EvaluatorIBLG_MID_LONG_01()



        element = Active(param, evaluator)


        return element

    def prepareINTC02(self):

        # PARAMETERS
        param = ParamINTC05(self.isDBData)
        param.name = "INTC"
        param.second_name = "INTC"


        # evaluator = EvaluatorDIRECTION_CLEAN_Opt02()
        # evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        # evaluator = EvaluatorDIRECTION_MEDSTD_03()
        # evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF()
        # evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01()
        # evaluator = EvaluatorEMA_01()
        evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        # evaluator = EvaluatorBOLLINGER_07()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt03()


        element = Active(param, evaluator)


        return element

    def prepareMCD(self):

        # PARAMETERS
        param = ParamMCD01(self.isDBData)
        param.name = "MCD"
        param.second_name = "MCD"


        # evaluator = EvaluatorMEDSTDOptimiz03()
        evaluator = EvaluatorRELATIVE_MEDSTD_02()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareMCD01(self):

        # PARAMETERS
        param = ParamMCD02(self.isDBData)
        param.name = "MCD"
        param.second_name = "MCD"


        # evaluator = EvaluatorMEDSTDOptimiz03()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareMCD02(self):

        # PARAMETERS
        param = ParamMCD02(self.isDBData)
        param.name = "MCD"
        param.second_name = "MCD"

        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        evaluator = EvaluatorEMA_LONG_02()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        # evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorIBLG_PROB_FLOW_02()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_03()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareGOOG(self):

        # PARAMETERS
        param = ParamGOOG01(self.isDBData)
        param.name = "GOOG"
        param.second_name = "GOOG"

        # evaluator = Evaluator01()
        # evaluator = EvaluatorDistance02()
        # evaluator = EvaluatorDistMarketTendence09()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        evaluator = EvaluatorMEDSTDOptimiz03()
        # evaluator = EvaluatorDistIndicatorTendence02()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareGOOG1(self):

        # PARAMETERS
        param = ParamGOOG02(self.isDBData)
        param.name = "GOOG"
        param.second_name = "GOOG"



        evaluator = EvaluatorDIRECTION_CLEAN_Opt04()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareGOOG2(self):

        # PARAMETERS
        param = ParamGOOG02(self.isDBData)
        param.name = "GOOG"
        param.second_name = "GOOG"


        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorDistMarketTendence12()
        # evaluator = EvaluatorMEDSTDOptimiz07()
        evaluator = EvaluatorDIRECTION_CLEAN_Opt03()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareGOOG3(self):

        # PARAMETERS
        param = ParamGOOG03(self.isDBData)
        param.name = "GOOG"
        param.second_name = "GOOG"


        # evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        # evaluator = EvaluatorDistMarketTendence12()
        # evaluator = EvaluatorMEDSTDOptimiz07()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt05()
        evaluator = EvaluatorDistMarketTenOptimiz03()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareGOOG4(self):

        # PARAMETERS
        param = ParamGOOG03(self.isDBData)
        param.name = "GOOG"
        param.second_name = "GOOG"



        evaluator = EvaluatorDIRECTION_PROB_Opt01()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz04()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorDirectionMEDSTD03()
        # evaluator = EvaluatorMEDSTDRelative04()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareGOOG5(self):

        # PARAMETERS
        param = ParamGOOG02(self.isDBData)
        param.name = "GOOG"
        param.second_name = "GOOG"


        # evaluator = EvaluatorIBLG_PROB_FLOW_01()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_05()
        # evaluator = EvaluatorIMA1_ANGLE_01()
        # evaluator = EvaluatorEMA_LONG_03_03()
        # evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        evaluator = EvaluatorIBLG_LONG_03()




        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareGOOG6(self):

        # PARAMETERS
        param = ParamGOOG01(self.isDBData)
        param.name = "GOOG"
        param.second_name = "GOOG"

        # evaluator = EvaluatorDIRECTION_CLEAN_Opt05()
        # evaluator = EvaluatorDIRECTION_PROB_Opt02()
        evaluator = EvaluatorDirectionMEDSTD_MEDDIFF_01()
        # evaluator = EvaluatorDirectionMEDSTD_MEDDIFF_01()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA(self):

        # PARAMETERS
        param = ParamNVDA01(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"

        # evaluator = Evaluator01()
        # evaluator = EvaluatorDistance02()
        evaluator = EvaluatorDistMarketTendence09()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorMEDSTDOptimiz03()
        # evaluator = EvaluatorDistIndicatorTendence02()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA01(self):

        # PARAMETERS
        param = ParamNVDA02(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"


        # evaluator = EvaluatorDistMarketTendence09()
        evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        # evaluator = EvaluatorMEDSTDOptimiz07()
        # evaluator = EvaluatorMEDSTDRelative01()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorMEDSTDOptimiz04()
        # evaluator = EvaluatorDistIndicatorTendence02()
        # evaluator = Evaluator04()
        # evaluator = EvaluatorDistance02()
        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA02(self):

        # PARAMETERS
        param = ParamNVDA03(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"


        # evaluator = EvaluatorDistMarketTendence09()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        evaluator = EvaluatorMEDSTDRelative04()

        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorRELATIVE_MEDSTD_02()
        # evaluator = EvaluatorMEDSTDOptimiz07()
        # evaluator = EvaluatorMEDSTDRelative01()
        # evaluator = EvaluatorDistMarketTenOptimiz03()
        # evaluator = EvaluatorMEDSTDOptimiz04()
        # evaluator = EvaluatorDistIndicatorTendence02()
        # evaluator = Evaluator04()
        # evaluator = EvaluatorDistance02()
        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA03(self):

        # PARAMETERS
        param = ParamNVDA06(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"



        # evaluator = EvaluatorDIRECTION_MEDSTD_04()
        # evaluator = EvaluatorDirectionMEDSTD03()
        evaluator = EvaluatorMARKETTENDENCE_STDMED_01()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA04(self):

        # PARAMETERS
        param = ParamNVDA04(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"



        # evaluator = EvaluatorDIRECTION_MEDSTD_03()
        # evaluator = EvaluatorIMA1_CLEAN_Optimiz02()
        # evaluator = EvaluatorDIRECTION_CLEAN_Opt03()
        # evaluator = EvaluatorDIRECTION_MEDSTD_02()
        evaluator = EvaluatorDIRECTION_MEDSTD_04()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA05(self):

        # PARAMETERS
        param = ParamNVDA07(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"


        evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01()
        # evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        # evaluator = EvaluatorSTDMarketOptimiz01()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA06(self):

        # PARAMETERS
        param = ParamNVDA01(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"

        # evaluator = EvaluatorIBLG_START_CLOSE_03()
        # evaluator = EvaluatorEMA_LONG_02()
        evaluator = EvaluatorEMA_LONG_02_01()
        # evaluator = EvaluatorRSI_01()
        # evaluator = EvaluatorEMA_LONG_03_01()
        # evaluator = EvaluatorEMA_LONG_03_06()
        # evaluator = EvaluatorEMA_LONG_03_06_02()
        # evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        # evaluator = EvaluatorIBLG_LONG_08()
        # evaluator = EvaluatorIMA1_ANGLE_02()
        # evaluator = EvaluatorIMA1_ANGLE_02()
        # evaluator = EvaluatorIBLG_WEEK_FLOW_03()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_03()

        # evaluator = EvaluatorIBLG_START_CLOSE_02()
        # evaluator = EvaluatorIBLG_WEEK_FLOW_03()
        # evaluator = EvaluatorIBLG_PROB_FLOW_02()



        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareNVDA07(self):

        # PARAMETERS
        param = ParamNVDA02(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"


        # evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_02()
        # evaluator = Evaluator01()
        # evaluator = EvaluatorIMA1Optimiz_MEDDIFF_02()
        # evaluator = EvaluatorIMA1_INDICATOR_MEDDIFF_01()
        # evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06_MEDDIFF_01()
        # evaluator = EvaluatorEMA_01()
        # evaluator = EvaluatorBOLLINGER_08()
        # evaluator = EvaluatorSTDMarketOptimiz01()
        # evaluator = EvaluatorIMA1_CLEAN_BLG_03()
        # evaluator = EvaluatorMEDMOMENT_01_MEDDIFF_VALUEDIFF_01()
        # evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        # evaluator = EvaluatorBOLLINGER_LARGE_01()
        # evaluator = EvaluatorSTDMarketOptimiz01()
        evaluator = EvaluatorIMA1_CLEAN_BLG_04()
        # evaluator = EvaluatorIMA1_CLEAN_BLG_05()
        # evaluator = EvaluatorIMA1_CLEAN_BLG_04_ONLY_DOWN_01()
        # evaluator = EvaluatorDirectionMEDSTD_MEDDIFF_01()
        # evaluator = EvaluatorIMA1_CLEAN_BLG_04_ONLY_UP_01()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element
    def prepareNVDA08(self):

        # PARAMETERS
        param = ParamNVDA02(self.isDBData)
        param.name = "NVDA"
        param.second_name = "NVDA"


        evaluator = EvaluatorIBLG_PROB_FLOW_01()
        # evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        # evaluator = EvaluatorSTDMarketOptimiz01()


        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element
    def prepareHD01(self):

        # PARAMETERS
        param = ParamHD01(self.isDBData)
        param.name = "HD"
        param.second_name = "HD"


        # evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        evaluator = EvaluatorIMA1_ANGLE_01()
        # evaluator = EvaluatorIBLG_START_CLOSE_02()
        # evaluator = EvaluatorIBLG_WEEK_FLOW_03()

        element = Active(param, evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element



    def prepareBTC(self):

        #PARAMETERS
        param = ParamBTC01(self.isDBData)
        param.name = "BTCUSD"
        param.second_name = "BTC/USD"



        # evaluator = Evaluator02()
        # evaluator = EvaluatorOnlyUpMARKET01()
        # evaluator = EvaluatorOnlyUp06()
        evaluator = EvaluatorMEDSTDOptimiz04()
        # evaluator = EvaluatorDistIndicatorTenOnlyUp01()
        # evaluator = EvaluatorDistMarketTenOnlyUp01()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareBTC1(self):

        #PARAMETERS
        param = ParamBTC04(self.isDBData)
        param.name = "BTCUSD"
        param.second_name = "BTC/USD"



        # evaluator = Evaluator02()
        # evaluator = EvaluatorOnlyUpMARKET01()
        # evaluator = EvaluatorOnlyUp06()
        # evaluator = EvaluatorMED_MOMENTOptimiz01OnlyUp()
        # evaluator = EvaluatorBOLLINGER_07()
        evaluator = EvaluatorBOLLINGER_ONLY_UP_03()
        # evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01_ONLYUP()
        # evaluator = EvaluatorMEDSTDOptimiz_MEDDIFF_07()
        # evaluator = EvaluatorDistIndicatorTenOnlyUp01()
        # evaluator = EvaluatorDistMarketTenOnlyUp01()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element



    def prepareBTC2(self):

        #PARAMETERS
        param = ParamBTC05(self.isDBData)
        param.name = "BTCUSD"
        param.second_name = "BTC/USD"




        # evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_03()
        # evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_04()
        # evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_05_test01()
        # evaluator = EvaluatorIBLG_ANGLE_FLOW_ONLY_UP_01()
        evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_05_test02()
        #
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareBTC3(self):

        #PARAMETERS
        param = ParamBTC06(self.isDBData)
        param.name = "BTCUSD"
        param.second_name = "BTC/USD"


        evaluator = EvaluatorEMA_IA_ONLY_UP_01()
        # evaluator = EvaluatorEMA_LONG_ONLY_UP_04()
        # evaluator = EvaluatorEMA_LONG_ONLY_UP_04_01()



        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element


    def prepareETH(self):

        #PARAMETERS
        param = ParamETH01(self.isDBData)
        param.name = "ETHUSD"
        param.second_name = "ETH/USD"



        # evaluator = EvaluatorOnlyUp04()
        # evaluator = EvaluatorOnlyUp06()
        evaluator = EvaluatorIBLG_LONG_ANGLE_ONLY_UP_01()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareETH1(self):

        #PARAMETERS
        param = ParamETH03(self.isDBData)
        param.name = "ETHUSD"
        param.second_name = "ETH/USD"



        # evaluator = EvaluatorOnlyUp04()
        # evaluator = EvaluatorOnlyUp06()
        # evaluator = EvaluatorMEDSTDOptimiz04OnlyUp()
        # evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01()
        evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01_ONLYUP()
        # evaluator = EvaluatorBOLLINGER_ONLY_UP_03()
        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element

    def prepareETH2(self):

        #PARAMETERS
        # param = ParamETH04(self.isDBData)
        param = ParamETH03(self.isDBData)
        param.name = "ETHUSD"
        param.second_name = "ETH/USD"




        # evaluator = EvaluatorEMA_LONG_ONLY_UP_02()
        # evaluator = EvaluatorEMA_LONG_ONLY_UP_03_01()
        # evaluator = EvaluatorEMA_LONG_ONLY_UP_04_01()
        # evaluator = EvaluatorEMA_IA_LONG_ONLY_UP()
        evaluator = EvaluatorEMA_IA_LONG_ONLY_UP_CROSS()
        # evaluator = EvaluatorEMA_IA_ONLY_UP_02()
        # evaluator = EvaluatorEMA_LONG_ONLY_UP_01()
        # evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_05_test07()
        # evaluator = EvaluatorOnlyUp06()
        # evaluator = EvaluatorETHUSD_ONLY_BUY_01()
        # evaluator = EvaluatorETHUSD_ONLY_BUY_02()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element
    def prepareETH3(self):

        #PARAMETERS
        # param = ParamETH04(self.isDBData)
        param = ParamETH05(self.isDBData)
        param.name = "ETHUSD"
        param.second_name = "ETH/USD"




        # evaluator = EvaluatorEMA_LONG_ONLY_UP_02()
        # evaluator = EvaluatorEMA_LONG_ONLY_UP_03_01()
        # evaluator = EvaluatorEMA_LONG_ONLY_UP_04_01()
        evaluator = EvaluatorEMA_LONG_ONLY_UP_04_02()
        # evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_05_test07()
        # evaluator = EvaluatorOnlyUp06()
        # evaluator = EvaluatorETHUSD_ONLY_BUY_01()


        element = Active(param,evaluator)

        # aapl = Active("AAPL", "AAPL", "https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL", "UP", 0.40, 0.55,
        #               self.telegram, 0.09, False, 2, -927043450, 0.04, 3, 3, 5, 7, operate=True)

        return element
    def prepareActivesEvaluators(self,active):
        activeList = list()

        active1 = copy.deepcopy(active)
        active1.evaluator = Evaluator01()
        activeList.append(active1)

        active2 = copy.deepcopy(active)
        active2.evaluator = EvaluatorDIRECTION_MEDSTD_03()
        activeList.append(active2)

        active3 = copy.deepcopy(active)
        active3.evaluator = EvaluatorDirectionMEDSTD03()
        activeList.append(active3)

        active4 = copy.deepcopy(active)
        active4.evaluator = EvaluatorDistance03()
        activeList.append(active4)

        active5 = copy.deepcopy(active)
        active5.evaluator = EvaluatorDistIndicatorTendence03()
        activeList.append(active5)

        active6 = copy.deepcopy(active)
        active6.evaluator = EvaluatorDistMarketTendence04()
        activeList.append(active6)

        active7 = copy.deepcopy(active)
        active7.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF()
        activeList.append(active7)

        active8 = copy.deepcopy(active)
        active8.evaluator = EvaluatorDistMarketTenOptimiz03()
        activeList.append(active8)

        active9 = copy.deepcopy(active)
        active9.evaluator = EvaluatorMEDSTDOptimiz04()
        activeList.append(active9)

        active10 = copy.deepcopy(active)
        active10.evaluator = EvaluatorMEDSTDOptimiz07()
        activeList.append(active10)

        active11 = copy.deepcopy(active)
        active11.evaluator = EvaluatorMEDSTDRelative04()
        activeList.append(active11)

        active12 = copy.deepcopy(active)
        active12.evaluator = EvaluatorRELATIVE_MEDSTD_02()
        activeList.append(active12)

        active13 = copy.deepcopy(active)
        active13.evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF()
        activeList.append(active13)

        active14 = copy.deepcopy(active)
        active14.evaluator = EvaluatorDIRECTION_MEDSTD_02()
        activeList.append(active14)

        active15 = copy.deepcopy(active)
        active15.evaluator = EvaluatorMEDSTDOptimiz03()
        activeList.append(active15)

        active16 = copy.deepcopy(active)
        active16.evaluator = EvaluatorDIRECTION_CLEAN_Opt02()
        activeList.append(active16)

        active17 = copy.deepcopy(active)
        active17.evaluator = EvaluatorDIRECTION_CLEAN_Opt01()
        activeList.append(active17)

        active18 = copy.deepcopy(active)
        active18.evaluator = EvaluatorDIRECTION_CLEAN_Opt03()
        activeList.append(active18)

        active19 = copy.deepcopy(active)
        active19.evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        activeList.append(active19)

        active20 = copy.deepcopy(active)
        active20.evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        activeList.append(active20)
        #
        active21 = copy.deepcopy(active)
        active21.evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01()
        activeList.append(active21)

        active22 = copy.deepcopy(active)
        active22.evaluator = EvaluatorMEDSTDOptimiz_MEDDIFF_07()
        activeList.append(active22)

        active23 = copy.deepcopy(active)
        active23.evaluator = EvaluatorIMA1_CLEAN_Optimiz01()
        activeList.append(active23)

        active24 = copy.deepcopy(active)
        active24.evaluator = EvaluatorIMA1_CLEAN_Optimiz02()
        activeList.append(active24)

        active25 = copy.deepcopy(active)
        active25.evaluator = EvaluatorIMA1_CLEAN_Optimiz03()
        activeList.append(active25)

        active26 = copy.deepcopy(active)
        active26.evaluator = EvaluatorMEDSTDOptimiz10()
        activeList.append(active26)

        active27 = copy.deepcopy(active)
        active27.evaluator = EvaluatorMARKETTENDENCE_STDMED_01()
        activeList.append(active27)


        active28 = copy.deepcopy(active)
        active28.evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_02()
        activeList.append(active28)

        active29 = copy.deepcopy(active)
        active29.evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_02()
        activeList.append(active29)

        active30 = copy.deepcopy(active)
        active30.evaluator = EvaluatorMED_WEEK_Optimiz01()
        activeList.append(active30)

        active31 = copy.deepcopy(active)
        active31.evaluator = EvaluatorDIRECTION_CLEAN_Opt05()
        activeList.append(active31)

        active32 = copy.deepcopy(active)
        active32.evaluator = EvaluatorIMA1_CLEAN_Optimiz04()
        activeList.append(active32)

        active33 = copy.deepcopy(active)
        active33.evaluator = EvaluatorDIRECTION_CLEAN_Opt03_MEDDIFF_01()
        activeList.append(active33)

        active34 = copy.deepcopy(active)
        active34.evaluator = EvaluatorDirectionMEDSTD_MEDDIFF_01()
        activeList.append(active34)

        active35 = copy.deepcopy(active)
        active35.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt02()
        activeList.append(active35)

        active36 = copy.deepcopy(active)
        active36.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt01()
        activeList.append(active36)

        active37 = copy.deepcopy(active)
        active37.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03()
        activeList.append(active37)

        active38 = copy.deepcopy(active)
        active38.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz01()
        activeList.append(active38)

        active39 = copy.deepcopy(active)
        active39.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03()
        activeList.append(active39)

        active40 = copy.deepcopy(active)
        active40.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz04()
        activeList.append(active40)

        active41 = copy.deepcopy(active)
        active41.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06()
        activeList.append(active41)

        active42 = copy.deepcopy(active)
        active42.evaluator = EvaluatorDIRECTION_PROB_Opt01()
        activeList.append(active42)

        active43 = copy.deepcopy(active)
        active43.evaluator = EvaluatorDIRECTION_PROB_Opt02()
        activeList.append(active43)

        active44 = copy.deepcopy(active)
        active44.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF()
        activeList.append(active44)

        active45 = copy.deepcopy(active)
        active45.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06_MEDDIFF_01()
        activeList.append(active45)

        active46 = copy.deepcopy(active)
        active46.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01()
        activeList.append(active46)

        active47 = copy.deepcopy(active)
        active47.evaluator = EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01()
        activeList.append(active47)

        active48 = copy.deepcopy(active)
        active48.evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        activeList.append(active48)

        active49 = copy.deepcopy(active)
        active49.evaluator = EvaluatorIBLG_PROB_FLOW_01()
        activeList.append(active49)

        active50 = copy.deepcopy(active)
        active50.evaluator = EvaluatorIBLG_PROB_FLOW_02()
        activeList.append(active50)

        active51 = copy.deepcopy(active)
        active51.evaluator = EvaluatorIBLG_START_CLOSE_03()
        activeList.append(active51)

        active52 = copy.deepcopy(active)
        active52.evaluator = EvaluatorIBLG_START_CLOSE_05()
        activeList.append(active52)






        return activeList

    def prepareActivesEvaluators2(self, active):
        activeList = list()

        active1 = copy.deepcopy(active)
        active1.evaluator = Evaluator01()
        activeList.append(active1)

        active2 = copy.deepcopy(active)
        active2.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF()
        activeList.append(active2)

        active3 = copy.deepcopy(active)
        active3.evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF()
        activeList.append(active3)

        active4 = copy.deepcopy(active)
        active4.evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01()
        activeList.append(active4)

        active5 = copy.deepcopy(active)
        active5.evaluator = EvaluatorMEDSTDOptimiz_MEDDIFF_07()
        activeList.append(active5)

        active6 = copy.deepcopy(active)
        active6.evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_02()
        activeList.append(active6)

        active7 = copy.deepcopy(active)
        active7.evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_02()
        activeList.append(active7)

        active8 = copy.deepcopy(active)
        active8.evaluator = EvaluatorDIRECTION_CLEAN_Opt03_MEDDIFF_01()
        activeList.append(active8)

        active9 = copy.deepcopy(active)
        active9.evaluator = EvaluatorDirectionMEDSTD_MEDDIFF_01()
        activeList.append(active9)

        active10 = copy.deepcopy(active)
        active10.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF()
        activeList.append(active10)

        active11 = copy.deepcopy(active)
        active11.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06_MEDDIFF_01()
        activeList.append(active11)

        active12 = copy.deepcopy(active)
        active12.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01()
        activeList.append(active12)

        active13 = copy.deepcopy(active)
        active13.evaluator = EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01()
        activeList.append(active13)

        active14 = copy.deepcopy(active)
        active14.evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        activeList.append(active14)

        active15 = copy.deepcopy(active)
        active15.evaluator = EvaluatorIMA1Optimiz_MEDDIFF_02()
        activeList.append(active15)

        active16 = copy.deepcopy(active)
        active16.evaluator = EvaluatorIMA1_INDICATOR_MEDDIFF_01()
        activeList.append(active16)

        active17 = copy.deepcopy(active)
        active17.evaluator = EvaluatorMEDMOMENT_01_MEDDIFF_INDDIST_01()
        activeList.append(active17)

        active18 = copy.deepcopy(active)
        active18.evaluator = EvaluatorEMA_01()
        activeList.append(active18)

        active19 = copy.deepcopy(active)
        active19.evaluator = EvaluatorEMA_02()
        activeList.append(active19)

        active20 = copy.deepcopy(active)
        active20.evaluator = EvaluatorBOLLINGER_01()
        activeList.append(active20)

        active21 = copy.deepcopy(active)
        active21.evaluator = EvaluatorBOLLINGER_02()
        activeList.append(active21)

        active22 = copy.deepcopy(active)
        active22.evaluator = EvaluatorBOLLINGER_03()
        activeList.append(active22)

        active23 = copy.deepcopy(active)
        active23.evaluator = EvaluatorBOLLINGER_04()
        activeList.append(active23)


        active24 = copy.deepcopy(active)
        active24.evaluator = EvaluatorBOLLINGER_05()
        activeList.append(active24)

        active25 = copy.deepcopy(active)
        active25.evaluator = EvaluatorBOLLINGER_06()
        activeList.append(active25)

        active26 = copy.deepcopy(active)
        active26.evaluator = EvaluatorBOLLINGER_07()
        activeList.append(active26)

        active27 = copy.deepcopy(active)
        active27.evaluator = EvaluatorBOLLINGER_LARGE_01()
        activeList.append(active27)

        active28 = copy.deepcopy(active)
        active28.evaluator = EvaluatorPROBMEDSTD_MEDDIFF_BLG_01()
        activeList.append(active28)

        active29 = copy.deepcopy(active)
        active29.evaluator = EvaluatorBOLLINGER_08()
        activeList.append(active29)

        active30 = copy.deepcopy(active)
        active30.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF01()
        activeList.append(active30)

        active31 = copy.deepcopy(active)
        active31.evaluator = EvaluatorIMA1_CLEAN_BLG_01()
        activeList.append(active31)

        active32 = copy.deepcopy(active)
        active32.evaluator = EvaluatorIMA1_CLEAN_BLG_02()
        activeList.append(active32)

        active33 = copy.deepcopy(active)
        active33.evaluator = EvaluatorIMA1_CLEAN_BLG_EXTREMES_01()
        activeList.append(active33)

        active34 = copy.deepcopy(active)
        active34.evaluator = EvaluatorIMA1_CLEAN_BLG_05()
        activeList.append(active34)

        active35 = copy.deepcopy(active)
        active35.evaluator = EvaluatorIBLG_LONG_ONLY_UP_01()
        activeList.append(active35)

        active36 = copy.deepcopy(active)
        active36.evaluator = EvaluatorIBLG_LONG_03()
        activeList.append(active36)

        active37 = copy.deepcopy(active)
        active37.evaluator = EvaluatorIBLG_LONG_04()
        activeList.append(active37)

        active38 = copy.deepcopy(active)
        active38.evaluator = EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_02()
        activeList.append(active38)

        active39 = copy.deepcopy(active)
        active39.evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        activeList.append(active39)

        active40 = copy.deepcopy(active)
        active40.evaluator = EvaluatorIBLG_LONG_06()
        activeList.append(active40)

        active41 = copy.deepcopy(active)
        active41.evaluator = EvaluatorIBLG_START_CLOSE_01()
        activeList.append(active41)

        active42 = copy.deepcopy(active)
        active42.evaluator = EvaluatorIBLG_WEEK_FLOW_01()
        activeList.append(active42)

        active42 = copy.deepcopy(active)
        active42.evaluator = EvaluatorIBLG_WEEK_FLOW_03()
        activeList.append(active42)

        active43 = copy.deepcopy(active)
        active43.evaluator = EvaluatorIBLG_PROB_FLOW_01()
        activeList.append(active43)

        active44 = copy.deepcopy(active)
        active44.evaluator = EvaluatorIBLG_PROB_FLOW_02()
        activeList.append(active44)

        active45 = copy.deepcopy(active)
        active45.evaluator = EvaluatorIBLG_START_CLOSE_03()
        activeList.append(active45)

        active46 = copy.deepcopy(active)
        active46.evaluator = EvaluatorIBLG_PROB_FLOW_01()
        activeList.append(active46)

        active47 = copy.deepcopy(active)
        active47.evaluator = EvaluatorIBLG_ANGLE_FLOW_01()
        activeList.append(active47)

        active48 = copy.deepcopy(active)
        active48.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_03()
        activeList.append(active48)

        active49 = copy.deepcopy(active)
        active49.evaluator = EvaluatorIMA1_ANGLE_01()
        activeList.append(active49)











        return activeList

    def prepareActivesEvaluators4Old(self, active):
        activeList = list()

        active1 = copy.deepcopy(active)
        active1.evaluator = EvaluatorIMA1_ANGLE_01()
        activeList.append(active1)


        active2 = copy.deepcopy(active)
        active2.evaluator = EvaluatorIBLG_LONG_03()
        activeList.append(active2)

        active3 = copy.deepcopy(active)
        active3.evaluator = EvaluatorIBLG_START_CLOSE_03()
        activeList.append(active3)

        active4 = copy.deepcopy(active)
        active4.evaluator = EvaluatorIBLG_LONG_08()
        activeList.append(active4)

        active5 = copy.deepcopy(active)
        active5.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        activeList.append(active5)

        active6 = copy.deepcopy(active)
        active6.evaluator = EvaluatorBOLLINGER_05()
        activeList.append(active6)

        active7 = copy.deepcopy(active)
        active7.evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        activeList.append(active7)

        active8 = copy.deepcopy(active)
        active8.evaluator = EvaluatorBOLLINGER_05_IMP_01()
        activeList.append(active8)

        active9 = copy.deepcopy(active)
        active9.evaluator = EvaluatorIMA1_ANGLE_02()
        activeList.append(active9)

        active10 = copy.deepcopy(active)
        active10.evaluator = EvaluatorEMA_LONG_02()
        activeList.append(active10)

        active11 = copy.deepcopy(active)
        active11.evaluator = EvaluatorEMA_LONG_03()
        activeList.append(active11)

        active12 = copy.deepcopy(active)
        active12.evaluator = EvaluatorEMA_LONG_02_01()
        activeList.append(active12)

        active13 = copy.deepcopy(active)
        active13.evaluator = EvaluatorEMA_LONG_03_04()
        activeList.append(active13)

        active14 = copy.deepcopy(active)
        active14.evaluator = EvaluatorEMA_LONG_03_05()
        activeList.append(active14)

        active15 = copy.deepcopy(active)
        active15.evaluator = EvaluatorEMA_LONG_03_06()
        activeList.append(active15)

        active16 = copy.deepcopy(active)
        active16.evaluator = EvaluatorEMA_LONG_03_06_01()
        activeList.append(active16)

        active17 = copy.deepcopy(active)
        active17.evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        activeList.append(active17)

        active18 = copy.deepcopy(active)
        active18.evaluator = EvaluatorRSI_01()
        activeList.append(active18)

        active19 = copy.deepcopy(active)
        active19.evaluator = EvaluatorSUPERBOT_ALPHA_01()
        activeList.append(active19)

        active20 = copy.deepcopy(active)
        active20.evaluator = EvaluatorEMA_IA_02()
        activeList.append(active20)

        active21 = copy.deepcopy(active)
        active21.evaluator = EvaluatorEMA_IA_01()
        activeList.append(active21)

        active22 = copy.deepcopy(active)
        active22.evaluator = EvaluatorEMA_IA_LONG()
        activeList.append(active22)

        active23 = copy.deepcopy(active)
        active23.evaluator = EvaluatorEMA_IA_LONG_01()
        activeList.append(active23)

        active24 = copy.deepcopy(active)
        active24.evaluator = EvaluatorEMA_LONG_02_02()
        activeList.append(active24)

        return activeList

# AUTO-GENERATED — NO EDITAR A MANO
# Run: python3 prepare_evaluators.py to regenerate

    def prepareActivesEvaluators4(self, active):
        activeList = list()

        active1 = copy.deepcopy(active)
        active1.evaluator = EvaluatorBOLLINGER_00()
        activeList.append(active1)

        active2 = copy.deepcopy(active)
        active2.evaluator = EvaluatorBOLLINGER_01()
        activeList.append(active2)

        active3 = copy.deepcopy(active)
        active3.evaluator = EvaluatorBOLLINGER_02()
        activeList.append(active3)

        active4 = copy.deepcopy(active)
        active4.evaluator = EvaluatorBOLLINGER_03()
        activeList.append(active4)

        active5 = copy.deepcopy(active)
        active5.evaluator = EvaluatorBOLLINGER_04()
        activeList.append(active5)

        active6 = copy.deepcopy(active)
        active6.evaluator = EvaluatorBOLLINGER_05()
        activeList.append(active6)

        active7 = copy.deepcopy(active)
        active7.evaluator = EvaluatorBOLLINGER_05_IMP_01()
        activeList.append(active7)

        active8 = copy.deepcopy(active)
        active8.evaluator = EvaluatorBOLLINGER_06()
        activeList.append(active8)

        active9 = copy.deepcopy(active)
        active9.evaluator = EvaluatorBOLLINGER_07()
        activeList.append(active9)

        active10 = copy.deepcopy(active)
        active10.evaluator = EvaluatorBOLLINGER_08()
        activeList.append(active10)

        active11 = copy.deepcopy(active)
        active11.evaluator = EvaluatorBOLLINGER_09()
        activeList.append(active11)

        active12 = copy.deepcopy(active)
        active12.evaluator = EvaluatorBOLLINGER_LARGE_01()
        activeList.append(active12)

        active13 = copy.deepcopy(active)
        active13.evaluator = EvaluatorBOLLINGER_LARGE_02()
        activeList.append(active13)

        active14 = copy.deepcopy(active)
        active14.evaluator = EvaluatorBOLLINGER_LARGE_03()
        activeList.append(active14)

        # active15 = copy.deepcopy(active)
        # active15.evaluator = EvaluatorBase()
        # activeList.append(active15)

        active16 = copy.deepcopy(active)
        active16.evaluator = EvaluatorDIRECTION_CLEAN_Opt01()
        activeList.append(active16)

        active17 = copy.deepcopy(active)
        active17.evaluator = EvaluatorDIRECTION_CLEAN_Opt02()
        activeList.append(active17)

        active18 = copy.deepcopy(active)
        active18.evaluator = EvaluatorDIRECTION_CLEAN_Opt03()
        activeList.append(active18)

        active19 = copy.deepcopy(active)
        active19.evaluator = EvaluatorDIRECTION_CLEAN_Opt03_MEDDIFF_01()
        activeList.append(active19)

        active20 = copy.deepcopy(active)
        active20.evaluator = EvaluatorDIRECTION_CLEAN_Opt04()
        activeList.append(active20)

        active21 = copy.deepcopy(active)
        active21.evaluator = EvaluatorDIRECTION_CLEAN_Opt05()
        activeList.append(active21)

        active22 = copy.deepcopy(active)
        active22.evaluator = EvaluatorDIRECTION_MEDSTD_01()
        activeList.append(active22)

        active23 = copy.deepcopy(active)
        active23.evaluator = EvaluatorDIRECTION_MEDSTD_02()
        activeList.append(active23)

        active24 = copy.deepcopy(active)
        active24.evaluator = EvaluatorDIRECTION_MEDSTD_03()
        activeList.append(active24)

        active25 = copy.deepcopy(active)
        active25.evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF()
        activeList.append(active25)

        active26 = copy.deepcopy(active)
        active26.evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_01()
        activeList.append(active26)

        active27 = copy.deepcopy(active)
        active27.evaluator = EvaluatorDIRECTION_MEDSTD_03_MEDDIFF_02()
        activeList.append(active27)

        active28 = copy.deepcopy(active)
        active28.evaluator = EvaluatorDIRECTION_MEDSTD_04()
        activeList.append(active28)

        active29 = copy.deepcopy(active)
        active29.evaluator = EvaluatorDIRECTION_PROB_Opt01()
        activeList.append(active29)

        active30 = copy.deepcopy(active)
        active30.evaluator = EvaluatorDIRECTION_PROB_Opt02()
        activeList.append(active30)

        active31 = copy.deepcopy(active)
        active31.evaluator = EvaluatorDirectionMEDSTD01()
        activeList.append(active31)

        active32 = copy.deepcopy(active)
        active32.evaluator = EvaluatorDirectionMEDSTD02()
        activeList.append(active32)

        active33 = copy.deepcopy(active)
        active33.evaluator = EvaluatorDirectionMEDSTD03()
        activeList.append(active33)

        active34 = copy.deepcopy(active)
        active34.evaluator = EvaluatorDirectionMEDSTD03_01()
        activeList.append(active34)

        active35 = copy.deepcopy(active)
        active35.evaluator = EvaluatorDirectionMEDSTD04()
        activeList.append(active35)

        active36 = copy.deepcopy(active)
        active36.evaluator = EvaluatorDirectionMEDSTD_MEDDIFF_01()
        activeList.append(active36)

        active37 = copy.deepcopy(active)
        active37.evaluator = EvaluatorDistIndicatorTenOnlyUp01()
        activeList.append(active37)

        active38 = copy.deepcopy(active)
        active38.evaluator = EvaluatorDistIndicatorTendence01()
        activeList.append(active38)

        active39 = copy.deepcopy(active)
        active39.evaluator = EvaluatorDistIndicatorTendence02()
        activeList.append(active39)

        active40 = copy.deepcopy(active)
        active40.evaluator = EvaluatorDistIndicatorTendence03()
        activeList.append(active40)

        active41 = copy.deepcopy(active)
        active41.evaluator = EvaluatorDistMarketTenOnlyUp01()
        activeList.append(active41)

        active42 = copy.deepcopy(active)
        active42.evaluator = EvaluatorDistMarketTenOptimiz00()
        activeList.append(active42)

        active43 = copy.deepcopy(active)
        active43.evaluator = EvaluatorDistMarketTenOptimiz01()
        activeList.append(active43)

        active44 = copy.deepcopy(active)
        active44.evaluator = EvaluatorDistMarketTenOptimiz02()
        activeList.append(active44)

        active45 = copy.deepcopy(active)
        active45.evaluator = EvaluatorDistMarketTenOptimiz03()
        activeList.append(active45)

        active46 = copy.deepcopy(active)
        active46.evaluator = EvaluatorDistMarketTendence01()
        activeList.append(active46)

        active47 = copy.deepcopy(active)
        active47.evaluator = EvaluatorDistMarketTendence02()
        activeList.append(active47)

        active48 = copy.deepcopy(active)
        active48.evaluator = EvaluatorDistMarketTendence03()
        activeList.append(active48)

        active49 = copy.deepcopy(active)
        active49.evaluator = EvaluatorDistMarketTendence04()
        activeList.append(active49)

        active50 = copy.deepcopy(active)
        active50.evaluator = EvaluatorDistMarketTendence05()
        activeList.append(active50)

        active51 = copy.deepcopy(active)
        active51.evaluator = EvaluatorDistMarketTendence06()
        activeList.append(active51)

        active52 = copy.deepcopy(active)
        active52.evaluator = EvaluatorDistMarketTendence07()
        activeList.append(active52)

        active53 = copy.deepcopy(active)
        active53.evaluator = EvaluatorDistMarketTendence08()
        activeList.append(active53)

        active54 = copy.deepcopy(active)
        active54.evaluator = EvaluatorDistMarketTendence09()
        activeList.append(active54)

        active55 = copy.deepcopy(active)
        active55.evaluator = EvaluatorDistMarketTendence10()
        activeList.append(active55)

        active56 = copy.deepcopy(active)
        active56.evaluator = EvaluatorDistMarketTendence11()
        activeList.append(active56)

        active57 = copy.deepcopy(active)
        active57.evaluator = EvaluatorDistMarketTendence12()
        activeList.append(active57)

        active58 = copy.deepcopy(active)
        active58.evaluator = EvaluatorDistance01()
        activeList.append(active58)

        active59 = copy.deepcopy(active)
        active59.evaluator = EvaluatorDistance02()
        activeList.append(active59)

        active60 = copy.deepcopy(active)
        active60.evaluator = EvaluatorDistance03()
        activeList.append(active60)

        active61 = copy.deepcopy(active)
        active61.evaluator = EvaluatorEMA_01()
        activeList.append(active61)

        active62 = copy.deepcopy(active)
        active62.evaluator = EvaluatorEMA_02()
        activeList.append(active62)

        active63 = copy.deepcopy(active)
        active63.evaluator = EvaluatorEMA_03()
        activeList.append(active63)

        active64 = copy.deepcopy(active)
        active64.evaluator = EvaluatorEMA_04()
        activeList.append(active64)

        active65 = copy.deepcopy(active)
        active65.evaluator = EvaluatorEMA_IA_01()
        activeList.append(active65)

        active66 = copy.deepcopy(active)
        active66.evaluator = EvaluatorEMA_IA_02()
        activeList.append(active66)

        active67 = copy.deepcopy(active)
        active67.evaluator = EvaluatorEMA_IA_LONG()
        activeList.append(active67)

        active68 = copy.deepcopy(active)
        active68.evaluator = EvaluatorEMA_IA_LONG_01()
        activeList.append(active68)

        active69 = copy.deepcopy(active)
        active69.evaluator = EvaluatorEMA_IA_LONG_02()
        activeList.append(active69)

        active70 = copy.deepcopy(active)
        active70.evaluator = EvaluatorEMA_LONG_01()
        activeList.append(active70)

        active71 = copy.deepcopy(active)
        active71.evaluator = EvaluatorEMA_LONG_02()
        activeList.append(active71)

        active72 = copy.deepcopy(active)
        active72.evaluator = EvaluatorEMA_LONG_02_01()
        activeList.append(active72)

        active73 = copy.deepcopy(active)
        active73.evaluator = EvaluatorEMA_LONG_02_02()
        activeList.append(active73)

        active74 = copy.deepcopy(active)
        active74.evaluator = EvaluatorEMA_LONG_03()
        activeList.append(active74)

        active75 = copy.deepcopy(active)
        active75.evaluator = EvaluatorEMA_LONG_03_01()
        activeList.append(active75)

        active76 = copy.deepcopy(active)
        active76.evaluator = EvaluatorEMA_LONG_03_02()
        activeList.append(active76)

        active77 = copy.deepcopy(active)
        active77.evaluator = EvaluatorEMA_LONG_03_03()
        activeList.append(active77)

        active78 = copy.deepcopy(active)
        active78.evaluator = EvaluatorEMA_LONG_03_04()
        activeList.append(active78)

        active79 = copy.deepcopy(active)
        active79.evaluator = EvaluatorEMA_LONG_03_05()
        activeList.append(active79)

        active80 = copy.deepcopy(active)
        active80.evaluator = EvaluatorEMA_LONG_03_06()
        activeList.append(active80)

        active81 = copy.deepcopy(active)
        active81.evaluator = EvaluatorEMA_LONG_03_06_01()
        activeList.append(active81)

        active82 = copy.deepcopy(active)
        active82.evaluator = EvaluatorEMA_LONG_03_06_02()
        activeList.append(active82)

        active83 = copy.deepcopy(active)
        active83.evaluator = EvaluatorEMA_LONG_03_07()
        activeList.append(active83)

        active84 = copy.deepcopy(active)
        active84.evaluator = EvaluatorEMA_LONG_03_08()
        activeList.append(active84)

        active85 = copy.deepcopy(active)
        active85.evaluator = EvaluatorEMA_LONG_03_09()
        activeList.append(active85)

        active86 = copy.deepcopy(active)
        active86.evaluator = EvaluatorIBLG_ANGLE_FLOW_01()
        activeList.append(active86)

        active87 = copy.deepcopy(active)
        active87.evaluator = EvaluatorIBLG_ANGLE_FLOW_02()
        activeList.append(active87)

        active88 = copy.deepcopy(active)
        active88.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        activeList.append(active88)

        active89 = copy.deepcopy(active)
        active89.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_02()
        activeList.append(active89)

        active90 = copy.deepcopy(active)
        active90.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_03()
        activeList.append(active90)

        active91 = copy.deepcopy(active)
        active91.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_04()
        activeList.append(active91)

        active92 = copy.deepcopy(active)
        active92.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_05()
        activeList.append(active92)

        active93 = copy.deepcopy(active)
        active93.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_06()
        activeList.append(active93)

        active94 = copy.deepcopy(active)
        active94.evaluator = EvaluatorIBLG_LONG_00()
        activeList.append(active94)

        active95 = copy.deepcopy(active)
        active95.evaluator = EvaluatorIBLG_LONG_01()
        activeList.append(active95)

        active96 = copy.deepcopy(active)
        active96.evaluator = EvaluatorIBLG_LONG_02()
        activeList.append(active96)

        active97 = copy.deepcopy(active)
        active97.evaluator = EvaluatorIBLG_LONG_03()
        activeList.append(active97)

        active98 = copy.deepcopy(active)
        active98.evaluator = EvaluatorIBLG_LONG_04()
        activeList.append(active98)

        active99 = copy.deepcopy(active)
        active99.evaluator = EvaluatorIBLG_LONG_05()
        activeList.append(active99)

        active100 = copy.deepcopy(active)
        active100.evaluator = EvaluatorIBLG_LONG_06()
        activeList.append(active100)

        active101 = copy.deepcopy(active)
        active101.evaluator = EvaluatorIBLG_LONG_07()
        activeList.append(active101)

        active102 = copy.deepcopy(active)
        active102.evaluator = EvaluatorIBLG_LONG_08()
        activeList.append(active102)

        active103 = copy.deepcopy(active)
        active103.evaluator = EvaluatorIBLG_LONG_09()
        activeList.append(active103)

        active104 = copy.deepcopy(active)
        active104.evaluator = EvaluatorIBLG_MID_LONG_01()
        activeList.append(active104)

        active105 = copy.deepcopy(active)
        active105.evaluator = EvaluatorIBLG_MID_LONG_02()
        activeList.append(active105)

        active106 = copy.deepcopy(active)
        active106.evaluator = EvaluatorIBLG_PROB_FLOW_01()
        activeList.append(active106)

        active107 = copy.deepcopy(active)
        active107.evaluator = EvaluatorIBLG_PROB_FLOW_02()
        activeList.append(active107)

        active108 = copy.deepcopy(active)
        active108.evaluator = EvaluatorIBLG_START_CLOSE_01()
        activeList.append(active108)

        active109 = copy.deepcopy(active)
        active109.evaluator = EvaluatorIBLG_START_CLOSE_02()
        activeList.append(active109)

        active110 = copy.deepcopy(active)
        active110.evaluator = EvaluatorIBLG_START_CLOSE_03()
        activeList.append(active110)

        active111 = copy.deepcopy(active)
        active111.evaluator = EvaluatorIBLG_START_CLOSE_03_01()
        activeList.append(active111)

        # active112 = copy.deepcopy(active)
        # active112.evaluator = EvaluatorIBLG_START_CLOSE_03_BCKUP()
        # activeList.append(active112)

        active113 = copy.deepcopy(active)
        active113.evaluator = EvaluatorIBLG_START_CLOSE_04()
        activeList.append(active113)

        active114 = copy.deepcopy(active)
        active114.evaluator = EvaluatorIBLG_START_CLOSE_05()
        activeList.append(active114)

        active115 = copy.deepcopy(active)
        active115.evaluator = EvaluatorIBLG_WEEK_FLOW_01()
        activeList.append(active115)

        active116 = copy.deepcopy(active)
        active116.evaluator = EvaluatorIBLG_WEEK_FLOW_02()
        activeList.append(active116)

        active117 = copy.deepcopy(active)
        active117.evaluator = EvaluatorIBLG_WEEK_FLOW_03()
        activeList.append(active117)

        active118 = copy.deepcopy(active)
        active118.evaluator = EvaluatorIMA1Optimiz_MEDDIFF_01()
        activeList.append(active118)

        active119 = copy.deepcopy(active)
        active119.evaluator = EvaluatorIMA1Optimiz_MEDDIFF_02()
        activeList.append(active119)

        active120 = copy.deepcopy(active)
        active120.evaluator = EvaluatorIMA1_ANGLE_01()
        activeList.append(active120)

        active121 = copy.deepcopy(active)
        active121.evaluator = EvaluatorIMA1_ANGLE_02()
        activeList.append(active121)

        active122 = copy.deepcopy(active)
        active122.evaluator = EvaluatorIMA1_ANGLE_03()
        activeList.append(active122)

        active123 = copy.deepcopy(active)
        active123.evaluator = EvaluatorIMA1_CLEAN_BLG_01()
        activeList.append(active123)

        active124 = copy.deepcopy(active)
        active124.evaluator = EvaluatorIMA1_CLEAN_BLG_02()
        activeList.append(active124)

        active125 = copy.deepcopy(active)
        active125.evaluator = EvaluatorIMA1_CLEAN_BLG_03()
        activeList.append(active125)

        active126 = copy.deepcopy(active)
        active126.evaluator = EvaluatorIMA1_CLEAN_BLG_04()
        activeList.append(active126)

        active127 = copy.deepcopy(active)
        active127.evaluator = EvaluatorIMA1_CLEAN_BLG_04_ONLY_DOWN_01()
        activeList.append(active127)

        active128 = copy.deepcopy(active)
        active128.evaluator = EvaluatorIMA1_CLEAN_BLG_05()
        activeList.append(active128)

        active129 = copy.deepcopy(active)
        active129.evaluator = EvaluatorIMA1_CLEAN_BLG_06()
        activeList.append(active129)

        active130 = copy.deepcopy(active)
        active130.evaluator = EvaluatorIMA1_CLEAN_BLG_EXTREMES_01()
        activeList.append(active130)

        active131 = copy.deepcopy(active)
        active131.evaluator = EvaluatorIMA1_CLEAN_Optimiz01()
        activeList.append(active131)

        active132 = copy.deepcopy(active)
        active132.evaluator = EvaluatorIMA1_CLEAN_Optimiz02()
        activeList.append(active132)

        active133 = copy.deepcopy(active)
        active133.evaluator = EvaluatorIMA1_CLEAN_Optimiz03()
        activeList.append(active133)

        active134 = copy.deepcopy(active)
        active134.evaluator = EvaluatorIMA1_CLEAN_Optimiz04()
        activeList.append(active134)

        active135 = copy.deepcopy(active)
        active135.evaluator = EvaluatorIMA1_INDICATOR_MEDDIFF_01()
        activeList.append(active135)

        active136 = copy.deepcopy(active)
        active136.evaluator = EvaluatorIMA1_STDMED_Optimiz01()
        activeList.append(active136)

        active137 = copy.deepcopy(active)
        active137.evaluator = EvaluatorIWEEK_DIRECTION_01()
        activeList.append(active137)

        active138 = copy.deepcopy(active)
        active138.evaluator = EvaluatorMARKETTENDENCE_STDMED_01()
        activeList.append(active138)

        active139 = copy.deepcopy(active)
        active139.evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01()
        activeList.append(active139)

        active140 = copy.deepcopy(active)
        active140.evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_01_ONLYUP()
        activeList.append(active140)

        active141 = copy.deepcopy(active)
        active141.evaluator = EvaluatorMARKETTENDENCE_STDMED_MEDDIFF_02()
        activeList.append(active141)

        active142 = copy.deepcopy(active)
        active142.evaluator = EvaluatorMEDMOMENT_01_MEDDIFF_INDDIST_01()
        activeList.append(active142)

        active143 = copy.deepcopy(active)
        active143.evaluator = EvaluatorMEDMOMENT_CLEAN_MEDDIFF_01()
        activeList.append(active143)

        active144 = copy.deepcopy(active)
        active144.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz01()
        activeList.append(active144)

        active145 = copy.deepcopy(active)
        active145.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz02()
        activeList.append(active145)

        active146 = copy.deepcopy(active)
        active146.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03()
        activeList.append(active146)

        active147 = copy.deepcopy(active)
        active147.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF()
        activeList.append(active147)

        active148 = copy.deepcopy(active)
        active148.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz03_MEDDIFF01()
        activeList.append(active148)

        active149 = copy.deepcopy(active)
        active149.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz04()
        activeList.append(active149)

        active150 = copy.deepcopy(active)
        active150.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz05()
        activeList.append(active150)

        active151 = copy.deepcopy(active)
        active151.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06()
        activeList.append(active151)

        active152 = copy.deepcopy(active)
        active152.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz06_MEDDIFF_01()
        activeList.append(active152)

        active153 = copy.deepcopy(active)
        active153.evaluator = EvaluatorMEDMOMENT_CLEAN_Optimiz07_PERCENT()
        activeList.append(active153)

        active154 = copy.deepcopy(active)
        active154.evaluator = EvaluatorMEDSTDOptimiz01()
        activeList.append(active154)

        active155 = copy.deepcopy(active)
        active155.evaluator = EvaluatorMEDSTDOptimiz02()
        activeList.append(active155)

        active156 = copy.deepcopy(active)
        active156.evaluator = EvaluatorMEDSTDOptimiz03()
        activeList.append(active156)

        active157 = copy.deepcopy(active)
        active157.evaluator = EvaluatorMEDSTDOptimiz04()
        activeList.append(active157)

        active158 = copy.deepcopy(active)
        active158.evaluator = EvaluatorMEDSTDOptimiz04OnlyUp()
        activeList.append(active158)

        active159 = copy.deepcopy(active)
        active159.evaluator = EvaluatorMEDSTDOptimiz04OnlyUp01()
        activeList.append(active159)

        active160 = copy.deepcopy(active)
        active160.evaluator = EvaluatorMEDSTDOptimiz05()
        activeList.append(active160)

        active161 = copy.deepcopy(active)
        active161.evaluator = EvaluatorMEDSTDOptimiz06()
        activeList.append(active161)

        active162 = copy.deepcopy(active)
        active162.evaluator = EvaluatorMEDSTDOptimiz07()
        activeList.append(active162)

        active163 = copy.deepcopy(active)
        active163.evaluator = EvaluatorMEDSTDOptimiz08()
        activeList.append(active163)

        active164 = copy.deepcopy(active)
        active164.evaluator = EvaluatorMEDSTDOptimiz09()
        activeList.append(active164)

        active165 = copy.deepcopy(active)
        active165.evaluator = EvaluatorMEDSTDOptimiz10()
        activeList.append(active165)

        active166 = copy.deepcopy(active)
        active166.evaluator = EvaluatorMEDSTDOptimiz_MEDDIFF_07()
        activeList.append(active166)

        active167 = copy.deepcopy(active)
        active167.evaluator = EvaluatorMEDSTDRelative01()
        activeList.append(active167)

        active168 = copy.deepcopy(active)
        active168.evaluator = EvaluatorMEDSTDRelative02()
        activeList.append(active168)

        active169 = copy.deepcopy(active)
        active169.evaluator = EvaluatorMEDSTDRelative03()
        activeList.append(active169)

        active170 = copy.deepcopy(active)
        active170.evaluator = EvaluatorMEDSTDRelative04()
        activeList.append(active170)

        active171 = copy.deepcopy(active)
        active171.evaluator = EvaluatorMEDSTDRelative04OnlyUP()
        activeList.append(active171)

        active172 = copy.deepcopy(active)
        active172.evaluator = EvaluatorMEDSTD_WEEK_MEDDIFF_01()
        activeList.append(active172)

        active173 = copy.deepcopy(active)
        active173.evaluator = EvaluatorMEDSTD_WEEK_Optimiz01()
        activeList.append(active173)

        active174 = copy.deepcopy(active)
        active174.evaluator = EvaluatorMEDSTD_WEEK_Optimiz02()
        activeList.append(active174)

        active175 = copy.deepcopy(active)
        active175.evaluator = EvaluatorMEDSTD_WEEK_Optimiz03()
        activeList.append(active175)

        active176 = copy.deepcopy(active)
        active176.evaluator = EvaluatorMED_MOMENTOptimiz01OnlyUp()
        activeList.append(active176)

        active177 = copy.deepcopy(active)
        active177.evaluator = EvaluatorMED_WEEK_Optimiz01()
        activeList.append(active177)

        active178 = copy.deepcopy(active)
        active178.evaluator = EvaluatorMED_WEEK_Optimiz02()
        activeList.append(active178)

        active179 = copy.deepcopy(active)
        active179.evaluator = EvaluatorOnlyUp01()
        activeList.append(active179)

        active180 = copy.deepcopy(active)
        active180.evaluator = EvaluatorOnlyUp02()
        activeList.append(active180)

        active181 = copy.deepcopy(active)
        active181.evaluator = EvaluatorOnlyUp03()
        activeList.append(active181)

        active182 = copy.deepcopy(active)
        active182.evaluator = EvaluatorOnlyUp04()
        activeList.append(active182)

        active183 = copy.deepcopy(active)
        active183.evaluator = EvaluatorOnlyUp05()
        activeList.append(active183)

        active184 = copy.deepcopy(active)
        active184.evaluator = EvaluatorOnlyUp06()
        activeList.append(active184)

        active185 = copy.deepcopy(active)
        active185.evaluator = EvaluatorOnlyUp07()
        activeList.append(active185)

        active186 = copy.deepcopy(active)
        active186.evaluator = EvaluatorOnlyUp08()
        activeList.append(active186)

        active187 = copy.deepcopy(active)
        active187.evaluator = EvaluatorOnlyUp09()
        activeList.append(active187)

        active188 = copy.deepcopy(active)
        active188.evaluator = EvaluatorOnlyUpMARKET01()
        activeList.append(active188)

        active189 = copy.deepcopy(active)
        active189.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt01()
        activeList.append(active189)

        active190 = copy.deepcopy(active)
        active190.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt02()
        activeList.append(active190)

        active191 = copy.deepcopy(active)
        active191.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03()
        activeList.append(active191)

        active192 = copy.deepcopy(active)
        active192.evaluator = EvaluatorPROBMEDSTD_CLEAN_Opt03_MEDDIFF_01()
        activeList.append(active192)

        active193 = copy.deepcopy(active)
        active193.evaluator = EvaluatorPROBMEDSTD_MEDDIFF_BLG_01()
        activeList.append(active193)

        active194 = copy.deepcopy(active)
        active194.evaluator = EvaluatorPROBMEDSTD_MEDDIFF_BLG_02()
        activeList.append(active194)

        active195 = copy.deepcopy(active)
        active195.evaluator = EvaluatorRELATIVE_MEDSTD_01()
        activeList.append(active195)

        active196 = copy.deepcopy(active)
        active196.evaluator = EvaluatorRELATIVE_MEDSTD_02()
        activeList.append(active196)

        active197 = copy.deepcopy(active)
        active197.evaluator = EvaluatorRELATIVE_MEDSTD_03()
        activeList.append(active197)

        active198 = copy.deepcopy(active)
        active198.evaluator = EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_01()
        activeList.append(active198)

        active199 = copy.deepcopy(active)
        active199.evaluator = EvaluatorRELATIVE_MEDSTD_03_MEDDIFF_02()
        activeList.append(active199)

        active200 = copy.deepcopy(active)
        active200.evaluator = EvaluatorRELATIVE_MEDSTD_ONLYUP_01()
        activeList.append(active200)

        active201 = copy.deepcopy(active)
        active201.evaluator = EvaluatorRSI_01()
        activeList.append(active201)

        active202 = copy.deepcopy(active)
        active202.evaluator = EvaluatorRSI_ONLYUP_01()
        activeList.append(active202)

        active203 = copy.deepcopy(active)
        active203.evaluator = EvaluatorSTDMarketOptimiz01()
        activeList.append(active203)

        active204 = copy.deepcopy(active)
        active204.evaluator = EvaluatorSTDMarketOptimiz02()
        activeList.append(active204)

        active205 = copy.deepcopy(active)
        active205.evaluator = EvaluatorSUPERBOT_ALPHA_01()
        activeList.append(active205)

        # active206 = copy.deepcopy(active)
        # active206.evaluator = factory()
        # activeList.append(active206)

        return activeList

    def prepareActivesEvaluators3(self, active):
        activeList = list()

        active1 = copy.deepcopy(active)
        active1.evaluator = EvaluatorIMA1_ANGLE_01()
        activeList.append(active1)

        active2 = copy.deepcopy(active)
        active2.evaluator = EvaluatorIBLG_LONG_03()
        activeList.append(active2)

        active3 = copy.deepcopy(active)
        active3.evaluator = EvaluatorIBLG_START_CLOSE_03()
        activeList.append(active3)

        active4 = copy.deepcopy(active)
        active4.evaluator = EvaluatorIBLG_LONG_08()
        activeList.append(active4)

        active5 = copy.deepcopy(active)
        active5.evaluator = EvaluatorIBLG_ANGLE_FLOW_LONG_01()
        activeList.append(active5)





        return activeList

    def prepareActivesEvaluatorsONLYUP(self, active):
        activeList = list()

        active1 = copy.deepcopy(active)
        active1.evaluator = EvaluatorOnlyUp06()
        activeList.append(active1)

        active2 = copy.deepcopy(active)
        active2.evaluator = EvaluatorMEDSTDOptimiz04OnlyUp()
        activeList.append(active2)

        active3 = copy.deepcopy(active)
        active3.evaluator = EvaluatorRELATIVE_MEDSTD_ONLYUP_01()
        activeList.append(active3)

        active4 = copy.deepcopy(active)
        active4.evaluator = EvaluatorBOLLINGER_ONLY_UP_03()
        activeList.append(active4)

        active5 = copy.deepcopy(active)
        active5.evaluator = EvaluatorIBLG_LONG_ONLY_UP_01()
        activeList.append(active5)

        active6 = copy.deepcopy(active)
        active6.evaluator = EvaluatorIMA1_CLEAN_BLG_04_ONLY_UP_01()
        activeList.append(active6)

        active7 = copy.deepcopy(active)
        active7.evaluator = EvaluatorDistIndicatorTenOnlyUp01()
        activeList.append(active7)

        active8 = copy.deepcopy(active)
        active8.evaluator = EvaluatorIBLG_LONG_ONLY_UP_02()
        activeList.append(active8)

        active9 = copy.deepcopy(active)
        active9.evaluator = EvaluatorIBLG_LONG_ONLY_UP_00()
        activeList.append(active9)

        active10 = copy.deepcopy(active)
        active10.evaluator = EvaluatorMED_MOMENTOptimiz01OnlyUp()
        activeList.append(active10)

        active11 = copy.deepcopy(active)
        active11.evaluator = EvaluatorIBLG_LONG_ONLY_UP_05()
        activeList.append(active11)

        active12 = copy.deepcopy(active)
        active12.evaluator = EvaluatorIBLG_LONG_ANGLE_ONLY_UP_01()
        activeList.append(active12)

        active12 = copy.deepcopy(active)
        active12.evaluator = EvaluatorIBLG_LONG_ANGLE_ONLY_UP_02()
        activeList.append(active12)

        active13 = copy.deepcopy(active)
        active13.evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_05_test01()
        activeList.append(active13)

        active14 = copy.deepcopy(active)
        active14.evaluator = EvaluatorIBLG_ANGLE_ONLY_UP_05_test07()
        activeList.append(active14)

        return activeList
    def prepareActivesEvaluatorsONLYUPNEW(self, active):
        activeList = list()

        active1 = copy.deepcopy(active)
        active1.evaluator = EvaluatorEMA_LONG_ONLY_UP_01()
        activeList.append(active1)

        active2 = copy.deepcopy(active)
        active2.evaluator = EvaluatorEMA_LONG_ONLY_UP_03_01()
        activeList.append(active2)

        active3 = copy.deepcopy(active)
        active3.evaluator = EvaluatorEMA_LONG_ONLY_UP_04()
        activeList.append(active3)

        active4 = copy.deepcopy(active)
        active4.evaluator = EvaluatorEMA_LONG_ONLY_UP_04_01()
        activeList.append(active4)

        active5 = copy.deepcopy(active)
        active5.evaluator = EvaluatorRSI_ONLYUP_01()
        activeList.append(active5)

        active6 = copy.deepcopy(active)
        active6.evaluator = EvaluatorBTCUSD_ONLY_BUY_01()
        activeList.append(active6)

        active7 = copy.deepcopy(active)
        active7.evaluator = EvaluatorETHUSD_ONLY_BUY_01()
        activeList.append(active7)

        active8 = copy.deepcopy(active)
        active8.evaluator = EvaluatorEMA_IA_LONG_ONLY_UP()
        activeList.append(active8)

        active9 = copy.deepcopy(active)
        active9.evaluator = EvaluatorEMA_IA_ONLY_UP_01()
        activeList.append(active9)

        active10 = copy.deepcopy(active)
        active10.evaluator = EvaluatorEMA_IA_ONLY_UP_02()
        activeList.append(active10)

        active11 = copy.deepcopy(active)
        active11.evaluator = EvaluatorEMA_IA_LONG_ONLY_UP_CROSS()
        activeList.append(active11)








        return activeList

    def \
             prepare_Actives_Start_CLose_Evaluators(self, active):
        activeList = list()
        startList = list()
        endList = list()

        # start
        # startList.append("getANGLE_START_BLG_01") #getANGLE_START_BLG_02
        startList.append("getANGLE_START_BLG_02")
        startList.append("getANGLE_START_BLG_03")
        startList.append("getProb_START_ANGLE_H_01")
        startList.append("getProb_START_ANGLE_H_02")
        startList.append("getANGLE_START_BLG_04")
        startList.append("getANGLE_START_EMA_RSI_01")

        # end
        # endList.append("getProb_HOURLY_ANGLE_01")#getProb_END_HOURLY_ANGLE_02
        endList.append("getProb_END_HOURLY_ANGLE_03")
        endList.append("getProb_END_HOURLY_ANGLE_02")
        endList.append("getProb_END_HOURLY_ANGLE_05")
        endList.append("getProb_END_EMA_RSI_01")

        for s in startList:
            for e in endList:

                active = copy.deepcopy(active)
                active.parameters.startProbDef = s
                active.parameters.endProbDef = e

                activeList.append(active)

        return activeList

    def prepare_EMA_parameters(self, active):
        activeList = list()
        startList = list()
        endList = list()

        # start
        # startList.append("getANGLE_START_BLG_01") #getANGLE_START_BLG_02
        startList.append(5)
        startList.append(10)
        startList.append(15)

        # end
        # endList.append("getProb_HOURLY_ANGLE_01")#getProb_END_HOURLY_ANGLE_02
        endList.append(20)
        endList.append(25)
        endList.append(30)

        for s in startList:
            for e in endList:

                active = copy.deepcopy(active)
                active.parameters.ema10 = s
                active.parameters.ema20 = e

                activeList.append(active)

        return activeList

    def prepare_Actives_Control_Evaluators(self, active):
        activeList = list()
        startList = list()
        endList = list()

        # start
        # startList.append("getANGLE_START_BLG_01") #getANGLE_START_BLG_02
        startList.append("control_BUY_BLG_01")
        startList.append("control_BUY_BLG_02")
        # startList.append("getProb_START_ANGLE_H_01")
        # startList.append("getProb_START_ANGLE_H_02")
        # startList.append("getANGLE_START_BLG_04")

        # end
        # endList.append("getProb_HOURLY_ANGLE_01")#getProb_END_HOURLY_ANGLE_02
        endList.append("control_SELL_BLG_01")
        # endList.append("control_SELL_BLG_02")
        endList.append("control_SELL_BLG_03")

        for s in startList:
            for e in endList:

                active = copy.deepcopy(active)
                active.parameters.dinamicControl = True
                active.parameters.controlBUY = s
                active.parameters.controlSELL = e

                activeList.append(active)

        return activeList

    def angleExclusion(self,results, activeName):
        res = False
        exclusion = ""
        if activeName in exclusion:
            res = True
        return res