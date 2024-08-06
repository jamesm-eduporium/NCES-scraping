## FS Page Scraping

The fs in fs-pages stands for Finalsite, a customer relationship manager (CRM). When checking the HTML, `INSERT NUMBER OF SITES HERE` schools seemed to use Finalsite, by checking for the string 'finalsite' in their HTML source. This meant that all of those schools, for the most part, would have the exact same structure so I could build one system that is pretty much guarenteed to work on them.

This ended up being the case, and I used Selenium to check through every site and gather each staff member's name, title(s), and email. If the system failed to scrape any of them, it is a 99.99% chance that it was left blank by the school's site, which explains why so many of the staff member's data is not "complete". Feel free to check out the individual scripts to get some more specific documentation about them.

- [Get FS Pages](./scripts/get_fs_pages.py)
- [Scrape FS Pages](./scripts/scrape_fs_pages.py)
- [Normalzie FS Pages](./scripts/normalize_fs_data.py)

Click [here](../README.md) to head back to the main documentation.