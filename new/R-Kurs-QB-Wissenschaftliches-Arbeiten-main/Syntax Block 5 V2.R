##################################################################
#Survivalmodelle
##################################################################

rm(list = ls())

# URL to the raw .RData file (important: must be the raw file link!)
url <- "https://raw.githubusercontent.com/BirteHoltfreter/R-Kurs-QB-Wissenschaftliches-Arbeiten/refs/heads/main/Daten_Blockseminar2.rdata"
# Temporary file location
destfile <- tempfile(fileext = ".RData")
# Download the file
download.file(url, destfile, mode = "wb")
# Load the .RData into the R environment
load(destfile)
# List the objects that were loaded
ls()

#load("Daten_Blockseminar2.RData")

MyData<-dat

library(rms)

##### Datenaufbereitung Teil 1 #####

print(MyData)
describe(MyData) 

describe(MyData$Geschlecht) 
MyData$Sex<-factor(MyData$Geschlecht, levels = c(0,1), labels=c("female","male")) 
label(MyData$Sex)<-"Sex"
describe(MyData$Sex)

##### Datenaufbereitung Teil 2: Welche Alterskategorien sind für die Beschreibung der Daten sinnvoll? #####
# Prinzipien: 
# 1. Auf Originaldaten zugreifen. 
# 2. Höchste Genauigkeit walten lassen. 1 year = 365.242198781 days! 
# https://stackoverflow.com/questions/63523659/convert-days-to-years-in-r 
# https://www.reddit.com/r/askscience/comments/1z5pu4/why_are_there_are_exactly_36525_days_in_a_year/ 
# 3. Nicht durch Bezeichnungen täuschen lassen!

MyData$AgeDays <-  (MyData$Untersuchungstag - MyData$Geburtstag)
describe(MyData$AgeDays) 
MyData$Age <- as.numeric(MyData$AgeDays)/365.242198781 
describe(MyData$Age) 
label(MyData$Age)<-"Age"
units(MyData$Age)<-"Year"
describe(MyData$Age) 
describe(MyData$Alter_exakt)
describe(MyData$AgeDays) 
describe(MyData$AlterTage)
plot( MyData$Sex, MyData$Age)

# Welche Altersgruppen sind zur Beschreibung (Table 1) geeignet?  

MyData$AgeGroup<-cut(MyData$Alter_exakt, breaks = c(20,30,40,50,60,70,80,90))
table(MyData$AgeGroup)
table( MyData$AgeGroup, MyData$Todesfall )

# Stop; Sind die Kategorien sinnvoll? Nein! Können also überschrieben werden. 

MyData$AgeGroup<-cut(MyData$Alter_exakt, breaks = c(20,30,40,50,60,70,82))
table(MyData$AgeGroup)
table( MyData$AgeGroup, MyData$Todesfall )
with(MyData,by(Age, AgeGroup, describe))

##### Datenaufbereitung Teil 3 #####

describe(MyData$Bildungslevel) 
MyData$Education<-factor(MyData$Bildungslevel, levels = c(0,1,2), labels=c("<10 years","10 years", ">10 years")) 
label(MyData$Education)<-"School education"
describe(MyData$Education)
plot( MyData$Education, MyData$Age)

MyData$Income<-MyData$Einkommen
label(MyData$Einkommen)<-"Household income"
units(MyData$Einkommen) <- "€"
describe(MyData$Income)
plot( MyData$Education, MyData$Income)

describe(MyData$Familienstand) 
MyData$MaritalStatus<-factor(MyData$Familienstand, levels = c(1,2,3,4,5), 
                                   labels=c("married","married but separated ", "single","divorced","widowed")) 
label(MyData$MaritalStatus)<-"Marital status"
describe(MyData$MaritalStatus)
plot( MyData$MaritalStatus, MyData$Age)

describe(MyData$Zusammenleben) 
MyData$Partnership<-factor(MyData$Zusammenleben, levels = c(0,1), labels=c("no","yes")) 
label(MyData$Partnership)<-"Living with a partner"
describe(MyData$Partnership)
plot( MyData$Partnership, MyData$Age)

describe(MyData$Rauchen) 
MyData$Smoke3<-factor(MyData$Rauchen, levels = c(0,1,2), labels=c("never smoker","ex-smoker", "current smoker")) 
label(MyData$Smoke3)<-"Smoking status"
describe(MyData$Smoke3)
plot( MyData$Smoke3, MyData$Age)

