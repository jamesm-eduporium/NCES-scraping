# NCES Web Scraping System for Staff Emails

This is a system of scraping that utilizes mainly bs4 and Selenium to gain faculty emails from as many public schools in the United States as possible. Starting with data accessed from the National Center for Education Statistics (NCES), that data is then filtered through 7 seperate modules. Each module acts as a machine taking an input and performing a task on that input to provide the correct output for the next module. The order of operations is as follows:

- Module 1 - Access all reference pages from the main search function of NCES
- Module 2 - From each reference page, access the listed school district website
- Module 3 - Attempts to find all school directories for each district
- Module 4 - Filters and seperates the located school directory links
- Module 5 - Finds all the staff directories that were not found in Module 4
- Module 6 - Accesses each staff directory and stores their HTML content for parsing
- Module 7 - Parses all of the stored HTML and stores all emails found

In theory, this system needs to only be executed once, storing all of the desired emails after the final module is finished. However, it was written with re-use in mind, and can be re-run efficiently and autonomously. This was for a few reasons, including natural growth of school districts over time, and a slightly variety in results each execution due to site loading times, district maintinence, and an assortment of other reasons that result in slightly changed values each time (Usually less than 1%).

The entire system can be ran at once by using the run_all.py file. Runtime will vary depending on internet speeds, system starting point, and a myriad of other factors, but one could expect a long runtime if they were to reset the system from scratch, in the range of 10-14 hours. Over half of this runtime is due to Modules 1 and 2, which are the least likely to vary over time, so instead it is reccomended to start from module three. This should result in a runtime of about 2 hours.

_All data is only representative of Public Schools in the United States, and may not be the latest data._

**This project was written entirely by James McGillicuddy for the sole use of Eduporium.**



## STATISTICS (last updated 07/16/24):

Emails Accessed: 57580

School District Websites Found: 16042

School Directories Found: 11827

Schools Found: 6585

Staff Directories Found: 13,397 (Some staff directories were found directly from the school directory, which is why there are more staff directories than schools.)



## SUCCESS RATE (last updated 07/16/24):

I have again used NCES for the following data. All of the data is either directly reported or derived from that data. Values may be slightly changed as some data is from 2020-2021, but the variance is not significant enough for the purposes of this project.

- Amount of Public Schools: 98,328
- (Average) Teachers per School District: 193.3 (TPSD)
- (Average) Teachers per School: 38.28 (TPS)


1. 57,580 emails / (19442 school districts * 193.3 TPSD) = _57,580 / 3,758,138.6_ = `1.532%`

2. 57,580 emails / (16042 accessed school districts * 193.3 TPSD) = _57,580 / 3,100,918.6_ = `1.857%`

3. 57,580 emails / (11827 school directories * 193.3 TPSD) = _57,580 / 2,286,159.1_ = `2.519%`

4. 57,580 emails / (13397 staff directories * 38.28 TPS) = _57,580 / 512,837.16_ = `11.228%`

All four of these numbers represent different perspectives of success, ranging an order of magnitude. The first value can represent that over 1% of all teacher emails in the United States have been accessed and stored. About the same percentage is shown in the second value, which shows that the system is able to get almost all, or _16042 / 19442 = 82.5%_ of school district sites from NCES. This is promising as a good portion of districts do not have a URL listed or fall into another bucket that is not helpful for this project, so the system pretty much nears 100% efficiency on that mark.

The third and fourth values also give insight on the effectiveness of the system when "entered" at different steps. Looking from step 2 -> 3, there is a large drop off in number of sites. This is due to the swap from one domain to the variety of domains of each school district. This is one (if not the most applicable) section of improvement for the system, but it still remains the most difficult. Regardless, the percentage there shows that the system was successful in ~2% of all school districts **it was able to find in previous steps**. The same can be said for step four.

These small percentages represent massive wins for the system. A task like webscraping can only produce so much, as it inherently approaches a limit due to the vast differences in all of the site design. When looking back at the 57,580 figure, while that can be represented as a small percentage, it also represents the amount of potential customers gained which makes it appear much larger. However, that limit has not yet been met by this system and I will continue to attempt to increase it by accessing more schools and staff directories. The first iteration of the completed system found 19,275 emails, which means as of writing it has improved **298.73%**, and only stands to improve even more!