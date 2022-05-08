# Imports
import requests
from bs4 import BeautifulSoup
import csv
import random
from time import sleep
from requests.adapters import HTTPAdapter, Retry


def get_data_from_articles(article_url):
    # Here are listed proxies for further usage
    proxies_all = [{'http': 'http://47.252.82.135:8080'}, {'http': 'http://203.32.120.205:80'},
                   {'http': 'http://185.171.231.158:80'},
                   {'http': 'http://91.226.97.7:80'}, {'http': 'http://203.22.223.178:80'},
                   {'http': 'http://203.24.109.14:80'},
                   {'http': 'http://203.30.191.76:80'}, {'http': 'http://91.243.35.112:80'},
                   {'http': 'http://185.162.230.205:80'},
                   {'http': 'http://91.226.97.27:80'}, {'http': 'http://45.12.31.208:80'},
                   {'http': 'http://203.28.8.165:80'},
                   {'http': 'http://203.24.102.136:80'}, {'http': 'http://199.60.103.47:80'},
                   {'http': 'http://185.171.231.98:80'},
                   {'http': 'http://172.67.181.118:80'}, {'http': 'http://172.67.181.77:80'},
                   {'http': 'http://172.67.255.224:80'},
                   {'http': 'http://172.67.180.27:80'}, {'http': 'http://172.67.181.8:80'},
                   {'http': 'http://172.67.167.33:80'},
                   {'http': 'http://203.30.189.138:80'}, {'http': 'http://203.30.188.244:80'},
                   {'http': 'http://185.162.229.16:80'}]

    # Session usage allows to save certain parameters across requests.
    # Moreover, this helps you to save cookies if you need them in your project
    source_get = requests.Session()
    source_get.keep_alive = False  # This parameter helps to close excess connections
    retries = Retry(total=1,
                    backoff_factor=0.15,
                    status_forcelist=[500, 502, 503, 504])  # This parameter helps to increase timeout not to get banned
    # Moreover, this parameter allows to retry the connection
    # Until 2 minutes will pass, backoff_factor increases
    # timeout between requests, for example, you start from 0 second
    # second attempt will happen after 15 seconds and etc until 2 min.

    # Here we mount custom adapter with retries to our session
    source_get.mount('http://', HTTPAdapter(max_retries=retries))

    # Here we turn to the URL using a random proxies from the list
    source_get1 = source_get.get(article_url, proxies=random.choice(proxies_all))
    # Here we get a text from our request and turn it into the BeautifulSoup object
    source_get_text = source_get1.text
    soup_obj_get = BeautifulSoup(source_get_text)
    # Here one can specify the filename, recommended mode is 'a' that allows to add information to the existing file
    # This is helpful if you suffer from bad internet connection or electricity interruptions
    file = open("data_collection", "a", encoding="utf-8")


# Here are created several lists to contain all data inside them in future
    existence_list = []
    paper_name_list = []
    text_list = []
    hubs_list = []
    tags_list = []
    date_n_time_list = []
    paper_rating_list = []
    paper_bookmarks_list = []
    number_of_comments_list = []
    paper_author_list = []
    author_karma_list = []
    author_rating_list = []

    # Below are specified the parameters that we get from the article.
    # To my mode of thinking the best parameters for papers' classification are their:
    # 1. Name;
    # 2.Text;
    # 3.Hubs of the article;
    # 4.Tags of the article;
    # 5.Date and time of publication;
    # 6.Rating of the article;
    # 7.How many times users bookmarked this article;
    # 8.How many comments are left under the article;
    # 9.Author's name;
    # 10.Author's karma;
    # 11.Author's rating;
    # These parameters will be useful in the project's further steps

    # Check whether paper exist
    for existence in soup_obj_get.findAll('div', {'class': 'tm-error-message'}):
        existence_list.extend(existence)
    if len(existence_list) == 0:

        # Number of symbols in the paper
        for text_length in soup_obj_get.findAll('article', {'class': 'tm-article-presenter__content'}):
            len_text = len(text_length.text)
#             print("Количество символов в статье: ", len_text)
        if int(len_text) > 0:

            # Paper's name
            for name in soup_obj_get.findAll('h1', {'class': 'tm-article-snippet__title'}):
                paper_name = name.text.replace("|", " ").strip()