describe(MyData$Alkohol)
MyData$Alcohol<-factor(MyData$Alkohol, levels = c(0,1), labels=c("no","yes")) 
label(MyData$Alcohol)<-"Risky alcohol consumption"
describe(MyData$Alcohol)
plot( MyData$Alcohol, MyData$Sex)
plot( MyData$Sex, MyData$Alcohol)

describe(MyData$Sport)
MyData$PhysicalActivity<-factor(MyData$Sport, levels = c(0,1), labels=c("no","yes")) 
label(MyData$PhysicalActivity)<-"Physical activity"
describe(MyData$PhysicalActivity)
plot( MyData$PhysicalActivity, MyData$Sex)
plot( MyData$Sex, MyData$PhysicalActivity)

describe(MyData$BMI_exakt)
MyData$BMI<-MyData$BMI_exakt
label(MyData$BMI) <- "Body Mass Index"
units(MyData$BMI) <- "kg/m²"
describe(MyData$BMI)
plot( MyData$Sex, MyData$BMI)

describe(MyData$Groesse)
MyData$Height<-MyData$Groesse
label(MyData$Height) <- "Body height"
units(MyData$Height) <- "cm"
describe(MyData$Height)
plot( MyData$Sex, MyData$Height)

describe(MyData$Gewicht)
MyData$Weight<-MyData$Gewicht
label(MyData$Weight) <- "Body weight"
units(MyData$Weight) <- "kg"
describe(MyData$Weight)
plot( MyData$Sex, MyData$Weight)

describe(MyData$Taille)
MyData$WaistCircumference<-MyData$Taille
label(MyData$WaistCircumference) <- "Waist circumference"
units(MyData$WaistCircumference) <- "cm"
describe(MyData$WaistCircumference)
plot( MyData$Sex, MyData$WaistCircumference)

describe(MyData$Huefte)
MyData$HipCircumference<-MyData$Huefte
label(MyData$HipCircumference) <- "Hip circumference"
units(MyData$HipCircumference) <- "cm"
describe(MyData$HipCircumference)
plot( MyData$Sex, MyData$HipCircumference)


describe(MyData$Diabetes) 
MyData$DiabetesM<-factor(MyData$Diabetes, levels = c(0,1), labels=c("no","yes")) 
label(MyData$DiabetesM)<-"Diabetes mellitus"
describe(MyData$DiabetesM)
plot( MyData$DiabetesM, MyData$Age)

describe(MyData$HbA1c) 
label(MyData$HbA1c)<-"HbA1c"
units(MyData$HbA1c)<-"%"
describe(MyData$HbA1c) 
plot( MyData$DiabetesM, MyData$HbA1c)

describe(MyData$Krebserkrankung) 
MyData$Cancer<-factor(MyData$Krebserkrankung, levels = c(0,1), labels=c("no","yes")) 
label(MyData$Cancer)<-"Cancer"
describe(MyData$Cancer)
plot( MyData$Cancer, MyData$Age)

describe(MyData$Harnwegserkrankung) 
MyData$UTD<-factor(MyData$Harnwegserkrankung, levels = c(0,1), labels=c("no","yes")) 
label(MyData$UTD)<-"Urinary tract disease"
describe(MyData$UTD)
plot( MyData$UTD, MyData$Age)
plot( MyData$UTD, MyData$Sex)
plot( MyData$Sex, MyData$UTD)


##### Datenaufbereitung Teil 4: Endpunkt #####

describe(MyData$Todesfall)
typeof(MyData$Todesfall)

MyData$Death<-MyData$Todesfall 
label(MyData$Death)<-"Death"
describe(MyData$Death)
table(MyData$Death)

plot(MyData$Death, MyData$Age)
plot(as.factor(MyData$Death), MyData$Age)

getOption("max.print")
options(max.print=150)
print(MyData[, c("Geburtstag","Untersuchungstag","AgeDays","Age","Zeit_bis_Zensur", "Death")])

plot(as.factor(MyData$Death),MyData$Zeit_bis_Zensur/365.25)
# plot(MyData$Death,MyData$Zeit_bis_Zensur/365.25)
with(MyData,by(Zeit_bis_Zensur/365.25,Death,describe))

##### Data dist #####

dd<-datadist(MyData)
options(datadist="dd")
dd

##### Survival: Intro #####

S<-Surv(MyData$Zeit_bis_Zensur/365.25,MyData$Death)
S
describe(S)
n0<-npsurv(S~1)
n0
survplot(n0,conf="bands", n.risk=TRUE, xlab=expression(Years) )
options(max.print=2000)
summary(n0)

