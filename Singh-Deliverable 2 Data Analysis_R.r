# Set the working directory
setwd('C:/Users/Asmita Singh/Documents/GMU/AIT 580/Project Dataset')

# Read the file
storm.df <- read.csv(file='1950-2018_all_tornadoes.csv')

# Store numeric variables 
stormdf.numeric <- unlist(lapply(storm.df, is.numeric))  

# store the needed libraries
library(ggplot2)
library(dplyr)
library(corrplot)

# Check if Tornado's loss is related to injuries, fatalities, and area.
# since the losses before 1996 is given as 0 - 9, converting the values into million
# Converting to a loss amount for pre-1996 events
# 1 : <$50
# 2: $50 to $500
# 3: $500 to $5,000
# 4: $5,000 to $50,000
# 5: $50,000 to $500,000
# 6: $500,000 to $5,000,000
# 7: $5,000,000 to $50,000,000
# 8: $50,000,000 to $500,000,000
# 9: $500,000,000

storm.df$LossNew <- 
    case_when(
        storm.df$yr<1996 & storm.df$loss == 0 ~ 10,
        storm.df$yr<1996 & storm.df$loss == 1 ~ 50,
        storm.df$yr<1996 & storm.df$loss == 2 ~ 250,
        storm.df$yr<1996 & storm.df$loss == 3 ~ 2750,
        storm.df$yr<1996 & storm.df$loss == 4 ~ 27500,
        storm.df$yr<1996 & storm.df$loss == 5 ~ 275000,
        storm.df$yr<1996 & storm.df$loss == 6 ~ 2750000,
        storm.df$yr<1996 & storm.df$loss == 7 ~ 27500000,
        storm.df$yr<1996 & storm.df$loss == 8 ~ 275000000,       
        storm.df$yr<1996 & storm.df$loss == 9 ~ 500000000
    )

# Translate losses after 1996 into $Millions
storm.df$LossNew=ifelse(storm.df$y>=1996 & storm.df$y<=2015,storm.df$loss*1000000,storm.df$LossNew)
storm.df$LossNew=ifelse(storm.df$y>=2016,storm.df$loss,storm.df$LossNew)

# TUKEY'S FIVE NUMBER SUMMARY, CORRELATION MATRIX AND CORRELOGRAM

# Since there are 33 columns in the data, we will create a subset of the data, columns included 'inj','fat','mag','LossNew','closs','len','wid')
storm.subset <- storm.df %>%
    select('inj','fat','mag','LossNew','closs','len','wid')

# Compute correlation matrix for injuries, fatalities, magnitude, loss, crop loss, length of the tornado, the width of the tornado
correlation <- round(cor(storm.subset[sapply(storm.subset, is.numeric)],use="complete.obs",method="pearson"),4)
correlation

# Draw a correlogram injuries, fatalities, magnitude, loss, crop loss, length of the tornado, the width of the tornado
corrplot(correlation, type = "full", order = "hclust", 
         tl.col = "black", tl.srt = 45)

# pairwise distribution plot for each interesting pair of columns
pairs(~inj+fat+LossNew+closs+len+wid, data=storm.subset,
      main="Simple Scatterplot Matrix")

# LINEAR REGRESSION
# linear regression of tornado losses

regressor <- lm(formula = LossNew ~ yr + mo + mag + inj + fat + slat + slon + elat + elon + len + wid,
                data = storm.df)
summary(regressor, test = "F")

# Removing unsignificant model parameters and running linear regression
regressor1 <- lm(formula = LossNew ~ yr + inj + fat + wid,
                data = storm.df)
summary(regressor1, test = "F")

# A high value of F statistic, with a very low p-value (<2.2e-16), implies that the null hypothesis can be rejected. This means there is a potential relationship between the predictors and the outcome.

# Predicting loss for new data
yr <- 2008
inj <- 0
fat <- 1
wid <- 100
new.data<-data.frame(yr,mag,inj,fat,wid)
Predicted_Loss=predict(regressor1, newdata = new.data)
format(Predicted_Loss,big.mark=",",scientific=FALSE)
paste("$",format(Predicted_Loss, big.mark=",", digits = 2),sep="")

# HYPOTHESIS TEST:
# Null hypothesis: Tornado loss IS NOT influenced by magnitude of the storm
# Alternative hypothesis: Tornado loss is influenced by magnitude of the storm
# assuming the data does not follow a normal distribution, hence using wilcox test
result <- with(storm.df, wilcox.test(LossNew[mag == 3], LossNew[mag == 4]),simulate.p.value = TRUE)
result
# print only the p-value
result$p.value
# The p-value of the test is 0.00, which is less than the significance level alpha = 0.05. We can reject null hypotesis and conclude that tornado loss is incluenced by the Magnitude of the storm.

# test some relationships
# Create a confusion matrix
table(storm.df$mag,storm.df$fc)
# calculate chi-square
chisq.test(storm.df$mag,storm.df$fc,simulate.p.value = TRUE)
