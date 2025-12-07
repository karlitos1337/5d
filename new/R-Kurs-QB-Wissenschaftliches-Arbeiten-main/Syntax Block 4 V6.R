################################################################################
# Vorbereitungen
################################################################################

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

# Pakete laden (falls noch nicht installiert, vorher mit install.packages() installieren)
# Pakete enthalten Funktionen und Tools, die von der R Commuity entwickelt wurden.
# Sie verbessern in der Regel bereits bestehende Basisfunktionalitäten in R oder ergänzen neue Funktionalitäten.
# 1. Installieren der Packages; 2. Aufrufen/Laden der Packages

#install.packages(
#  c("ggplot2",
#    "dplyr",
#    "Rtools",
#    "Rtools45",
#    "summarytools",
#    "corrplot",
#    "naniar",
#    "car",
#    "ggfortify",
#    "performance",
#    "effects",
#    "ResourceSelection",
#    "pROC"
#  ), dependencies = TRUE)
#install.packages("C:/Users/holtfreterb/Downloads/broom_1.0.9.tar.gz", repos = NULL, type = "source")

library(ggplot2)   # Für Grafiken
library(dplyr)     # Für Datenmanipulation
library(summarytools) # Für erweiterte Zusammenfassungen
library(Hmisc)
library(corrplot)
library(car)
library(performance) # Modelldiagnostik
library(ggfortify) # Modelldiagnostik
library(effects) # Modelleffekte
library(broom)
library(rms) # Modelle und Plots
library(pROC)
library(ggeffects)
library(ResourceSelection)

################################################################################
# Datensatz laden und sichten; Variablen definieren
################################################################################

# Beispiel-Datensatz laden (Falls eigener Datensatz: dat <- read.csv("datei.csv"))
#load("Daten_Blockseminar2.RData")
dat

# kategorielle VAriablen definieren
dat$Bildungslevel<-factor(dat$Bildungslevel,levels=c(0,1,2),labels=c("0: <10","1: 10","2: >10"))
dat$Rauchen<-factor(dat$Rauchen,levels=c(0,1,2),labels=c("0: never","1: former","2: current"))
dat$Diabetes<-factor(dat$Diabetes,levels=c(0,1),labels=c("0: no","1: yes"))
dat$Geschlecht<-factor(dat$Geschlecht,levels=c(0,1),labels=c("0: female","1: male"))

# Erstellt Summaries für Variablen; Vorbereitung für rms-Package
dd <- datadist(dat)
options(datadist="dd")

# Überblick über die Datenstruktur
glimpse(dat)

# Erste Zeilen und Dimensionen prüfen
dim(dat)        # Anzahl Zeilen und Spalten
names(dat)      # Spaltennamen
summary(dat)    # Verteilungsmaße als Übersicht (Min, Max, Median, Mean, etc.)


#### 1. Korrelationen berechnen und visualisieren

cor(dat$Alter_exakt, dat$hdl)

#Korrelationsmatrix und Visualisierung
cor(dat[,c("Alter_exakt","Zahnzahl_max28","BMI_exakt","hdl","crp","mean_ST")],use = "complete.obs", method = "spearman")
cor_matrix <- cor(dat[,c("Alter_exakt","Zahnzahl_max28","BMI_exakt","hdl","ldl","crp","mean_ST")],use = "complete.obs", method = "spearman")
cor_matrix

#r und p values extrahieren
result <- rcorr(as.matrix(dat[,c("Alter_exakt","Zahnzahl_max28","BMI_exakt","hdl","ldl","crp","mean_ST")], method="spearman"))
corrplot(cor_matrix, method = "circle", type = "lower", tl.col = "black")

#### 2. Einen ersten Einblick erhalten: Streudiagramme

par(las=1,mai=c(1,1,1,1))
plot(Zahnzahl_max28 ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab="Zahnzahl (max. 28)",pch=20,col="steelblue")

# Lowess - Plot erstellen
ggplot(dat, aes(x = Alter_exakt, y = Zahnzahl_max28)) +
  geom_point() +
  geom_smooth(method = "loess", se = TRUE, color = "blue") +
  labs(title = "LOESS-Plot", x = "Alter, Jahre", y = "Zahnzahl (max. 28)") +
  theme_minimal()


