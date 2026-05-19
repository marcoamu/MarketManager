"""Simulation module for MarketManager - standalone functions."""

from core.simulation.analysis import (
    generateAnalisysData,
    generateAnalisysDataColoredOK,
    generateAnalisysDataColored,
    evaluateMarketMovements,
)

from core.simulation.simulate import (
    simulateFlowConfig,
    simulateFlow,
    RealModeConfig,
    RealMode,
    RealModeLocal,
    drawActive,
    drawActiveDates,
    drawActiveDatesSelected,
    simulateFlowActive,
    drawRelativeTendence,
    simulateWeekDirection,
    simulateIndicatorDates,
    simulateEvaluatorsForActiveDates,
    simulate_Star_Close_ForActiveDates,
    simulate_EMA_parameters_ForActiveDates,
    simulate_Control_ForActiveDates,
)

__all__ = [
    # Analysis
    'generateAnalisysData',
    'generateAnalisysDataColoredOK',
    'generateAnalisysDataColored',
    'evaluateMarketMovements',
    # Simulate
    'simulateFlowConfig',
    'simulateFlow',
    'RealModeConfig',
    'RealMode',
    'RealModeLocal',
    'drawActive',
    'drawActiveDates',
    'drawActiveDatesSelected',
    'simulateFlowActive',
    'drawRelativeTendence',
    'simulateWeekDirection',
    'simulateIndicatorDates',
    'simulateEvaluatorsForActiveDates',
    'simulate_Star_Close_ForActiveDates',
    'simulate_EMA_parameters_ForActiveDates',
    'simulate_Control_ForActiveDates',
]