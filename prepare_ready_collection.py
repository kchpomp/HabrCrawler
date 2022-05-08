# Reading&Cleaning Part of the program
# Imports
import re
import pandas as pd


# Open the file and read all the lists
my_file = open("data_collection.txt", "r", encoding="utf-8")
content_list = my_file.readlines()
my_file.close()

# Leave only even list elements because odd elements are empty
data = content_list[::2]

# Here list of strings is converted to the list of lists where list element is an article. Moreover, one article
# contains 11 lists where contained all the information about one article
y = []
for j in range(0, len(data)):

    for i in range(0, data[j].count('|')):
        x = data[j].split('|')
    y.append(x)

# Here the text is cleaned from unprintable symbols, line breaks and excessive spaces.
# Moreover, the final collection will contain only papers that have text length more that 2000 symbols and if future int
# columns do not exist
z = []
for j in range(0, len(y)):
    y[j][1] = re.sub(r'[^\w\s]', " ", y[j][1])
    y[j][1] = y[j][1].replace("\r", " ")
    y[j][1] = y[j][1].replace("\n", " ")
    y[j][1] = y[j][1].split()
    y[j][1] = " ".join(y[j][1])
    y[j][6] = y[j][6].replace("Закладка", "")
    y[j][5] = y[j][5].replace("Рейтинг", "")
    y[j][7] = y[j][7].replace("Комментировать", "")
    y[j][7] = y[j][7].replace("Комментарии", "")
    y[j][9] = y[j][9].replace("Карма", "")
    y[j][10] = y[j][10].replace("Рейтинг", "")

    if len(y[j][1]) > 2000:
        z.append(y[j])

# In the final collection all excessive spaces, line breaks, extra square brackets, excessive "'" are deleted
# From all the elements of paper
for j in range(0, len(z)):
    for i in range(0, len(z[j])):
        z[j][i] = z[j][i].replace("'", "")
        z[j][i] = z[j][i].replace("[", "")
        z[j][i] = z[j][i].replace("]", "")
        z[j][i] = z[j][i].replace("\r", " ")
        z[j][i] = z[j][i].replace("\n", " ")
        z[j][i] = z[j][i].replace("+", " ")

    if z[j][5] == "":
        z[j][5] = "0"

    if z[j][6] == "":
        z[j][6] = "0"

    if z[j][7] == "":
        z[j][7] = "0"

    if z[j][9] == "":
        z[j][9] = "0"

    if z[j][10] == "":
        z[j][10] = "0.0"


# In this section is specified the final collection file
file_cleaned = open("cleaned_collection", "a", encoding="utf-8")

# The first elements of the collection is put inside the pandas DataFrame structure
# All column names are specified
df1 = df = pd.DataFrame({'Название статьи': [z[0][0]],
                         'Текст Статьи': [z[0][1]],
                         'Хабы статьи': [z[0][2]],
                         'Тэги статьи': [z[0][3]],
                         'Дата и время публикации': [z[0][4]],
                         'Рейтинг статьи': [z[0][5]],
                         'Добавлено в закладки, раз': [z[0][6]],
                         'Количество комментариев': [z[0][7]],
                         'Автор статьи': [z[0][8]],
                         'Карма автора': [z[0][9]],
                         'Рейтинг автора': [z[0][10]]})
# Here are specified data types for some of the columns
df1 = df1.astype({'Рейтинг статьи': float, 'Добавлено в закладки, раз': float, 'Количество комментариев': float,
                  'Карма автора': float, 'Рейтинг автора': float})

# In this section all the papers that are left in list z are appended to the dataframe
for i in range(1, len(z)):
    df2 = pd.DataFrame({'Название статьи': [z[i][0]],
                        'Текст Статьи': [z[i][1]],
                        'Хабы статьи': [z[i][2]],
                        'Тэги статьи': [z[i][3]],
                        'Дата и время публикации': [z[i][4]],
                        'Рейтинг статьи': [z[i][5]],
                        'Добавлено в закладки, раз': [z[i][6]],
                        'Количество комментариев': [z[i][7]],
                        'Автор статьи': [z[i][8]],
                        'Карма автора': [z[i][9]],
                        'Рейтинг автора': [z[i][10]]})

    df2 = df2.astype({'Рейтинг статьи': float, 'Добавлено в закладки, раз': float, 'Количество комментариев': float,
                      'Карма автора': float, 'Рейтинг автора': float})

    df1 = df1.append(df2, ignore_index=True)

# The final Data Frame is saved to the csv file
df_csv = df1.to_csv(file_cleaned)

file_cleaned.close()