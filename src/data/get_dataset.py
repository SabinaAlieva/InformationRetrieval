import os
from tqdm import tqdm
import parser_api as pb
import pandas as pd

if __name__ == '__main__':
    data = []
    columns = (['FileName', 'Title', 'Link', 'ArticleId', 'Date', 'Views',
                'Author', 'Tags', 'AmountComments', 'Rating', 'Text'])

    directory = r'C:\Users\Public\Projects\python\Pikabu\InformationRetrieval\src\data\data'
    #  directory = r'C:\Users\Public\Projects\python\Pikabu\InformationRetrieval\notebooks\source_hot_html'
    files_list = os.listdir(directory)

    array = []

    for f in tqdm(files_list):
        page = pb.open_html(os.path.join(directory, f))

        array = ([f, pb.title(page), pb.link(page), pb.article_id(page), pb.page_date(page), pb.views(page),
                  pb.author(page), pb.tags(page), pb.amount_comments(page), pb.rating(page), pb.text(page)])

        data.append(dict(zip(columns, array)))
        array = []

    df = pd.DataFrame(data)
    df.to_csv(directory + "pikabu_dataset_new.csv")
