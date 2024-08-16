CREATE DATABASE if not exists iris_db;

USE iris_db;

CREATE TABLE iris_dataset (
    sepal_length FLOAT,
    sepal_width FLOAT,
    petal_length FLOAT,
    petal_width FLOAT,
    species FLOAT
);                                                        

CREATE TABLE predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sepal_length FLOAT,
    sepal_width FLOAT,
    petal_length FLOAT,
    petal_width FLOAT,
    pred_species FLOAT,
    time_pred DOUBLE
);
