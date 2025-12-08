####################################################################################
#### Vorbereitungen 
####################################################################################

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
# Pakete enthalten Funktionen und Tools, die von der R Community entwickelt wurden.
# Sie verbessern in der Regel bereits bestehende Basisfunktionalitäten in R oder ergänzen neue Funktionalitäten.

# Installieren und Aufrufen/Laden von Paketen
#install.packages(
#  c("ggplot2",
#  "dplyr",
#  "summarytools",
#  "corrplot",
#  "naniar",
#  "cowplot",
#  "gridExtra",
#  "gtsummary"), dependencies=TRUE)

library(ggplot2)   # Für Grafiken
library(dplyr)     # Für Datenmanipulation
library(summarytools) # Für erweiterte Zusammenfassungen
library(corrplot) #Korrelation Plots
library(naniar) #Visualization of missing data
library(mice) #Multiple imputation
library(reshape2) #Umstrukturierung von Daten; wide -> long
library(psych)  # Für detaillierte deskriptive Statistiken
library(Hmisc) # umfangreiches Paket von Frank Harrel
library(cowplot) # Kombinieren von ggplot Grafiken
library(gridExtra) # Kombinieren von ggplot Grafiken
library(gtsummary) # Deskriptive Tabellen erstellen

####################################################################################
# 1. Überblick über die Datenstruktur
####################################################################################

# Beispiel-Datensatz laden (Falls eigener Datensatz: dat <- read.csv("datei.csv"))

load("Daten_Blockseminar2.RData")
dat

# Datentypen und Strukturen

str(dat)        # Datentypen und Struktur
glimpse(dat)    # Alternative zu str(), kompakter

# Erste Zeilen und Dimensionen prüfen

head(dat, 10)   # Erste 10 Zeilen anzeigen
tail(dat, 10)   # Letzte 10 Zeilen anzeigen
dim(dat)        # Anzahl Zeilen und Spalten
names(dat)      # Spaltennamen
summary(dat)    # Verteilungsmaße als Übersicht (Min, Max, Median, Mean, etc.)

####################################################################################
# 2. Daten anzeigen/manipulieren/verändern
####################################################################################

## Zeileneinträge einer Variablen anzeigen
dat$Alter_exakt[1:10]

## Zeige alle Zeilen an, für die Glukose_Urin=positiv ist
dat[dat$Glukose_Urin=="positiv",]

## Spalteneinträge einer Zeile anzeigen
dat[,1:2]
dat[,1:5]

## Zeilen/Spalteneinträge einer Zeile anzeigen
dat[1:10,1:10]
dat[1:4,1:4]
dat[-(1:980),1:4]

dat$Alter_gerundet[dat$Alter_gerundet %in% c(30,40,50)]

dat$Alter_rounded <- round(dat$Alter_exakt,1)
table(dat$Alter_rounded)
dat[dat$Alter_gerundet==43,] 

dat[dat$Geschlecht==0,]

## Daten umstellen
sort(dat$Alter_exakt) #Ausgabe der sortierten Liste
unique(dat$Alter_gerundet) #einzelne Elemente
rev(dat$Alter_gerundet) #umgekehrte Reihenfolge

## Neue Variable erstellen: Kategorien bestimmen; HbA1c <=7; >7 bis 9, >9
dat$HbA1c
freq(dat$HbA1c)
hist(dat$HbA1c)
dat$HbA1c_7 <- cut(dat$HbA1c,
                      breaks = c(-Inf, 7, 9, Inf),
                      labels = c("well", "poor I", "poor II"),
                      right = TRUE)
table(dat$HbA1c_7)
summary(dat$HbA1c[dat$HbA1c_7=="well"])
summary(dat$HbA1c[dat$HbA1c_7=="poor I"])
summary(dat$HbA1c[dat$HbA1c_7=="poor II"])

