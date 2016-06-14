# APS - Avalanche Problem Solver

Tools for effective avalanche forecasting.

The Norwegian Avalanche Center is developing a new avalanche forecasting system with the goal to provide automated forecasts to support the avalanche forecasters in their daily work routine.

The system should be able to collect and filter relevant weather and snow information from various sources. Main sources are the observational database regobs.no, the seNorge/xgeo snow models, the numerical weather prediction model AROME-MetCoop, and the weather observation database eklima.no.

The system should model the following workflow:

- analysis of the currently valid avalanche forecast (danger level, avalanche problem, persistent weak layers, current and upcoming weather issued)
- cross-check the current forecast against recent snow and weather observations
- update now-cast based on cross-check
- analyze weather prediction and snow pack models with regard to effects on avalanche danger, avalanche problems
- combine now-cast and prognosis to a draft of the forecast for the next 48 hours including danger level, avalanche problem, and weather forecast
- the forecaster needs to control the draft and update the text manually

Based on the definitions for each avalanche problem, we try to define the main parameters controlling each problem. We want to set up table/matrix/sheet linking each parameter and dependencies for each avalanche problem.
Final product of APS

The avalanche problem solver should provide a danger level, avalanche problem(s) (distribution/ranking) and a weather/snowpack overview for each region each day.
Xgeo-map: a map layer that indicates the terrain where each avalanche problem is present (region, elevation, aspect); indicate which competence is necessary to manage that kind of terrain depending on the danger level, avalanche problem, steepness