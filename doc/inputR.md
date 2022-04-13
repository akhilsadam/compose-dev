
The first few lines of each input file are shown below:  

```{r,echo=FALSE}
url <- 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml'
res <- GET(url)
di <- xmlToDataFrame(content(res, "text", encoding = "UTF-8"))
head(di)
```

-----  

```{r,echo=FALSE}
url <- 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml'
res <- GET(url)
di <- xmlToDataFrame(content(res, "text", encoding = "UTF-8"))
head(di)
```