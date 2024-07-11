# NCES Web Scraping System for Staff Emails

This is a system of scraping that utilizes mainly bs4 and Selenium to gain faculty emails from as many public schools
in the United States as possible. Starting with data accessed from the National Center for Education Statistics (NCES),
that data is then filtered through 7 seperate modules. Each module acts as a machine taking an input and performing a task
on that input to provide the correct output for the next module. The order of operations is as follows:

- Module 1 - Access all reference pages from the main search function of NCES
- Module 2 - From each reference page, access the listed school district website
- Module 3 - Attempts to find all school directories for each district
- Module 4 - Filters and seperates the located school directory links
- Module 5 - Finds all the staff directories that were not found in Module 4
- Module 6 - Accesses each staff directory and stores their HTML content for parsing
- Module 7 - Parses all of the stored HTML and stores all emails found

In theory, this system needs to only be executed once, storing all of the desired emails after the final module is finished.
However, it was written with re-use in mind, and can be re-run efficiently and autonomously. This was for a few reasons, including
natural growth of school districts over time, and a slightly variety in results each execution due to site loading times,
district maintinence, and an assortment of other reasons that result in slightly changed values each time (Usually less than 1%).

When they are run in conjunction, expect the process to take about 3.5 - 4 hours, although this number may vary drastically depending
on connection speeds and other external factors. The entire system can be ran at once by using the run_all.py file.

_All data is only representative of Public Schools in the United States, and may not be the latest data._
_**This project was written entirely by James McGillicuddy for the sole use of Eduporium.**_



## STATISTICS (last updated 07/09/24):

Emails Accessed: 14,955

School District Websites Found: 5883

School Directories Found: 2863

Schools Found: 4005

Staff Directories Found: 3895



## SUCCESS RATE (last updated 07/09/24):

Success rate can be different as each module had its own success rate from input to output, and none besides module 6 reached over 95%.
However, on a dataset as large as this a success rate of even 5% is acceptable for practical purposes. Therefore, I have listed out all
"possible" success rates.

I have again used NCES for the following data. All of the data is either directly reported or derived from that data. Values may
be slightly changed as some data is from 20202-2021, but the variance is not significant enough for the purposes of this project.

Amount of Public Schools: 98,328
(Average) Teachers per School District: 193.3 (TPSD)
(Average) Teachers per School: 38.28 (TPS)


1. 14,955 emails / (19473 school districts * 193.3 TPSD) = _14,955 / 3,764,130.9_ = `0.397%`

2. 14,955 emails / (5883 accessed school districts * 193.3 TPSD) = _14,955 / 1,137,183.9_ = `1.315%`

3. 14,955 emails / (2863 school directories * 193.3 TPSD) = _14,955 / 553,417.9_ = `2.702%`

4. 14,955 emails / (3895 staff directories * 38.28 TPS) = _14,955 / 125,730.6_ = `11.894%`

All four of these numbers display different perspectives of success. The first, 0.397%, displays that the system was able
to access about half a percent of every single possible email it could. While overarching, this number does not show much as
almost 75% of school districts on NCES either consisted of less than 4 schools or did not list a website. Therefore, there is
little the system can do to improve the number of districts accessed. 

Thats why the second value is much more valuable. It displays the total percentage found of all districts that could actually be accessed.
This gives a better insight and says that for any given school district url, expect a ~1.3% success rate.

The third and fourth values also give insight on the effectiveness of the system when "entered" at different steps, however
they only display the effectiveness of part of the system rather than the whole. So while they show important information
about individual sections of the system, I believe that the 2nd value still represents the overarching system the best.


These small percentages represent massive wins for the system. A task like webscraping, especially using just bs4 and Selenium,
inherently approach a limit due to the vast differences in all of the site design. At some point it becomes more efficient to
go to each site and write down the emails by hand rather than to write scraping code so specific it cannot work for any other site.
However, the limit has not yet been met and I will continue to attempt to increase it by accessing more schools and staff directories,
and also having a higher html parsing success rate. LLMs and other AIs can also be used to find directories more efficiently and without
as much fail.