c1<-npsurv(S~Cancer, MyData)
c1
survplot(c1,conf="bands", n.risk=TRUE, xlab=expression(Jahre))
summary(c1)
summary(c1, seq(0,18,by=2))

MyData$Jahre_bis_Zensur <- MyData$Zeit_bis_Zensur/365.25
sortMyData<-MyData[order(MyData$Cancer, MyData$Jahre_bis_Zensur, MyData$Death),]
sortMyData[sortMyData$Cancer=="yes", c("Death","Cancer","Jahre_bis_Zensur")]

# https://stats.stackexchange.com/questions/361354/choosing-conf-type-for-survfit-in-r 

n1<-npsurv(S~DiabetesM, MyData)
n1
summary(n1)
survplot(n1,conf="bands", n.risk=TRUE, aehaz=TRUE,xlab=expression(Years) )

survplot(psm(S~DiabetesM, data=MyData, dist ="exponential"), add=TRUE, col="red" )

survplot(psm(S~DiabetesM, data=MyData, dist ="logistic"), add=TRUE, col="orange", lwd=3 )

0.0413/0.013
d1 <- cph (S ~ DiabetesM , data=MyData, method="efron", surv =TRUE , x=TRUE , y=TRUE)
summary(d1)
library(EValue)
evalues.HR(est= 3.308, lo=2.4626, hi=4.4436 , rare=0)

co <- c("blue", "red")
survplot (n1, lty=c(1, 1), lwd=c(3, 3), col =co ,
          label.curves=FALSE , conf= "none" )
legend (c(2, 8.5), c(.28 , .34), cex=.8 ,
        c( "Diabetes mellitus = no" , "Diabetes mellitus = yes" ), lwd=c(3,3), col =co, bty = ' n ' )
legend (c(2, 8.5), c(.48 , .54),
        c( "Kaplan-Meier Method (or Observed)" , "Cox Model" ),
        lty=c(1, 3),lwd=c(3,3), cex=.8, bty= ' n ' )

survplot (d1, lty=c(3, 3), lwd=c(3, 3), col =co , # Efron approx.
          add =TRUE , label.curves=FALSE , conf.type = "none")

survplot(psm(S~DiabetesM, data=MyData, dist ="logistic"), add=TRUE, col="orange", lwd=3 )

survplot (d1, lty=c(3, 3), lwd=c(3, 3), col =co , # Efron approx.
                      label.curves=FALSE , conf.type = "none")

s1n<-npsurv(S~Sex, MyData)
s1p <- cph (S ~ Sex , data=MyData, method="efron", surv =TRUE , x=TRUE , y=TRUE)

survplot (s1p, lty=c(3, 3), lwd=c(3, 3), col =co , # Efron approx.
                  label.curves=FALSE , conf.type = "none",  grid=TRUE, time.inc =1)
legend (c(2, 8.5), c(.28 , .34), cex=.8 ,
        c( "Female" , "Male" ), lwd=c(3,3), col =co, bty = ' n ' )
legend (c(2, 8.5), c(.48 , .54),
        c( "Kaplan-Meier Method (or Observed)" , "Cox Model" ),
        lty=c(1, 3),lwd=c(3,3), cex=.8, bty= ' n ' )

survplot (s1n, lty=c(1, 1), lwd=c(3, 3), col =co ,
          add =TRUE , label.curves=FALSE , conf= "none" )

survplot (s1n, lty=c(1, 1), lwd=c(3, 3), col =co ,
          add =TRUE , label.curves=FALSE , conf= "none",n.risk=TRUE,cex.n.risk=1, time.inc =1 , grid=TRUE)

##### Cox models ##### 

h <- cph (S ~ DiabetesM + Sex + Age , data=MyData,method="efron", surv =TRUE , x=TRUE , y=TRUE)
k <- cph (S ~ DiabetesM + Sex + rcs(Age,5) , data=MyData,method="efron", surv =TRUE , x=TRUE , y=TRUE)
l <- cph (S ~ DiabetesM + Sex + AgeGroup , data=MyData,method="efron", surv =TRUE , x=TRUE , y=TRUE)
m <- cph (S ~ DiabetesM + Sex + rcs(Age,5)+rcs(BMI,3) , data=MyData,method="efron", surv =TRUE , x=TRUE , y=TRUE)
specs(m)
m
anova(m)
plot(anova(m))

P<-Predict(m)
plot(P)

# dd$limits$Age
P<-Predict(k, Age, ref.zero=TRUE, fun=exp)
ggplot(P, ylim=c(0,35))

