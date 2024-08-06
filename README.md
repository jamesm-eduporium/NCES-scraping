# NCES Scraping Project

This is a webscraping project authored and devloped by James McGillicuddy for the sole use of Eduoporium.

## Welcome!
This project was built on the foundation of the National Center of Education Statistic's (NCES) school finder, which you can find [here](https://nces.ed.gov/ccd/schoolsearch/index.asp). The main premise lead generation, from that site to a list of staff data. I did this through a system of "modules" as I called them. I think of it as a I/O flow chart, where each module takes the input generated before it and outputs the next module's input. It looks like this:

NCES School Searcher --> NCES School Page --> School's Page --> School's Staff Directory --> Staff Data

Most of this was completed in Python with bs4 and Selenium. The system as a whole consists of two main parts, which I have dubbed main modules and fs pages. These (which you can check out at [main-modules](./main_modules/README.md) and [fs-pages](./fs_pages/README.md)) serve two different purposes. Main modules goes all the way from NCES School Searcher to each staff directory's HTML content. It then finds some emails there, but the bulk of the data is found by the fs-pages modules.

## By The Numbers

After running the system, a total of `INSERT TOTAL NUMBER OF LEADS HERE` leads were generated! Of these leads, `INSERT NUMBER OF COMPLETE LEADS HERE` were complete (i.e they contain name, title(s), and email). The rest of the leads still contain valuable information, with 100% containing email and many containing just the titles or names, but oftentimes those two variables can be found by a google search of the email. This was such a huge win for not only the system, but me personally as well. This was my first time working not only with web scraping but python in general. The very first run through of this system produced just 19,000 staff members, and even then that was only their emails. Since the first iteration, the system has seen a `INSERT PERCENTAGE HERE` improvement. However, that also means that it takes a lot longer to run. The code can certainly be optimized further, and perhaps one day it will. The good news is that this system does not need to be run often. Once it is run, the data is stored forever and will probably not have to be ran again for a year or more.