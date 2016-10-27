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