P<-Predict(h, Age, ref.zero=TRUE, fun=exp)
ggplot(P, ylim=c(0,35))

# https://stats.stackexchange.com/questions/297740/what-is-the-difference-between-the-different-types-of-residuals-in-survival-anal
# https://stats.stackexchange.com/questions/161069/difference-between-loess-and-lowess 
# iter.max=0 : null model, see book why

##### Modelldiagnostik 1 mit Lupenbrille (first choice): Martingale residual #####

h0 <- cph (S ~ DiabetesM + Sex + Age , 
           data=MyData,method="efron", surv =TRUE , x=TRUE , y=TRUE, iter.max=0)
h0
res <- resid(h0)
hloess <- loess(res ~ Age, data=MyData)
hloessp<-predict(hloess, se=TRUE)
h1 <- ols (res ~ Age, MyData)
h3 <- ols (res ~ rcs(Age ,3), MyData)
h4 <- ols (res ~ rcs(Age ,4), MyData)
h5 <- ols (res ~ rcs(Age ,5), MyData)
h6 <- ols (res ~ AgeGroup, MyData)
plot(MyData$Age, res, xlab="Age (Years)", ylab="Martingale Residual", col="gray")

points(MyData$Age[MyData$Death==1], res[MyData$Death==1], xlab="Alter (Jahre)", ylab="Martingale Residual", pch=16)

lines(spline(MyData$Age,hloessp$fit), col="blue", lwd=3)

lines(spline(MyData$Age,hloessp$fit+ qt(0.975,hloessp$df)*hloessp$se), lty=2,col="blue")
lines(spline(MyData$Age,hloessp$fit- qt(0.975,hloessp$df)*hloessp$se), lty=2,col="blue")

lines (lowess (MyData$Age , res , iter=0), lty =1, col="lightblue", lwd=3)

legend (22.5 , 0.30 , c("loess smoother and 95% CI ",
                      "lowess smoother",
                      "ols linear fit",
                      "ols spline fit with 3 knots for age (2 degrees of freedom)",
                      "ols spline fit with 4 knots for age (3 degrees of freedom)",
                      "ols spline fit with 5 knots for age (4 degrees of freedom)",
                      "ols spline fit with age groups       (5 degrees of freedom)"), 
        lty=c(1,1,1,1,1,1,1),lwd=c(3,3,3,3,3,3,3), col=c("blue","lightblue","red", "orange","lightgreen", "darkgreen","black"), 
        bty="n")

lines(spline(MyData$Age,h1$fit), col="red", lwd=3)

lines(spline(MyData$Age,h3$fit), col="orange", lwd=3)

lines(spline(MyData$Age,h4$fit), col="lightgreen", lwd=3)

lines(spline(MyData$Age,h5$fit), col="darkgreen", lwd=3)

lines(spline(MyData$Age,h6$fit), col="black", lwd=3)


##### Modelldiagnostik 1 mit Lupenbrille ohne Lupenbrille (second best choice): Martingale residual ######
res <- resid(h)
hloess <- loess(res ~ Age, data=MyData)
hloessp<-predict(hloess, se=TRUE)
plot(MyData$Age, res, xlab="Alter (Jahre)", ylab="Martingale Residual", col="gray")
points(MyData$Age[MyData$Death==1], res[MyData$Death==1], xlab="Alter (Jahre)", ylab="Martingale Residual", pch=16)

plot(MyData$Age, res, xlab="Alter (Jahre)", ylab="Martingale Residual", ylim=c(-0.5, 0.5), col="gray")
points(MyData$Age[MyData$Death==1], res[MyData$Death==1], xlab="Alter (Jahre)", ylab="Martingale Residual", pch=16)
lines(spline(MyData$Age,hloessp$fit), col="blue", lwd=3)
lines(spline(MyData$Age,hloessp$fit+ qt(0.975,hloessp$df)*hloessp$se), lty=2,col="blue")
lines(spline(MyData$Age,hloessp$fit- qt(0.975,hloessp$df)*hloessp$se), lty=2,col="blue")
lines (lowess (MyData$Age , res , iter=0), lty =1, col="lightblue", lwd=3)
legend (25 , 0.30 , c("loess smoother and 95% CI ",
                      "lowess smoother"),
        lty=c(1,1),lwd=c(3,3), col=c("blue","lightblue"), 
        bty="n")

