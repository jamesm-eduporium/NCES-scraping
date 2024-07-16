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

The entire system can be ran at once by using the run_all.py file.

_All data is only representative of Public Schools in the United States, and may not be the latest data._
**This project was written entirely by James McGillicuddy for the sole use of Eduporium.**



## STATISTICS (last updated 07/16/24):

Emails Accessed: 27247

School District Websites Found: 16042

School Directories Found: 6583

Schools Found: 6688

Staff Directories Found: 9985 (Some staff directories were found directly from the school directory, which is why there are more directories than schools.)



## SUCCESS RATE (last updated 07/16/24):

Success rate can be different as each module had its own success rate from input to output, and none besides module 6 reached over 95%.
However, on a dataset as large as this a success rate of even 5% is acceptable for practical purposes. Therefore, I have listed out all
"possible" success rates.

I have again used NCES for the following data. All of the data is either directly reported or derived from that data. Values may
be slightly changed as some data is from 2020-2021, but the variance is not significant enough for the purposes of this project.

- Amount of Public Schools: 98,328
- (Average) Teachers per School District: 193.3 (TPSD)
- (Average) Teachers per School: 38.28 (TPS)


1. 27,247 emails / (19442 school districts * 193.3 TPSD) = _27,247 / 3,758,138.6_ = `0.725%`

2. 27,247 emails / (16042 accessed school districts * 193.3 TPSD) = _27,247 / 3,100,918.6_ = `0.879%`

3. 27,247 emails / (6583 school directories * 193.3 TPSD) = _27,247 / 1,272,493.3_ = `2.141%`

4. 27,247 emails / (9985 staff directories * 38.28 TPS) = _27,247 / 382,225.8_ = `7.129%`

All four of these numbers represent different perspectives of success, ranging an order of magnitude. The first value can represent that almost 1% of all teacher emails in the United States have been accessed and stored. About the same percentage is shown in the second value, which shows that the system is able to get almost all, or _16042 / 19442 = 82.5%_ of school district sites from NCES. This is promising as a good portion of districts do not have a URL listed or fall into another bucket that is not helpful for this project, so the system pretty much nears 100% efficiency on that mark.

The third and fourth values also give insight on the effectiveness of the system when "entered" at different steps. Looking from step 2 -> 3, there is a large drop off in number of sites. This is due to the swap from one domain to the variety of domains of each school district. This is one (if not the most applicable) section of improvement for the system, but it still remains the most difficult. Regardless, the percentage there shows that the system was successful in ~2% of all school districts **it was able to find in previous steps**. The same can be said for step four.

These small percentages represent massive wins for the system. A task like webscraping can only produce so much, as it
inherently approaches a limit due to the vast differences in all of the site design. When looking back at the 27,247 figure, while that can be represented as a small percentage, it also represents the amount of potential customers gained which makes it appear much larger. However, that limit has not yet been met by this system and I will continue to attempt to increase it by accessing more schools and staff directories, and also having a higher html parsing success rate. LLMs and other AIs can also be used to find directories more efficiently and without as much fail.