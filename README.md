# HabrCrawler
This repository contains programs that allow to create a collection of documents from Habr website and prepare this collection for further data analysis.


The aim of this project is to create a collection of documents that contains around 100000 papers from Habr website. 
This collection is needed in further data analysis.


There are two python scripts.

The first one, which is called create_raw_collection.py allows to create collection of the documents from Habr website. 
The information that is taken from all papers includes Paper's name, Paper's text, Paper's hubs, Paper's tags, Date and Time of the publication, 
Paper's rating, How many times people added this paper in bookmarks, How many comments are left under the paper, Author's karma, Author's rating.
There are two functions in this file: habr_url_puller where you have to specify the first paper number and how many iterations the function has to pass to 
create the collection and get_data_from_articles where you have to specify the URL which is automatically made in habr_url_puller. Finally, the file called
"data_collection" is created.

The second file which is called prepare_ready_collection.py allows to open raw collection, take only existing lists, then create a list which contains lists of papers 
where there are lists with all the info which was taken from the papers in create_raw_collection.py. The final collection contains only papers which text is longer
then 2000 characters, moreover, all lists with info are cleaned from unprinted symbols, extra spaces, line breaks and other extra symbols. Finally, there is an output
of the file which is called "cleaned_collection" which is a csv file that is made by converting list of papers into DataFrame object using pandas library.



All the requirements are written in Requirements.txt file.
