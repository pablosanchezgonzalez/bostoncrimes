import pandas
import sklearn.model_selection
import sklearn.metrics
import sklearn.neighbors
import sklearn.preprocessing
import typing
import pickle
import os

import matplotlib
import seaborn

#TODO: Comentarios

def create_directory_if_not_exists(path: str) -> None:
    """This function checks if a directory exists ans if not creates it

    Args:
        path (str): route to directory to be created
    """

    try:
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            print(f"Directory {path} already exists.")
    except TypeError:
        print(f"Creation of the directory {path} failed")
    else:
        print(f"Successfully created the directory {path}")

    

def get_graphs(crimes: pandas.DataFrame) -> None:
    """The purpose of this function is to obtain representative images of the dataset to make a presentation.

    Args:
        crimes (pandas.DataFrame): Boston crimes dataset
    """
    #Intentar evitar lambdas
    crimes["LATITUDE"] = crimes.apply(lambda row: float(row.Location[1:-1].split(",")[0]), axis=1)
    crimes["LONGITUDE"] = crimes.apply(lambda row: float(row.Location[1:-1].split(",")[1]), axis=1)
    crimes.drop(crimes[crimes.LATITUDE < 5].index, inplace=True)

    # Se comprueba si existe el directorio dónde se van a almacenar las gráficas; si no existe, se crea.
    create_directory_if_not_exists("./graphs")

    seaborn.displot(crimes['MONTH'])
    matplotlib.pyplot.ylabel('Frequency')
    matplotlib.pyplot.title('Distribution')
    matplotlib.pyplot.xticks(list(range(1,13,1)))
    matplotlib.pyplot.savefig("./graphs/month_distribution.png")

    crimes['DAY_OF_WEEK'].value_counts().plot(kind='bar')
    matplotlib.pyplot.ylabel('Frequency')
    matplotlib.pyplot.title('Distribution')
    matplotlib.pyplot.savefig("./graphs/weekday_distribution.png")

    seaborn.histplot(crimes['HOUR'])
    matplotlib.pyplot.ylabel('Frequency')
    matplotlib.pyplot.title('Distribution')
    matplotlib.pyplot.savefig("./graphs/hour_distribution.png")

    seaborn.scatterplot(x='LATITUDE',
                        y='LONGITUDE',
                        hue="UCR_PART",
                        data=crimes)
    matplotlib.pyplot.savefig("./graphs/ucr_by_location.png")

    seaborn.scatterplot(x='LATITUDE',
                        y='LONGITUDE',
                        hue="HOUR",
                        data=crimes)
    matplotlib.pyplot.savefig("./graphs/hour_by_location.png")



def train_model_knn(crimes: pandas.DataFrame) -> typing.Tuple[sklearn.neighbors.KNeighborsClassifier, float, sklearn.preprocessing.LabelEncoder]:
    """This function trains a knn model to predict 'UCR_PART' given the boston crimes dataset.

    Args:
        crimes (pandas.DataFrame): Boston crimes dataset

    Returns:
        typing.Tuple[sklearn.neighbors.KNeighborsClassifier, float, sklearn.preprocessing.LabelEncoder]: Tuple with the model, its accuracy and the encoder of UCR_PART.
    """

    #Nombres más descriptivos

    features = crimes.drop(['INCIDENT_NUMBER', 'OFFENSE_CODE', 'OFFENSE_CODE_GROUP',
       'REPORTING_AREA', 'OCCURRED_ON_DATE', 'DAY_OF_WEEK',
       'Location', "UCR_PART"], axis=1)

    ucr_encoder = sklearn.preprocessing.LabelEncoder()
    ucr = ucr_encoder.fit_transform(crimes.UCR_PART)

    features_train, features_test, ucr_train, ucr_test = sklearn.model_selection.train_test_split(features, ucr, test_size=0.2)

    neigh = sklearn.neighbors.KNeighborsClassifier(n_neighbors=5)
    neigh.fit(features_train, ucr_train)

    # Se comprueba la existencia del directorio mdo
    create_directory_if_not_exists("./models")

    outfile = open("./models/knn.pkl",'wb')
    pickle.dump(neigh,outfile)
    outfile.close()

    outfile = open("./models/encoder.pkl",'wb')
    pickle.dump(ucr_encoder, outfile)
    outfile.close()


    ucr_pred = neigh.predict(features_test)

    return(neigh, sklearn.metrics.accuracy_score(ucr_test, ucr_pred), ucr_encoder)
