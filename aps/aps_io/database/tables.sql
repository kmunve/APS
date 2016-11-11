/*
SQL commands to set-up dummy database for the APS project.
Using SQLite dialect.
*/


/*


*/
CREATE TABLE Regions(
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  extent TEXT -- probably a polygon or other element that maps to the seNorge grid
  );

-- could also be a part of the Regions table if there are not good reasons to separate it.
CREATE TABLE Regional_terrain_attributes(
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  grid_index_low_left_x INT,
  grid_index_low_left_y INT,
  grid_index_up_right_x INT,
  grid_index_up_right_y INT,
  total_land_area REAL,
  min_elevation REAL,
  max_elevation REAL,
  avg_elevation REAL,
  elevation_band_1_bot REAL,
  elevation_band_1_top REAL,
  elevation_band_2 (bot REAL, top REAL), -- is it possible to have tuples in SQL server?
  elevation_band_3 (bot REAL, top REAL),
  elevation_band_4 (bot REAL, top REAL),
  elevation_band_5 (bot REAL, top REAL),
  elevation_band_1_total_area REAL,
  elevation_band_2_total_area REAL,
  elevation_band_3_total_area REAL,
  elevation_band_4_total_area REAL,
  elevation_band_5_total_area REAL,
  percentage_aval_terrain REAL,
  elevation_band_1_aval_terrain REAL,
  elevation_band_2_aval_terrain REAL,
  elevation_band_3_aval_terrain REAL,
  elevation_band_4_aval_terrain REAL,
  elevation_band_5_aval_terrain REAL,
  avg_treeline REAL
  );

/*
Table containing information on the temperature distribution within a forecasting region
at different elevation bands.
Observation: The temperature data comes from the seNorge grid within the region boundaries
Should it b possible that the tops and bottoms of the elevation bands overlap?
*/
CREATE TABLE Temperature_distribution(
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  region TEXT,
  date DATE,
  elevation_bottom INTEGER,
  elevation_top INTEGER,
  median REAL,
  first_quartile REAL,
  third_quartile REAL,
  min REAL,
  max REAL,
  avg_freezing_level REAL,
  freezing_night BOOLEAN,

  FOREIGN KEY(region) REFERENCES Regions(name)
  );


/*

 */



/*
Table containing the score for the four main avalanche problems for each region and day.

 */
CREATE TABLE Avalanche_problem_score(
  ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  region TEXT,
  date DATE,
  new_snow_score INTEGER,
  wind_slab_score INTEGER,
  pwl_score INTEGER,
  wet_snow_score INTEGER,
  FOREIGN KEY(region) REFERENCES Regions(name)
  );