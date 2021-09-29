import pandas
import boston.main


# Cargamos los datos en memoria
crimes = pandas.read_csv("crimes_dataset.csv", sep=";")


# A continuación exportamos las gráficas que se usarán en la presentación para el cliente
boston.main.get_graphs(crimes)


# Entrenamos el modelo y calculamos la precisión
model_knn, accuracy, ucr_encoder = boston.main.train_model_knn(crimes)

print("The accuracy is: ", accuracy)

sample = crimes.sample().drop(['INCIDENT_NUMBER', 'OFFENSE_CODE', 'OFFENSE_CODE_GROUP',
       'REPORTING_AREA', 'OCCURRED_ON_DATE', 'DAY_OF_WEEK',
       'Location', "UCR_PART"], axis=1)
print("For: \n", sample, "\nUCR is:\n", ucr_encoder.inverse_transform(model_knn.predict(sample)))