#### 3. Lineares Regressionsmodell aufstellen und Ausgabe erstellen

# Modell aufstellen
M1 <- glm(Zahnzahl_max28 ~ Alter_exakt + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat)

# Modellzusammenfassung anzeigen
summary(M1)

# Konfidenzintervalle anzeigen
confint(M1)

# Ausgabe der Effektschätzer, Konfidenzintervalle, p values, etc
tidy(M1, conf.int = TRUE)

#### 4. Check für nicht-lineare Zusammenhänge; globale Tests auf Nichtlinearität etc.; nur mit Funktionen aus dem rms-Package
# Verwendung von restricted cubic splines zu Modellierung nicht-linearer Zusammenhänge

M1 <- Glm(Zahnzahl_max28 ~ rcs(Alter_exakt,3) + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat, family = gaussian)
anova(M1) 

#### 5. Modellgüte und Modellfit (R2, p-Werte, AIC und BIC)
M1 <- lm(Zahnzahl_max28 ~ rcs(Alter_exakt,3) + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat)
summary(M1)$r.squared    
AIC(M1) #Bestraft die Anzahl der Parameter linear (mit Faktor 2)
BIC(M1) #Bestraft Komplexität stärker als AIC (durch ln(n))

#### 6. Modelldiagnostik

M1 <- glm(Zahnzahl_max28 ~ Alter_exakt + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat)

# Standard-Diagnostikplots:

# Sind die Beobachtungen korrekt?
# high leverage - extreme Werte in den Prädiktoren
# große Residuen - Modellanpassung an die Daten ist schlecht
# hohe Cook's Distance - Beobachtung beeinflusst die geschätzten Regressionskoeffizienten stark

plot(M1)

# mit autoplot() aus dem Package "ggfortify":

#Residuals vs Fitted -> Homoskedastizität
#Normal Q-Q -> Normalverteilung der Residuen
#Scale-Location Plot (Residuals vs Fitted mit sqrt(|residuals|)) -> prüft Homoskedastizität
#Residuals vs Leverage 

autoplot(M1)


#which = 1 → Residuen vs Fitted
#which = 2 → Normal Q-Q Plot
#which = 3 → Scale-Location (Varianzhomogenität)
#which = 4 → Cook’s Distance
#which = 5 → Residuen vs Leverage
#which = 6 → Cook’s Distance vs Leverage

autoplot(M1, which = 4)

# Test auf Normalverteilung der Residuen
shapiro.test(residuals(M1))

# Einflussreiche Beobachtungen identifizieren
influencePlot(M1)

# Erweiterte Diagnostikpakete
check_model(M1)

# Ein fast perfektes Modell
M2 <- glm(ldl ~ Alter_exakt + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat)
check_model(M2)

#### 7. Multikollinaritäten prüfen 
#(VIF = Variance Inflation Factor); Werte > 5 oder 10 deuten auf starke Multikollinearität hin.
vif(M1)

#### 8. Marginale Effekte bestimmen und visualisieren

M1 <- glm(Zahnzahl_max28 ~ rcs(Alter_exakt,3) + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat, family = gaussian)
marginaleffects::avg_comparisons(M1)

# Effekte visualisieren, z.B. für Alter
M1 <- Glm(Zahnzahl_max28 ~ rcs(Alter_exakt,3) + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat, family = gaussian)
p <- rms::Predict(M1, Alter_exakt)
plot(p, confint=TRUE)
plot(rms::Predict(M1, Alter_exakt, Geschlecht), 
     xlab = "Alter", 
     ylab = "Vorhergesagte Zahnzahl", 
     main = "Zahnzahl Vorhersage in Abhängigkeit vom Alter",
     conf.int = TRUE)

# Alle marginalen Effekte darstellen
M1 <- glm(Zahnzahl_max28 ~ rcs(Alter_exakt,3) + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat, family = gaussian)
plot(effects::allEffects(M1))

# Alternative Darstellung der Vorhersagen
M1 <- Glm(Zahnzahl_max28 ~ rcs(Alter_exakt,3) + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat, family = gaussian)

# Vorhersagen in neuem Datensatz speichern
pred_df <- as.data.frame(rms::Predict(M1, Alter_exakt))
head(pred_df)

