# Covid-19 Data Google Sheets & Excel Spreadsheet Add-on

A variety of data about Covid-19 is available on GitHub in CSV format. Three important sources include Github Repositories with data from [John's Hopkin's University](https://github.com/CSSEGISandData/COVID-19), the [New York Times](https://github.com/nytimes/covid-19-data), and [Our World In Data](https://github.com/owid/covid-19-data).

The Flex.io Covid-19 spreadsheet functions allow data from these sources to be easily accessed in a spreadsheet as a function with search capabilities. Here are some examples:

* Return rows containing "Illinois" and "Cook" between 2020-04-01 and 2020-04-30 with all information from John's Hopkin's Covid-19 incident data:
```
=FLEX("covid-19-cases-jhu", "*", "+Illinois +Cook +date:[2020-04-01 TO 2020-04-30]")
```

* Return rows containing "Illinois" for "2020-04-01" with all information from New York Times Covid-19 incident data:
```
=FLEX("covid-19-cases-nyt", "*", "+Illinois +date:2020-04-01")
```

* Return rows containing "CDC" and "United States" with all information from "Our World In Data" Covid-19 test data:
```
=FLEX("covid-19-tests-owid", "*", "+CDC +\"United States\"")

This repository contains the code that implements the data feed to pull data from the various repositories to populate an index that powers the functions in the Flex.io Covid-19 integration. The actual functions are available in the [Flex.io Covid-19 Repository](https://github.com/flexiodata/functions-covid-19). See below for information about how to install the functions to access data from this feed.

## Prerequisites

The Flex.io Covid-19 spreadsheet functions utilize [Flex.io](https://www.flex.io). To use these functions, you'll need:

* A [Flex.io account](https://www.flex.io/app/signup) to run the functions
* A [Flex.io Add-on](https://www.flex.io/add-ons) for Microsoft Excel or Google Sheets to use the functions in your spreadsheet

## Installing the Functions

Once you've signed up for Flex.io and have the Flex.io Add-on installed, you're ready to install the function pack. To install the function pack, go to the [Flex.io Covid-19 Integration](https://www.flex.io/integrations/covid-19) and click "TRY IT NOW".

If you prefer, you can also install these functions directly by mounting this repository in Flex.io:

1. [Sign in](https://www.flex.io/app/signin) to Flex.io
2. In the Functions area, click the "New" button in the upper-left and select "Function Mount" from the list
3. In the function mount dialog, select "GitHub", then authenticate with your GitHub account
4. In the respository URL box, enter the name of this repository, which is "flexiodata/functions-covid-19"
5. Click "Create Function Mount"

## Using the Functions

Once you've installed the function pack, you're ready to use the functions.

1. Open Microsoft Excel or Google Sheets
2. Open the Flex.io Add-in:
   - In Microsoft Excel, select Home->Flex.io
   - In Google Sheets, select Add-ons->Flex.io
3. In the Flex.io side bar, log in to Flex.io and you’ll see the functions you have installed
4. For any function, click on the “details” in the function list to open a help dialog with some examples you can try at the bottom
5. Simply copy/paste the function into a cell, then edit the formula with a value you want to use

## Sources

The data for the Flex.io Add-on is pulled from data curated by John's Hopkins University, the New York Times, and Our World In Data. The data for each of these is available per the individual licenses in each of the respective repositories. Here are links to the sources and related information.

Data from Johns Hopkins Center for Systems Science and Engineering:
  * Johns Hopkins Covid-19 GitHub Repo Source Data: \
    https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
  * Johns Hopkins Covid-19 GitHub Repo Source Data README: \
    https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
  * Johns Hopkins Covid-19 GitHub Repo: \
    https://github.com/CSSEGISandData/COVID-19
  * Johns Hopkins Covid-19 Visualization: \
    https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
  * Johns Hopkins Center for Systems Science and Engineering (CSSE): \
    https://systems.jhu.edu/

Data from The New York Times, based on reports from state and local health agencies:
  * New York Times Covid-19 GitHub Repo Source Data: \
    https://github.com/nytimes/covid-19-data
  * New York Times Covid-19 Tracking Page: \
    https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html

Data from Our World In Data, based on data collected by the Our World in Data team from official reports:
  * Our World In Data Covid-19 GitHub Repo Source Data: \
    https://github.com/owid/covid-19-data/tree/master/public/data
  * Our World In Data Covid-19 Tracking Page: \
    https://ourworldindata.org/coronavirus
  * Our World In Data Covid-19 Testing Sources: \
    https://ourworldindata.org/covid-testing#source-information-country-by-country

## Documentation

Here are some additional resources:

* [Flex.io Covid-19 Function Documentation.](https://www.flex.io/integrations/covid-19/functions-and-syntax/) Here, you'll find a list of the functions available, their syntax and parameters, as well as examples for how to use them.
* [Flex.io Covid-19 Integration and Templates.](https://www.flex.io/integrations/covid-19/) Here, you'll find more information about the Flex.io Covid-19 integration as well as templates you can use to start using the integration easily.
* [Flex.io Add-ons.](https://www.flex.io/add-ons) Here, you'll find more information about the Flex.io Add-ons for Microsoft Excel and Google Sheets, including how to install them and use them.
* [Flex.io Integrations.](https://www.flex.io/integrations) Here, you'll find out more information about other spreadsheet function packs available.

## Help

If you have question or would like more information, please feel free to live chat with us at our [website](https://www.flex.io) or [contact us](https://www.flex.io/about#contact-us) via email.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