## Mathematische Funktionen
log(dat$Alter_exakt)
exp(dat$Alter_exakt)
max(dat$Alter_exakt)
mean(dat$Alter_exakt)
sum(dat$Alter_exakt)
median(dat$Alter_exakt)
quantile(dat$Alter_exakt)
round(dat$Alter_exakt,1)
rank(dat$Alter_exakt)

## Operatoren
#a != b #a is not equal to b
#! logical NOT
#& logical AND
#a == b #a equals b
#a >= b
#| #logical OR
#a ^ b Exponentiation 

sort(dat$Alter_gerundet[dat$Alter_gerundet!=50])
sort(dat$Alter_gerundet[dat$Alter_gerundet==50])
sort(dat$Alter_gerundet[dat$Alter_gerundet==50 | dat$Alter_gerundet==60])
sort(dat$Alter_gerundet[dat$Alter_gerundet<50 & dat$Geschlecht==0])
sort(dat$Alter_gerundet[dat$Alter_gerundet<50 & dat$Geschlecht==1])
dat$Alter_gerundet^2

## Daten extrahieren in einen neuen Datensatz
cbind(dat$Alter_exakt,dat$Geschlecht)
rbind(dat[1,],dat[2,])
dat2 <- data.frame(cbind(dat$Alter_exakt,dat$Geschlecht))
dat2
colnames(dat2)<-c("Alter","Geschlecht")
dat2$Geschlecht<-factor(dat2$Geschlecht,levels=c(0,1),labels=c("0: female","1: male"))
table(dat2$Geschlecht)


##Aufgabe 1: Sortieren Sie die Werte für die Werte von crp. Wie hoch sind der Mittelwert und der Median?


##Aufgabe 2: Bilden Sie eine neue kategorielle Variable, die die Werte 0 (crp<=2) und 1 (crp>2) annimmt. 
#Tabben Sie die neue Variable und ermitteln Sie die Verteilungswerte.


####################################################################################
# 3. Fehlende Werte prüfen
####################################################################################

colSums(is.na(dat))  # Anzahl fehlender Werte pro Spalte
sum(is.na(dat))      # Gesamtanzahl fehlender Werte

#Visualierung fehlender Werte
gg_miss_var(dat)
gg_miss_upset(dat)

#Heatmap der fehlenden Werte; gemeinsame Missings über Variablen hinweg erkennbar
md.pattern(dat,rotate.names=TRUE)

####################################################################################
# 4. Deskriptive Statistiken
####################################################################################

# Grundlegende Statistik für numerische Variablen
summary(dat)
summary(dat$HbA1c)
summary(dat$Alter_exakt)
table(dat$Alter_exakt)
table(dat$Geschlecht)

# Detailliertere deskriptive Statistiken mit psych::describe()
describe(dat)

# Gruppierte deskriptive Statistiken

# Variante 1
summary(dat$HbA1c[dat$HbA1c_7=="well"])
summary(dat$HbA1c[dat$HbA1c_7=="poor I"])
summary(dat$HbA1c[dat$HbA1c_7=="poor II"])

# Variante 2; split dataset into subsets and compute summary statistics for each
aggregate(HbA1c ~ Geschlecht, data=dat, FUN = median)
aggregate(HbA1c ~ Geschlecht, data=dat, FUN = mean)
aggregate(HbA1c ~ Geschlecht, data=dat, 
                                FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x)) )

aggregate(HbA1c ~ HbA1c_7, data=dat, 
                           FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x)) )

# Variante 3, mit dplyr package
summary_HbA1c <- dat %>%
  group_by(Geschlecht) %>%
  summarise(
    count = n(),
    mean_HbA1c = mean(HbA1c, na.rm = TRUE),
    sd_HbA1c = sd(HbA1c, na.rm = TRUE),
    median_HbA1c = median(HbA1c, na.rm=TRUE),
    min_HbA1c = min(HbA1c, na.rm=TRUE),
    max_HbA1c = max(HbA1c, na.rm=TRUE)
  )
print(summary_HbA1c)

