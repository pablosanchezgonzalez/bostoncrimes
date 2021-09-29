import pandas
import sklearn.model_selection
import sklearn.metrics
import sklearn.neighbors
import sklearn.preprocessing
import typing
import pickle

import matplotlib
import seaborn

#TODO: Comentarios y tests

def get_graphs(crimes: pandas.DataFrame) -> None:
    """
    Esta función sirve para obtener imagenes respresentativas del conjunto de datos con el fin de
    emplearlas en la presentación.
    """
    #Intentar evitar lambdas
    crimes["LATITUDE"] = crimes.apply(lambda row: float(row.Location[1:-1].split(",")[0]), axis=1)
    crimes["LONGITUDE"] = crimes.apply(lambda row: float(row.Location[1:-1].split(",")[1]), axis=1)
    crimes.drop(crimes[crimes.LATITUDE < 5].index, inplace=True)

    seaborn.displot(crimes['MONTH'])
    matplotlib.pyplot.ylabel('Frequency')
    matplotlib.pyplot.title('Distribution')
    matplotlib.pyplot.xticks(list(range(1,13,1)))
    matplotlib.pyplot.savefig("month_distribution.png")

    crimes['DAY_OF_WEEK'].value_counts().plot(kind='bar')
    matplotlib.pyplot.ylabel('Frequency')
    matplotlib.pyplot.title('Distribution')
    matplotlib.pyplot.savefig("weekday_distribution.png")

    seaborn.histplot(crimes['HOUR'])
    matplotlib.pyplot.ylabel('Frequency')
    matplotlib.pyplot.title('Distribution')
    matplotlib.pyplot.savefig("hour_distribution.png")

    seaborn.scatterplot(x='LATITUDE',
                        y='LONGITUDE',
                        hue="UCR_PART",
                        data=crimes)
    matplotlib.pyplot.savefig("ucr_by_location.png")

    seaborn.scatterplot(x='LATITUDE',
                        y='LONGITUDE',
                        hue="HOUR",
                        data=crimes)
    matplotlib.pyplot.savefig("hour_by_location.png")



def train_model_knn(crimes: pandas.DataFrame) -> typing.Tuple[sklearn.neighbors.KNeighborsClassifier, float, sklearn.preprocessing.LabelEncoder]:
    """
    Esta función entrena un modelo de k vecinos más cercanos dado el dataframe de crimenes de Boston
    asumiendo que la variable objetivo es 'UCR_PART'
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

    outfile = open("knn.pkl",'wb')
    pickle.dump(neigh,outfile)
    outfile.close()

    ucr_pred = neigh.predict(features_test)

    return(neigh, sklearn.metrics.accuracy_score(ucr_test, ucr_pred), ucr_encoder)