res <- resid(l)
hloess <- loess(res ~ Age, data=MyData)
hloessp<-predict(hloess, se=TRUE)
plot(MyData$Age, res, xlab="Alter (Jahre)", ylab="Martingale Residual", col="gray")
points(MyData$Age[MyData$Death==1], res[MyData$Death==1], xlab="Alter (Jahre)", ylab="Martingale Residual", pch=16)
plot(MyData$Age, res, xlab="Alter (Jahre)", ylab="Martingale Residual", ylim=c(-0.5, 0.5), col="gray")
points(MyData$Age[MyData$Death==1], res[MyData$Death==1], xlab="Alter (Jahre)", ylab="Martingale Residual", pch=16)
lines(spline(MyData$Age,hloessp$fit), col="blue", lwd=3)
lines(spline(MyData$Age,hloessp$fit+ qt(0.975,hloessp$df)*hloessp$se), lty=2,col="blue")
lines(spline(MyData$Age,hloessp$fit- qt(0.975,hloessp$df)*hloessp$se), lty=2,col="blue")
lines (lowess (MyData$Age , res , iter=0), lty =1, col="lightblue", lwd=3)
legend (25 , 0.30 , c("loess smoother and 95% CI ",
                      "lowess smoother"),
        lty=c(1,1),lwd=c(3,3), col=c("blue","lightblue"), 
        bty="n")

anova(h)
anova(k)

summary(h)
summary(k)

##### Modelldiagnostik 2 mit Lupenbrille: dfbetas residual (instead of score residual) ######

dfbetas<-as.data.frame(resid (h , "dfbetas" ))
describe(dfbetas)

plot(MyData$DiabetesM,dfbetas$V1)

plot(MyData$Sex,dfbetas$V2)

plot(MyData$Age,dfbetas$V3)

points(MyData$Age[MyData$Death==1],dfbetas$V3[MyData$Death==1], pch=16, col="red")


w <- which.influence(h, 0.2)
w

w <- which.influence(k, 0.2)
w

which.influence(l, 0.2)

which.influence(m, 0.2)

nam <- names(w)
for(i in 1: length (nam )) {
  cat("Influential observations for effect of", nam[i],"\n")
  print (MyData[w[[i]],])
}

k.rob<-robcov(k)
k 
k.rob

anova(k)
anova(k.rob)

summary(k)
summary(k.rob)

specs(k)
kreduced<-cph(formula = Surv(Zeit_bis_Zensur/365.25, Death) ~ DiabetesM + Sex + rcs(Age, 5), subset(MyData, Nummer!= 14 ), 
              method = "efron", x = TRUE, y = TRUE, surv = TRUE)
k
kreduced

##### Modelldiagnostik 3 ohne und dann mit Lupenbrille: Schoenfeld residual  #####
##### ohne Lupenbrille #####
library(survival)
phtesth<-cox.zph(h ,terms=TRUE, transform="identity")
plot(phtesth)

plot (phtesth , var= "Sex" , pch=16)
summary(h)
h
h$coefficients

abline(0.4845737,0)

abline(h=h$coefficients[2], col="red")

plot (phtesth , var= "DiabetesM", pch=16 ); abline(h=h$coefficients[1], col="red")

plot (phtesth , var= "Age" , pch=16);abline(h=h$coefficients[3], col="red")
h
describe(phtesth$y)

phtestk<-cox.zph(k ,terms=TRUE, transform="identity")
phtestk
specs(k)
plot (phtestk , var= "rcs(Age, 5)", pch=16 ) ; abline(1,0, col="blue")
k
describe(phtestk$y)

phtestkf<-cox.zph(k ,terms=FALSE, transform="identity")
phtestkf
k
describe(phtestkf$y)
plot (phtestkf , var= "Age'''" , pch=16); abline(h=k$coefficients[6], col="red")

##### mit Lupenbrille #####

phtestkm <-cox.zph( k,terms=TRUE, transform="km")
describe(phtestkm$y)
plot(phtestk, var= "Sex" , pch=16);abline(h=k$coefficients[2], col="red")

plot(phtestkm, var= "Sex" , pch=16);abline(h=k$coefficients[2], col="red")

survplot(n0,  time.inc = 1, grid=TRUE, conf= "none" )
summary(n0)
1-phtestkm$x

phtestkm$x
phtestkm$time

##### graph trumps test #####

phtestkm
cox.zph(k ,terms=TRUE, transform="km")

cox.zph(k ,terms=TRUE, transform="rank")

cox.zph(k ,terms=TRUE, transform="identity")

cox.zph(k ,terms=TRUE, transform="log")

phtesth<-cox.zph(h ,terms=TRUE, transform="log")
plot(phtesth)

##### Session info #####

library(usethis)
sessionInfo()