summary_HbA1c <- dat %>%
  summarise(
    count = n(),
    mean_HbA1c = mean(HbA1c, na.rm = TRUE),
    sd_HbA1c = sd(HbA1c, na.rm = TRUE),
    median_HbA1c = median(HbA1c, na.rm=TRUE),
    min_HbA1c = min(HbA1c, na.rm=TRUE),
    max_HbA1c = max(HbA1c, na.rm=TRUE)
  )
print(summary_HbA1c)

# Variante 4: mit dem Hmisc package von Harrell
summaryM_result <- summaryM( Triglyzeride + hdl ~ Geschlecht, data = dat, quant=c(0.25, 0.5, 0.75), na.include=FALSE)
summaryM_result
html(summaryM_result)

summaryM_result <- summaryM( Rauchen + Bildungslevel ~ Geschlecht, data = dat, quant=c(0.25, 0.5, 0.75), na.include=FALSE)
summaryM_result
html(summaryM_result)

# variante 5: mit dem gtsummary package

dat %>%
  select(Geschlecht, HbA1c, Fibrinogen) %>%
  tbl_summary()

dat %>%
  select(Geschlecht, HbA1c) %>%
  tbl_summary(
    by = Geschlecht,
    statistic = all_continuous() ~ "{median} ({p25}, {p75})"
  )

dat %>%
  select(Geschlecht, HbA1c, Fibrinogen) %>%
  tbl_summary(
    by = Geschlecht,
    statistic = all_continuous() ~ "{mean} ± {sd}"
  )

dat %>%
  select(Geschlecht, Rauchen, HbA1c, Fibrinogen, Todesfall) %>%
  tbl_summary(
    by = Todesfall,
    statistic = list(all_continuous() ~ "{median} ({p25}, {p75})", 
                     all_categorical() ~ "{n} ({p}%)")
    )


##Aufgabe 3: Ermitteln Sie die Verteilung (absolute und prozentuale Verteilung) der Kategorien für die Variable "Rauchen"


##Aufgabe 4: Ermitteln Sie N, Mittelwert, SD, Median, 25% und 75% Quantil für die Werte der Variablen "Zahnzahl_max28"


##Aufgabe 5: Ermitteln Sie Mittelwert und SD für die Werte der Variablen "Zahnzahl_max28" nach Kategorien von "Rauchen"



####################################################################################
### 5. Kreisdiagramme (Pie chart)
####################################################################################

#Farben anzeigen
colours()

## Häufigkeiten einer kategorialen Variable berechnen
# Variable als kategorielle variable deklarieren; Kategorien beschriften
dat$Familienstand <- factor(dat$Familienstand,levels=c(1,2,3,4,5),labels=c("1: verheiratet, lebe mit partner",
"2: verheiratet, lebe getrennt","3: ledig, nie verheiratet gewesen","4: geschieden","5: verwitwet"))

# Counts berechnen
counts <- table(dat$Familienstand)
counts

## Basis-R Kreisdiagramm
pie(counts)

pie(counts, 
    main="Familienstand")

pie(counts, 
    main="Familienstand", 
    col=c("yellow1","skyblue", "orange", "green","sienna"), 
    labels=names(counts))

## Kreisdiagramm mit ggplot2 (besseres Design)

dat_pie <- data.frame(
  familienstand = factor(names(counts)), # Labelling für das Kreisdiagramm
  count = as.numeric(counts) # Counts
)
dat_pie

#ggplot: Jede Grafik wird aus Komponenten wie Daten, Ästhetiken und Geometrien zusammengesetzt. 

#ggplot(data = <DATEN>,
  #aes(x = <X-VARIABLE>, y = <Y-VARIABLE>)) +
    #<GEOM-FUNKTION>() +
        #weitere_Optionen()