# Plotten der Vorhersagewerte mit dem 95% KI (geom_ribbons = "flächige Bänder")
ggplot(pred_df, aes(x = Alter_exakt, y = yhat)) +
  geom_line(color = "steelblue") +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.2) +
  labs(x = "Alter", y = "Vorhergesagte Zahnzahl", 
       title = "Zahnzahl-Vorhersage in Abhängigkeit vom Alter") +
  theme_minimal()

#### 9. Interaktionseffekte // Effektmodifikation prüfen

# Modelle mit Interaktionen aufstellen
M1 <- glm(Zahnzahl_max28 ~ Alter_exakt + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat)
summary(M1)
M1_inter <- glm(Zahnzahl_max28 ~ Alter_exakt * Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data=dat)
summary(M1_inter)

# Modellvergleich
anova(M1, M1_inter, test = "Chisq")

# Visualisierung von Interaktionen (package effects)
plot(allEffects(M1_inter))

# Visualisierung von Interaktionen (package ggeffects)
pred <- ggpredict(M1_inter, terms = c("Alter_exakt", "Geschlecht"))
plot(pred)
plot(pred) + labs(
  x = "Alter in Jahren",
  y = "Vorhergesagte Zahnzahl",
  title = "Interaktion von Alter und Geschlecht"
)

# Inhalte von pred
pred$group
pred$x
pred$predicted
pred$conf.low
pred$conf.high

ggplot(pred, aes(x = x, y = predicted, color = group, fill = group)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = 0.2) +
  labs(
    x = "Alter in Jahren",
    y = "Vorhergesagte Zahnzahl",
    title = "Interaktion von Alter und Geschlecht"
  ) 

#Aufgabe 1: Untersuchen Sie den Zusammenhang zwischen dem Diabetesstatus und den 
#Erythrozyten-Leveln unter Adustierung für Alter, Geschlecht, Rauchen, Bildung und Zusammenleben.
#Führen Sie eine Modelldiagnostik durch.

#Aufgabe 2: Visualisieren Sie die durch das Modell vorhergesagten Werte in Abhängigkeit von der Exposition.


################################################################################
################################################################################
# Logistisches Regressionsmodell aufstellen und Ausgabe erstellen
################################################################################
################################################################################

rm(list = ls())
# Return working directory

#Datensatz laden

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
dat

# kategorielle VAriablen definieren
dat$Bildungslevel<-factor(dat$Bildungslevel,levels=c(0,1,2),labels=c("0: <10","1: 10","2: >10"))
dat$Rauchen<-factor(dat$Rauchen,levels=c(0,1,2),labels=c("0: never","1: former","2: current"))
dat$Diabetes<-factor(dat$Diabetes,levels=c(0,1),labels=c("0: no","1: yes"))
dat$Geschlecht<-factor(dat$Geschlecht,levels=c(0,1),labels=c("0: female","1: male"))

#Definition Zahnlosigkeit
dat$edentulous = ifelse(dat$Zahnzahl_max28 ==0 , 1, 0)
table(dat$edentulous)

#### 1. Modell definieren und Summaries erstellen
M2 <- glm(edentulous ~ rcs(Alter_exakt,3)+ Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data = dat, family = binomial)

dd <- datadist(dat)
options(datadist="dd")
M3 <- lrm(edentulous ~ rcs(Alter_exakt,3)+ Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data = dat, x=TRUE, y=TRUE)

M2
M3

summary(M2)
confint(M2) #exakt; empfohlen bei glm
confint.default(M2)  # nutzt Standardfehler (Wald-Konfidenzintervall)

# Odds Ratios
exp(coef(M2))
exp(confint(M2))

# mit tidy
broom::tidy(M2, conf.int = TRUE, exponentiate = TRUE)

#### 2. Modellgüte - Likelihood-Ratio-Test und Pseudo-R²
M3$stats["Model L.R."]
M3$stats["R2"]

#### 3. Diagnostik - einflussreiche Beobachtungen; Residuenstruktur prüfen

# Standardisierte Residuen: Differenz zwischen beobachteten und dem durch das Modell vorhergesagten Wert
plot(rstandard(M2, type = "pearson"), main = "Standardisierte Residuen", ylab = "rstandard")

