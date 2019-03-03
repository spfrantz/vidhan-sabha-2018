# Vidhan Sabha 2018 election results

This repository contains constituency-level results from five Indian state assembly (Vidhan Sabha) elections conducted in 2018. The results were collected from the Election Commission of India (ECI) website on March 2, 2019.

The five states are:
* Chhattisgarh
* Madhya Pradesh
* Mizoram
* Rajasthan
* Telangana

Formatting is per the ECI website; I have not made any attempt to improve its consistency.

Note that constituency IDs are unique per state but not unique overall (e.g., there is a constituency 1 in both Rajasthan and Mizoram, etc.).

I have also included the simple Python script used to collect the results. In addition to the two packages listed in `requirements.txt`, the script requires Google Chrome and the [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) package.