#aes(...): welche Variable kommt auf die x- und y-Achse; wie werden Farbe, Form oder Größe verwendet?
#geom(...): Geometrie, wie werden die Daten dargestellt (Punkte, Linien, Balken usw.)?
  #geom_point() → Streudiagramm
  #geom_line() → Liniendiagramm
  #geom_bar(stat = "identity") → Balkendiagramm (mit eigenen Werten)
  #geom_col() → ebenfalls Balkendiagramm (bei zählfertigen Daten)
  #geom_boxplot() → Boxplot
#abs() → Achsentitel, Überschrift, etc.
#theme_minimal() → Design der Grafik
#scale_y_continuous(labels = scales::comma) → Formatierung der Achsen

ggplot(data=dat_pie, 
       aes(x="", y=count, fill=familienstand)) +
          geom_bar(stat="identity", width=1)

ggplot(data=dat_pie, aes(x="", y=count, fill=familienstand)) +
  geom_bar(stat="identity", width=1) +
    coord_polar("y", start=0) # Macht das Kreisdiagramm zirkulär

ggplot(data=dat_pie, aes(x="", y=count, fill=familienstand)) +
  geom_bar(stat="identity", width=1) +
    coord_polar("y", start=0) + 
      theme_minimal() #Layout anpassen

ggplot(data=dat_pie, aes(x="", y=count, fill=familienstand)) +
  geom_bar(stat="identity", width=1) +
    coord_polar("y", start=0) + 
      theme_minimal() +
        labs(title="Verteilung des Familienstandes") + #Titel anpassen
          scale_fill_manual(values=c("1: verheiratet, lebe mit partner"="yellow1","2: verheiratet, lebe getrennt"="skyblue3",
                                     "3: ledig, nie verheiratet gewesen"="orange2","4: geschieden"="green4","5: verwitwet"="sienna1")) #Farben anpassen

####################################################################################
# 6. Verteilung numerischer Variablen visualisieren - Histogramme
####################################################################################

hist(dat$Gewicht)

## Titel und Achsenlabelling ergänzen
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",ylab="Häufigkeit") 

## Achsen
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",ylab="Häufigkeit",ylim=c(0,250)) 

## Colorierung
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",ylab="Häufigkeit",ylim=c(0,250),col="lightblue",border="black")
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",ylab="Häufigkeit",ylim=c(0,250),col="lightblue",border="white")

#Ausrichtung des Textes
par(las=1)
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",ylab="Häufigkeit",ylim=c(0,250),col="lightblue", border="white")

# Breaks
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",ylab="Häufigkeit",ylim=c(0,250),col="lightblue", border="white",
     breaks=c(30,40,50,60,70,80,90,100,110,120,130,140))

hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",ylab="Häufigkeit",ylim=c(0,250),col="lightblue", border="white",
     breaks=c(30,50,70,90,110,130,150))

# Häufigkeiten versus Dichten (relative Häufigkeiten)
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",freq=TRUE)
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",freq=FALSE)

# Sollen die Intervalle rechts geschlossen und links offen sein? >30-40, >40-50, ...
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",right=TRUE)
hist(dat$Gewicht, main="Histogramm Gewicht", xlab="Gewicht",right=FALSE)

#Histogramm mit ggplot
ggplot(data=dat, aes(x = Gewicht)) +
  geom_histogram(binwidth = 5, fill = "steelblue", color = "black") +
    labs(title = "Histogramm Gewicht", x = "Gewicht", y = "Häufigkeit")

#Breite der Balken ändern
ggplot(data=dat, aes(x = Gewicht)) +
  geom_histogram(binwidth = 10, fill = "steelblue", color = "black") +
    labs(title = "Histogramm Gewicht", x = "Gewicht", y = "Häufigkeit")

ggplot(data=dat, aes(x = Gewicht)) +
  geom_histogram(binwidth = 10, fill = "steelblue", color = "black") +
    labs(title = "Histogramm Gewicht", x = "Gewicht", y = "Häufigkeit") +
      theme_minimal() +
        scale_x_continuous(breaks=c(30,40,50,60,70,80,90,100,110,120,130))


####################################################################################
# 7. Boxplots für eine numerische Variable
####################################################################################