# Deviance Residuen: Differenz zwischen beobachteten und dem durch das Modell vorhergesagten Wert auf Basis der Devianz; 
#Prüfung der Modellgüte; Identifikation schlecht passender Beobachtungen
plot(residuals(M2, type = "deviance"), main = "Deviance Residuen", ylab = "Residuals")

# Cook's Distance: beeinflusst eine einzelne Beobachtung das Modell?
plot(cooks.distance(M2), type = "h", main = "Cook's Distance")

# Leverage: beeinflussen bestimmte Beobachtungen mit ungewöhnlichen Wertekombinationen die Modellanpassung?
plot(hatvalues(M2), type = "h", main = "Leverage (hat values)")

#alle Diagnostikplots zusammen
check_model(M2)
autoplot(M2)
influence(M2)

#### 4. Linearity Check für kontinuierliche Variablen
# y-Achse: teilweise Residuen (Effekt auf den Logit)
# rosa Linie (zeigt geschätzten Zusammenhang) sollte ungefähr gerade sein - dann ist die Linearitätsannahme erfüllt
# starke Krümmung: nicht-lineare Formen prüfen

M2 <- glm(edentulous ~ Alter_exakt + Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data = dat, family=binomial)
car::crPlot(M2, "Alter_exakt", main="CR-Plot für Alter")  # predicted = Logit-Wahrscheinlichkeit

par(mfrow=c(1,2))
for(v in c("Alter_exakt","HbA1c")){
  crPlot(M2, v, main=paste("CR-Plot für", v))
}

#### 5. Kalibrierung

#Hosmer-Lemeshow-Test: prüft Vergleichbarkeit der beobachteten und vorhergesagten Wahrscheinlichkeiten
ResourceSelection::hoslem.test(dat$edentulous, fitted(M2))

#Calibration plot mit 200 boot straps; wie gut stimmen die Vorhersagen des Modells mit den tatsächlichen Werten überein?
plot(calibrate(M3, B=200))

#### 6. Diskriminationsfähigkeit: ROC Kurve und AUC
M3$stats["Dxy"]/2 + 0.5  # AUC value

pred <- predict(M2, type = "response")
roc_curve <- roc(dat$edentulous, pred)
plot(roc_curve, main = "ROC-Kurve")
auc(roc_curve)

#### 7. Multikollinearität prüfen
vif(M3) 

M4 <- lrm(edentulous ~ Alter_exakt+ Geschlecht + Bildungslevel + Rauchen + Diabetes + HbA1c, data = dat, x=TRUE, y=TRUE)
vif(M4) 

#### 8. Visualisierung des Modells

p <- Predict(M3, Alter_exakt, fun = plogis)  # plogis transformiert Logits in eine Wahrscheinlichkeit

plot(p,
     conf.int = TRUE,  # Konfidenzintervall
     xlab = "Alter (exakt, in Jahren)",
     ylab = "Wahrscheinlichkeit für Edentulous",
     main = "Vorhergesagte Wahrscheinlichkeit")

# weitere Variablen im Plot ergänzen
p2 <- Predict(M3, Alter_exakt, Geschlecht, fun = plogis)

plot(p2,
     conf.int = TRUE,
     xlab = "Alter (exakt, in Jahren)",
     ylab = "Wahrscheinlichkeit für Edentulous",
     main = "Vorhersage nach Geschlecht")

# Werte plotten, wenn Geschlecht=female
p3 <- Predict(M3, Alter_exakt, Geschlecht='0: female', fun = plogis)

plot(p3,
     conf.int = TRUE,
     xlab = "Alter (exakt, in Jahren)",
     ylab = "Wahrscheinlichkeit für Edentulous",
     main = "Vorhersage Females")


#Aufgabe 3: Untersuchen Sie den Zusammenhang zwischen der Bildung und dem Vorliegen einer Dyslipidaemie 
#unter Adustierung für das Alter und Geschlecht. Führen Sie eine Modelldiagnostik durch.

#Aufgabe 4: Visualisieren Sie die durch das Modell vorhergesagten Wahrscheinlichkeiten einer Dyslipidaemie in Abhängigkeit von der Bildung.