#                 print("Название статьи: ", paper_name)
            paper_name_list.append(paper_name)

            if len(paper_name_list) == 0:
                return None

            for paper_text in soup_obj_get.findAll('div', {'id': "post-content-body"}):
                if len(paper_text) != 0:
                    all_text = paper_text.text.replace("|", " ").strip()
                    text_list.append(all_text.strip())

            if len(text_list) == 0:
                return None

            # Paper's hubs
            for hubs in soup_obj_get.findAll('a', {'class': 'tm-hubs-list__link'}):
                if len(hubs) != 0:
                    hubs_list.append(hubs.string.replace("|", " ").strip())
                    # hubs_string = "; ".join(hubs_list)
    #                 print("Хбы статьи: ", hubs_string.strip())
                elif len(hubs) == 0:
                    return None

            # Paper's tags
            for tags in soup_obj_get.findAll('a', {'class': 'tm-tags-list__link'}):
                if len(tags) != 0:
                    tags_list.append(tags.string.replace("|", " ").strip())
                    # tags_string = "; ".join(tags_list)
                elif len(tags) == 0:
                    return None

            # Datetime of publication
            for datetime in soup_obj_get.findAll('span', {'class': 'tm-article-snippet__datetime-published'}):
                if len(datetime) != 0:
                    date_n_time = datetime.string.replace("|", " ").strip()
    #                 print("Дата и время публикации: ", date_n_time)
                if len(date_n_time) != 0:
                    date_n_time_list.append(date_n_time)
                elif len(date_n_time) == 0:
                    return None

            # Paper's rating
            for paper_rating in soup_obj_get.findAll('span', {'class': 'tm-votes-meter__value_rating'}):
                if len(paper_rating) != 0:
                    paper_rat = paper_rating.string.replace("|", " ").strip()
                    paper_rat = paper_rat.replace("Рейтинг", " ").strip()
    #                 print("Рейтинг статьи: ", paper_rat)
                if len(paper_rat) != 0:
                    paper_rating_list.append(paper_rat)
                elif len(paper_rat) == 0:
                    return None

            # Paper's bookmarks
            for bookmarks in soup_obj_get.findAll('span', {'class': 'bookmarks-button__counter'}):
                if len(bookmarks) != 0:
                    paper_bookmarks = bookmarks.string.replace("|", " ").strip()
                    paper_bookmarks = paper_bookmarks.replace("Закладка", " ").strip()
                    paper_bookmarks = paper_bookmarks.replace("Закладки", " ").strip()
    #                 print("Добавлений в закладки: ", paper_bookmarks)
                if len(paper_bookmarks) != 0:
                    paper_bookmarks_list.append(paper_bookmarks)
                elif len(paper_bookmarks) == 0:
                    return None

            # Number of comments
            for comments_num in soup_obj_get.findAll('span', {'class': 'tm-article-comments-counter-link__value'}):
                if len(comments_num) != 0:
                    number_of_comments = comments_num.string.replace("Комментарии", "").strip()
                    number_of_comments = number_of_comments.replace("Комментировать", "").strip()
                    number_of_comments = number_of_comments.replace("|", " ").strip()
#                 print("Количество комментариев: ", number_of_comments)
                    number_of_comments_list.append(number_of_comments)
                elif len(comments_num) == 0:
                    return None

            # Author's name
            for author in soup_obj_get.findAll('a', {'class': 'tm-user-info__username'}):
                if len(author) != 0:
                    paper_author = author.string.replace("|", " ").strip()
#                     print("Автор статьи: ", paper_author)
                    paper_author_list.append(paper_author)
                elif len(author) == 0:
                    return None

            # Author's karma
            for item in soup_obj_get.findAll('div', {'class': 'tm-karma__votes tm-karma__votes_positive'}):
                if len(item) != 0:
                    author_karma = item.string.replace("|", " ").strip()
                    author_karma = author_karma.replace("Карма", " ").strip()
#                     print("Карма пользователя: ", author_karma)
                    author_karma_list.append(author_karma)

            if len(author_karma_list) == 0:
                for karma in soup_obj_get.findAll('div', {'class': 'tm-karma__votes tm-karma__votes_negative'}):
                    if len(karma) != 0:
                        author_karma = karma.string.replace("|", " ").strip()
                        author_karma = author_karma.replace("Карма", " ").strip()
#                         print("Карма пользователя: ", author_karma)
                        author_karma_list.append(author_karma)
            if len(author_karma_list) == 0:
                return None

            # Author's rating
            for author_rating in soup_obj_get.findAll('div', {'class': 'tm-rating__counter'}):
                if len(author_rating) != 0:
                    author_rat = author_rating.string.replace("|", " ").strip()
                    author_rat = author_rat.replace("Рейтинг", " ").strip()
#                     print("Рейтинг пользователя: ", author_rat)
                    author_rating_list.append(author_rat)
                elif len(author_rating) == 0:
                    return None
            # This header allows the sender to
            # hint about how the connection may be used to set a timeout and a maximum amount of requests
            source_get.headers.update({'Connection': 'Keep-Alive'})

            # Now we have to put all the lists in one list to make  an access to each paper data element easier
            # This also helps to simplify the process of writing data to the file
            data_list = [[paper_name_list, text_list, hubs_list, tags_list,
                          date_n_time_list, paper_rating_list, paper_bookmarks_list,
                          number_of_comments_list, paper_author_list, author_karma_list, author_rating_list]]

            # Then the file is written into csv file separated by '|' sign, the text has been already
            # cleaned from this sign. This helps to alleviate further work with the file when the raw collection
            # will be preprocessed/cleaned.
            wr = csv.writer(file, delimiter='|')
            wr.writerows(data_list)
            # You can specify your own timeout - this helps not to get banned in case of excessive requests
            sleep(1)
            file.close()
            return data_list

        elif int(len_text) == 0:
            return None

    elif len(existence_list) != 0:
        #         print("Paper does not exist")
        return None


# First step is habr_url_puller function that scrapes the website, then it takes URL's of the posts
# In this function you have to specify two variables: paper_number and max_papers
# 1. paper_number allows to choose the first post, because in Habr posts are marked one by one
# 2. max_papers allows you to choose the size of your collection, how many papers there will be
#       in your collection. However, you should know that a lot of papers are deleted by now
#       that's why you have to choose a bigger size then you need

def habr_url_puller(paper_number, max_papers):
    # create a variable pages that is going to be iterated through all the pages that got scrapped
    # You can specify the start of the work by setting your own parameter what regulates the colelction size
    number_of_papers = 0

    while number_of_papers <= max_papers:

        # This is basic URL for any post on Habr website
        url = "https://habr.com/ru/post/" + str(paper_number) + "/"

        # The block bellow uses the function that gets all the info from the article
        # and writes it into the file
        # If any exceptions occured then they are output in the console
        # Finally statement allows to get the next post no matter what happen
        # This scheme is obligatory because many posts are deleted nowadays or there is no access to them
        try:
            get_data_from_articles(url)
        except Exception as e:
            print(e)
        #         sleep(1)
        finally:
            paper_number += 1
            number_of_papers += 1


habr_url_puller(150000, 10)