boxplot(dat$DMFT_max14)

# Labelling und Coloring
boxplot(dat$DMFT_max14, main="Boxplot DMFT",ylab="DMFT (14 Zähne)", col="orange")

# Darstellung mehrerer Variablen
boxplot(dat$DMFT_max14,dat$DFT_max14, main="Boxplot DMFT und DFT",ylab="DMFT (14 Zähne)", col="orange",
        names=c("DMFT","DFT"))

# Gruppenvergleiche
boxplot(dat$DMFT_max14[dat$Geschlecht==0],dat$DMFT_max14[dat$Geschlecht==1], main="Boxplot DMFT",ylab="DMFT (14 Zähne)", col="orange")
axis(side=1,lab=c("Frauen","Männer"),at=c(1,2))
mtext(side=1,line=2,"Geschlecht",at=1.5)

boxplot(dat$DMFT_max14[dat$Geschlecht==0],dat$DMFT_max14[dat$Geschlecht==1], main="Boxplot DMFT",ylab="DMFT (14 Zähne)", col="orange",
        names=c("Frauen","Männer"))

# Boxplot mit ggplot
dat$Geschlecht<-factor(dat$Geschlecht,levels=c(0,1),labels=c("0: Frauen","1: Männer"))

ggplot(data = dat, aes(group = Geschlecht, y = DMFT_max14)) +
  geom_boxplot() +
    labs(y="DMFT (14 Zähne)", x="", title="Boxplot DMFT") 

ggplot(data = dat, aes(fill = Geschlecht, y = DMFT_max14)) +
  geom_boxplot() +
    labs(y="DMFT (14 Zähne)", x="", title="Boxplot") +
      theme(axis.text.x = element_blank()) +
        scale_y_continuous( breaks=c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15) )

ggplot(data = dat, aes(x = Geschlecht, fill = as.factor(Diabetes), y = mean_CAL)) +
  geom_boxplot() +
    labs(y="Mittlerer Attachmentverlust, mm", x="", title="Boxplot") 

#Labelling für Diabetes anpassen
dat$Diabetes <- factor(dat$Diabetes,levels=c(0,1),labels=c("0: nein","1: ja"))

ggplot(data = dat, aes(x = Geschlecht, fill = Diabetes, y = mean_CAL)) +
  geom_boxplot() +
    labs(y="Mean CAL, mm", x="", title="Boxplot") 

#Splitten der Grafik - mit facet_wrap
ggplot(data = dat, aes(x = Geschlecht, fill = Diabetes, y = mean_CAL)) +
  geom_boxplot() +
    labs(y="Mean CAL, mm", x="", title="Boxplot") +
      facet_wrap( ~ Geschlecht, scale="free")

####################################################################################
# 8. Streudiagramm für zwei numerische Variablen
####################################################################################

plot(BMI_exakt ~ Alter_exakt, data=dat)
plot(BMI_exakt ~ Alter_exakt, data=dat, xlab="Alter, Jahre", ylab=expression(paste("BMI, kg/",m^2)))

#Ausrichtung der y-Achse und Ändern der Grafikränder
par(las=1,mai=c(1,1,1,1))

#Punktelayout ändern: Form und Farbe
plot(BMI_exakt ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab=expression(paste("BMI, kg/",m^2)),
     pch=3)

plot(BMI_exakt ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab=expression(paste("BMI, kg/",m^2)),
     pch=20,col="steelblue")

# einfaches Streudiagramm mit ggplot
ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt)) +
  geom_point()

#  Colorierung 
ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt)) +
  geom_point(color="steelblue")

# Beschriftungen
ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt)) +
  geom_point(color="steelblue") +
    labs(title="Zusammenhang zwischen Alter und BMI", x="Alter (Jahre)", 
       y=expression(paste("BMI (kg/",m^2,")")))

ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt)) +
  geom_point(color="steelblue") +
  labs(title="Zusammenhang zwischen Alter und BMI", x="Alter (Jahre)", y=expression(paste("BMI (kg/",m^2,")")), caption="Based on SHIP data.")

#Beschriftung entfernen
ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt)) +
  geom_point(color="steelblue") +
  labs(title="Zusammenhang zwischen Alter und BMI", x=NULL, y=NULL, caption=NULL)

#Layout ändern; auf minimal setzen
ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt)) +
  geom_point(color="steelblue") +
  theme_minimal() +
  labs(title="Zusammenhang zwischen Alter und BMI", x="Alter (Jahre)", y=expression(paste("BMI (kg/",m^2,")")))

#Coloring
ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt, color = Rauchen)) +
  geom_point() 

#Definiere Rauchen als kategorielle (Faktor-) Variable
dat$Rauchen<-factor(dat$Rauchen,levels=c(0,1,2),labels=c("0: Never","1: Former","2: Current"))

ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt, color = Rauchen)) +
  geom_point() 

ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt, color = Rauchen)) +
  geom_point() + 
    scale_color_manual(values = c("orange1", "steelblue", "green3")) +
        labs(title="Zusammenhang zwischen Alter und BMI", x="Alter (Jahre)", y=expression(paste("BMI (kg/",m^2,")")), colour = "Rauchstatus")

####################################################################################
# 9. Korrelation zwischen numerischen Variablen berechnen
####################################################################################

#Korrelationen zwischen zwei Variablen berechnen
cor(dat$Alter_exakt, dat$BMI_exakt)
cor(dat$Alter_exakt, dat$BMI_exakt, method = "pearson")
cor(dat$Alter_exakt, dat$BMI_exakt, method = "spearman")

#Korrelationsmatrix und Visualisierung
cor(dat[,c("Alter_exakt","Cholesterol","crp","mean_CAL","Zahnzahl_max28")],use = "complete.obs", method = "spearman")
cor_matrix <- cor(dat[,c("Alter_exakt","Cholesterol","crp","mean_CAL","Zahnzahl_max28")],use = "complete.obs", method = "spearman")

#r und p values extrahieren
result <- rcorr(as.matrix(dat[,c("Alter_exakt","Cholesterol","crp","mean_CAL","Zahnzahl_max28")], method="spearman"))
result

# Correlation coefficients
result$r

# P-values
result$P

corrplot(cor_matrix, method = "color", type = "lower", tl.col = "black")
corrplot(cor_matrix, method = "circle", type = "lower", tl.col = "black")
corrplot(cor_matrix, method = "pie", type = "lower", tl.col = "black")
corrplot(cor_matrix, method = "square", type = "lower", tl.col = "black")


####################################################################################
# 10. Balkendiagramm für eine kategoriale Variable
####################################################################################

# einfache Balkendiagramme - nicht geeignet
barplot(dat$hdl, names.arg = "", col = "skyblue", main = "HDL")

# einfache Balkendiagramme für kategorielle Variablen
barplot( table(dat$HbA1c_7), main = "HbA1c, %")
barplot( table(dat$HbA1c_7), names.arg = c("Well controlled","Poorly controlled I","Poorly controlled II"), col = "skyblue", main = "HbA1c, %")

# Beschriftungen ändern
barplot( table(dat$Familienstand), col = "skyblue", main = "Familienstand")
barplot( table(dat$Familienstand), names.arg = "", col = "skyblue", main = "Familienstand")

# Prozentwerte plotten
TAB <- 100 * table(dat$Familienstand) / sum(table(dat$Familienstand))
r <- barplot( TAB, col = "skyblue", main = "Familienstand", ylim=c(0,70), ylab="Prozentanteil")
text(r,TAB+3,TAB)

# Horizontales Balkendiagramm
par(las=1, mai=c(1,3,1,1))
barplot( TAB, col = "skyblue", main = "Horizontales Balkendiagramm", xlim=c(0,70), xlab="Prozentanteil", horiz=TRUE)

# Gruppiertes Balkendiagramm, absolute Häufigkeiten
TAB <- 100 * table(dat$Geschlecht, dat$Familienstand)
barplot( TAB, beside = TRUE, col = c("steelblue", "orange"), main = "Gruppiertes Balkendiagramm", legend.text=TRUE)

# Gruppiertes Balkendiagramm, Zeilenprozente
# margin=1: Zeilenprozente, margin=2: Spaltenprozente
TAB2 <- 100 * prop.table(table(dat$Geschlecht, dat$Familienstand), margin=1)
barplot( TAB2, beside = TRUE, col = c("steelblue", "orange"), main = "Gruppiertes Balkendiagramm", legend.text=TRUE)

# Balkendiagramme mit ggplot
ggplot(dat, aes(x=Familienstand)) +
  geom_bar() +
  theme_minimal() +
    labs(title="Verteilung des Familienstandes", x="Familienstand", y="Anzahl")

ggplot(dat, aes(x=Familienstand)) +
  geom_bar(fill="steelblue") +
  theme_minimal() +
  labs(title="Verteilung des Familienstandes", x="Familienstand", y="Anzahl")

dat$Familienstand <- factor(dat$Familienstand,
                       levels = c("1: verheiratet, lebe mit partner","2: verheiratet, lebe getrennt","3: ledig, nie verheiratet gewesen","4: geschieden","5: verwitwet"),
                       labels = c("Verheiratet, lebe mit Partner","Verheiratet, lebe getrennt","Ledig, nie verheiratet gewesen","Geschieden", "Verwitwet"))

ggplot(dat, aes(x=Familienstand)) +
  geom_bar(fill="steelblue") +
    theme_minimal() +
      labs(title="Verteilung des Familienstandes", x="Familienstand", y="Anzahl")

# Labelling ändern
df <- data.frame(
  Kategorie = c("Verheiratet, lebe mit partner","Verheiratet, lebe getrennt","Ledig, nie verheiratet gewesen","Geschieden", "Verwitwet"),
  Wert = table(dat$Familienstand)
); df

ggplot(df, aes(x = Kategorie, y = Wert.Freq)) +
  geom_bar(stat = "identity", fill="steelblue") +
    theme_minimal() +
      labs(title="Verteilung des Familienstandes", x="Familienstand", y="Anzahl")

# Werte ergänzen über den Balken
ggplot(df, aes(x = Kategorie, y = Wert.Freq)) +
  geom_bar(stat = "identity", fill="steelblue") +
  theme_minimal() +
  labs(title="Verteilung des Familienstandes", x="Familienstand", y="Anzahl") + 
  geom_text(aes(label = Wert.Freq), vjust = -0.5,color="black")


####################################################################################
# 11. Export von Grafiken
####################################################################################

#Export als PDF

pdf("Barplot1.pdf", height=8, width=12)

ggplot(df, aes(x = Kategorie, y = Wert.Freq)) +
  geom_bar(stat = "identity", fill="steelblue") +
  theme_minimal() +
  labs(title="Verteilung des Familienstandes", x="Familienstand", y="Anzahl") + 
  geom_text(aes(label = Wert.Freq), vjust = -0.5,color="black")

dev.off()

#Export als JPEG

jpeg("Barplot1.jpg",res=300, height=1400, width=2600)

ggplot(df, aes(x = Kategorie, y = Wert.Freq)) +
  geom_bar(stat = "identity", fill="steelblue") +
    theme_minimal() +
      labs(title="Verteilung des Familienstandes", x="Familienstand", y="Anzahl") + 
        geom_text(aes(label = Wert.Freq), vjust = -0.5,color="black")

dev.off()

# Aufteilung mit layout

mat=matrix( c(1,2,3,4), nrow=2 ); mat
layout(mat, widths = rep.int(1, ncol(mat)), heights = rep.int(1, nrow(mat)), respect = TRUE)
layout.show(n = 4)
layout(mat, widths = rep.int(1, ncol(mat)), heights = rep.int(1, nrow(mat)), respect = FALSE)
layout.show(n = 4)

pdf("Barplot2.pdf", height=8, width=12)

layout(mat, widths = rep.int(1, ncol(mat)), heights = rep.int(1, nrow(mat)), respect = TRUE)

plot(BMI_exakt ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab=expression(paste("BMI, kg/",m^2)),col="steelblue")
plot(crp ~ Alter_exakt,data=dat[dat$crp<50,],xlab="Alter, Jahre", ylab="CRP, g/l", col="steelblue")
plot(Taille ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab="Taillenumfang, cm",col="steelblue")
plot(Haemoglobin ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab="HbA1c, %",col="steelblue")

dev.off()


# Aufteilung mit mfrow

pdf("Barplot3.pdf", height=12, width=12)

par(mfrow=c(2,2),las=1)
plot(BMI_exakt ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab=expression(paste("BMI, kg/",m^2)),col="steelblue")
plot(crp ~ Alter_exakt,data=dat[dat$crp<50,],xlab="Alter, Jahre", ylab="CRP, g/l", col="steelblue")
plot(Taille ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab="Taillenumfang, cm",col="steelblue")
plot(Haemoglobin ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab="HbA1c, %",col="steelblue")

dev.off()


## Schriftgrößen ändern
#cex, cex.axis, cex.lab

pdf("Barplot3.pdf", height=12, width=12)

par(mfrow=c(2,2),las=1,mai=c(1,1,1,1))
plot(BMI_exakt ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab=expression(paste("BMI, kg/",m^2)),col="steelblue",
     cex=1.5, cex.axis=1.5, cex.lab=1.5)
# Punktgröße
plot(crp ~ Alter_exakt,data=dat[dat$crp<50,],xlab="Alter, Jahre", ylab="CRP, g/l", col="steelblue",
     cex=1.5)
# Achsenbeschriftung
plot(Taille ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab="Taillenumfang, cm",col="steelblue",
     cex.axis=1.5)
# Achsenlabel
plot(Haemoglobin ~ Alter_exakt,data=dat,xlab="Alter, Jahre", ylab="HbA1c, %",col="steelblue",
     cex.lab=1.5)

dev.off()

#ggplot-Grafiken zusammenfügen - mit plot_grid

g1 <- ggplot(dat, aes(x=Alter_exakt, y=BMI_exakt, color = Rauchen)) +
  geom_point() + labs(y="BMI, kg/m2", x="Alter"); g1

g2 <- ggplot(data = dat, aes(x = Geschlecht, y = mean_CAL)) +
  geom_boxplot() +
  labs(y="Mittlerer Attachmentverlust, mm", x="", title="Boxplot"); g2

plot_grid(g1, g2)
plot_grid(g1, g2, labels = "AUTO", ncol = 2)
plot_grid(g1, g2, labels = c("A)", "B)"), ncol = 2)

#ggplot-Grafiken zusammenfügen - mit grid.arrange

grid.arrange(g1, g2, ncol = 2)
grid.arrange(g1, g2, ncol = 2, widths=c(3,5))
grid.arrange(g1, g2, ncol = 1)
grid.arrange(g1, g2, ncol = 1, heights=c(2,4))

#Speichern der aktuellen ggplot-Grafik mit ggsave
ggsave("ggplot.pdf",width=10,height=5,dpi=300)

## Aufgabe 6: Erstellen und exportieren Sie eine PDF-Datei mit 4 Grafiken: 

#1. Histogramm der mean CAL Werte; Angabe der absoluten Häufigkeiten
#2. Balkendiagramm der kategoriellen Glukose-Werte (<7,8; 7,8 - 11,0; >11,0 mmol/l)
#3. Streudiagramm von Glukose (x) und mean CAL (y)
#4. Boxplot der mean CAL Werte (y) nach den kategoriellen Glukose-Werten (x)

#Beschriften Sie die Grafiken angemessen. Labeln Sie die Grafiken.

