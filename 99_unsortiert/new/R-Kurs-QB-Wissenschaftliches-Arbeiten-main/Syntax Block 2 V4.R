## ============================================================
## Teil 2 – Kreuztabellen, Abhängigkeit, epidemiologische Maßzahlen,
##          Diagnostische Tests
## ============================================================

# ------------------------------------------------------------
# Installation aller benötigten Pakete (+ Abhängigkeiten)
# Nur nötig, falls noch nicht vorhanden
# ------------------------------------------------------------
#install.packages(
#  c("dplyr",     # Datenmanipulation (Filtern, Gruppieren, Zusammenfassen)
#    "ggplot2",   # Grafiken erstellen 
#    "gmodels",   # CrossTable-Funktion 
#    "epiR",      # Sehr umfangreich, Standard für 2x2 Tabellen
#    "epitools",  # Odds Ratio, Risk Ratio, einfache Tabellen
#    "Epi"),      # twoby2()-Funktion
#  dependencies = TRUE
#)

# ------------------------------------------------------------
# Pakete laden
# ------------------------------------------------------------
library(dplyr)     
library(ggplot2)   
library(gmodels)  

# Epidemiologie-Pakete:
library(epiR)        
library(epitools)    
library(Epi)         

## ------------------------------------------------------------
## Daten laden
## ------------------------------------------------------------

rm(list = ls())

#load("Daten_Blockseminar2.rdata")

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

## Vorbemerkung: Wir arbeiten hier mit Querschnittsdaten, aus denen sich weder 
## eine zeitliche Abfolge noch kausale Zusammenhänge ableiten lassen. 
## Wir nutzen diese Daten dennoch für Übungszwecke; in einer realen Studie wäre
## ein qualifiziertes Studiendesign für jede Fragestellung nötig. 


## ------------------------------------------------------------
## 2x2-Kreuztabellen erstellen 
## ------------------------------------------------------------

# Einfache Tabelle
tab_bsp <- table(dat$Sport, dat$Diabetes)
tab_bsp

# Mit einfacher Beschriftung
dimnames(tab_bsp) <- list(
  "Sport"      = c("Nein", "Ja"),  
  "Diabetes"   = c("Nein", "Ja")               
)
tab_bsp

# Wenn %-Angaben gewünscht sind
prop.table(tab_bsp)                 # Rel. Häufigkeiten über alle Zellen (Gesamtsumme=1)
prop.table(tab_bsp, margin=1)       # Zeilenprozente  (Zeilensumme=1)
prop.table(tab_bsp, margin=2)       # Spaltenprozente (Spaltensumme=1) 

# Mit Rand-Summen (Gesamt)
addmargins(tab_bsp)

# Nutzung der CrossTable-Funktion
CrossTable(dat$Sport, dat$Diabetes,
           prop.r=TRUE, prop.c=FALSE, prop.t=FALSE, chisq=FALSE)


## Problem, damit die aus der Vorlesung gelernten Formeln anwendbar sind, benötigen wir folgende Darstellung:

##              Erkrankung:  krank  gesund
## Exposition:
## Exponiert                    a      b
## Nicht exponiert              c      d

## d.h. oben links, an Position "a", stehen die Erkrankten mit Exposition und nicht wie in unserem Beispiel oben rechts an Position "b"
## Es gibt 2 Lösungsmöglichkeiten: Entweder die Formeln anpassen oder die Tabelle umstellen. 
## Wir stellen hier die Tabelle um, da auch manche Epi-Pakete in R genau diese Anordnung benötigen. 


## ------------------------------------------------------------
## 2x2-Kreuztabellen umstellen  
## ------------------------------------------------------------
# Labels werden hier direkt bei der Erzeugung der Variablen erstellt, sodass hierfür später keine Beschriftung der Kategorien hinzugefügt werden muss.

# Bewegungsmangel als Exposition: 0 = kein Sport = exponiert wegen Bewegungsmangel , 1 = Sport = nicht exponiert
dat$Bewegungsmangel_Exposition <- factor(dat$Sport,
                        levels = c(0,1),               
                        labels = c("Bewegungsmangel", "nicht exponiert"))

# Diabetes als Erkrankung: 0 = nein = gesund, 1 = ja = Diabetes
dat$Diabetes_Erkrankung <- factor(dat$Diabetes,
                           levels = c(1,0),            
                           labels = c("Diabetes", "gesund"))

tab_bsp2 <- table(dat$Bewegungsmangel_Exposition, dat$Diabetes_Erkrankung,
                 dnn = c("Exposition", "Erkrankung"))
tab_bsp2
addmargins(tab_bsp2)


## ------------------------------------------------------------
## Einfache "Prüfung" der Unabhängigkeit  
## ------------------------------------------------------------

# Unabhängigkeit
# Zwei Ereignisse sind unabhängig, wenn das Auftreten des einen Ereignisses die 
# Wahrscheinlichkeit für das andere Ereignis nicht beeinflusst. 
# P(A)=P(A|B)=P(A|nicht B)

# Abhängigkeit
# Zwei Ereignisse sind abhängig, wenn das Auftreten des einen Ereignisses die 
# Wahrscheinlichkeit für das andere Ereignis beeinflusst. 
# P(A)≠ P(A|B)≠ P(A|nicht B) 

# Für unsere Tabelle gilt mit A= Diabetes und B=Bewegungsmangel nun die Frage:
# Was trifft zu?
# P(Diabetes) = P(Diabetes | Bewegungsmangel) = P(Diabetes | kein Bewegungsmangel) 
# oder 
# P(Diabetes) ≠ P(Diabetes | Bewegungsmangel) ≠ P(Diabetes | kein Bewegungsmangel) 

# P(Diabetes)= (a+c)/(a+b+c+d)
# P (Diabetes | Bewegungsmangel)= a / (a+b) 
# P (Diabetes | kein Bewegungsmangel)= c / (c+d) 

# direkte Berechnung 
(90+48) / (90+485+48+377)
(90) / (90+485)
(48) / (48+377)

# oder mit Umcodierung zu a,b,c,d
a <- tab_bsp2[1,1]
b <- tab_bsp2[1,2]
c <- tab_bsp2[2,1]
d <- tab_bsp2[2,2]

(a+c)/(a+b+c+d)
a / (a+b) 
c / (c+d)


## ------------------------------------------------------------
## Alternativen
## ------------------------------------------------------------

# Vergleich der Zeilenprozente
prop.table(tab_bsp2, margin=1)       

# Grafische Darstellung der Anteile
ggplot(dat, aes(x = Bewegungsmangel_Exposition, fill = Diabetes_Erkrankung)) +
  geom_bar(position = "fill") +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Verteilung von Diabetes innerhalb Bewegungsmangel-Kategorien",
       x = "Bewegungsmangel", y = "Anteil", fill = "Diabetes") +
  theme_minimal()

# Hinweis: Diese einfachen Herangehensweisen dienen der Ersteinschätzung und 
# sind kein Ersatz für valide statistische Tests. 


## ------------------------------------------------------------
## Aufgabe 1
## ------------------------------------------------------------

# a) Sind Diabetes und Bewegungsmangel nach der obigen formalen Definition abhängige oder unabhängige Ereignisse?
# b) Erzeugen Sie in R eine Kreuztabelle für Geschlecht (aktuell: 0=Frauen und 1= Männer) und Hypertonie (aktuell: 0=gesund und 1=Hypertonie). 
# c) Sind Geschlecht und Hypertonie abhängige Ereignisse? Nutzen Sie zur Berechnung R oder alternativ Ihren Handy-Taschenrechner. 


## ------------------------------------------------------------
## Berechnung einfacher epidemiologischer Maßzahlen "per Hand"
## ------------------------------------------------------------

# Falls in der Aufgabe zuvor überschrieben, setzen wir a,b,c & d wieder auf unsere Beispielwerte
a <- tab_bsp2[1,1]
b <- tab_bsp2[1,2]
c <- tab_bsp2[2,1]
d <- tab_bsp2[2,2]

# Risiken (entsprechen den theoretischen Wahrscheinlichkeiten)
risk_exp   <- a / (a + b)   # Risiko unter Exponierten 
risk_unexp <- c / (c + d)   # Risiko unter Nicht-Exponierten

# Maßzahlen
RD <- risk_exp - risk_unexp       # Risk Difference (absolute Differenz)
RR <- risk_exp / risk_unexp       # Risk Ratio
OR <- (a * d) / (b * c)           # Odds Ratio (Diagonalmultiplikation)
odds_exp   <- a / b               # Odds der Exponierten
odds_unexp <- c / d               # Odds der Nicht-Exponierten

# Ausgabe 
list(
  Zellen = c(a=a, b=b, c=c, d=d),
  Risiken = c(Exponiert = risk_exp, Nicht_exponiert = risk_unexp),
  RD = RD, RR = RR, OR = OR,
  Odds = c(Exponiert = odds_exp, Nicht_exponiert = odds_unexp)
)

## ------------------------------------------------------------
## Berechnung einfacher epidemiologischer Maßzahlen mit R-Paketen
## ------------------------------------------------------------


## epiR
# Cohort/count-Interpretation (Exposition -> Outcome)
epiR_cohort <- epi.2by2(tab_bsp2, method = "cohort.count", conf.level = 0.95, units = 100)
epiR_cohort  # enthält RR, OR, RD, Risiken usw.

## epitools
epitools_rr <- epitools::riskratio(tab_bsp2)   # RR (+ KI)
epitools_or <- epitools::oddsratio(tab_bsp2)   # OR (+ KI)
epitools_rr
epitools_or

## --- Epi ---
twoby2(tab_bsp2)
# liefert schön tabellarisch: Risiken, RR, OR, Attributable Risk

# Es gibt noch weitere Pakete mit leicht anderen Outputs 
# Wahl des "richtigen" Pakets nach Studiendesign, gewünschten Ausgabevariablen & persönlicher Präferenz


## ------------------------------------------------------------
## Ausblick: Odds Ratios sind für binäre Variablen bzw. 2x2 - Tabellen gedacht. 
##           Was passiert dann bei mehr als 2 Kategorien?
## ------------------------------------------------------------

# Outcome hat > 2 Kategorien: dichotomisieren oder multinomiale logistische Regression
# Exposition hat > 2 Kategorien: Aufsplitten auf mehrere 2x2 Tabellen mit jeweils gleicher Referenz (nicht exponiert)
#                                Oder logistische Regression mit kategorialer Exposition


## ------------------------------------------------------------
## Aufgabe 2
## ------------------------------------------------------------

# Parodontitis-Erkrankung definieren
dat$Paro <- ifelse(is.na(dat$mean_CAL), NA,          # NAs bleiben NAs
            ifelse(dat$mean_CAL >= 3, "Parodontitis", "gesund"))

# Als Faktor mit definierter Reihenfolge
dat$Paro <- factor(dat$Paro, levels = c("Parodontitis", "gesund"))

# Kontrolle
table(dat$Paro, useNA = "ifany")

tab_bsp3 <- table(dat$Paro, dat$Diabetes_Erkrankung,
                  dnn = c("Exposition", "Erkrankung"))
tab_bsp3
addmargins(tab_bsp3)

# a) Wann hat ein Proband in diesem Beispiel Parodontitis?
# b) Wie hoch ist die Gesamtanzahl (N) in tab_bsp3? Warum ist sie nicht 1000?
# c) Berechnen Sie RR, RD und OR "per Hand" und mit einem R-Paket Ihrer Wahl. 


## ------------------------------------------------------------
## Diagnostische Tests
## ------------------------------------------------------------

# Es geht hier nicht um statistische Tests, sondern um die Güte medizinischer 
# Tests bei der Diagnose einer Zielerkrankung. Denn auch hier lassen sich 
# grundlegende Maßzahlen leicht aus Vierfeldertafeln ableiten. 

# Beispiel-Szenario:
# Index-Test: Urin-Glukose (negativ/positiv)
# Krankheit: Diabetes_Erkrankung (gesund/Diabetes)
tab_test_bsp1 <- table(dat$Glukose_Urin, dat$Diabetes_Erkrankung)
tab_test_bsp1

# benötigte 2×2-Notation:
#                 Erkrankung
#            |   ja     |    nein
# -----------+----------+----------
# TEST +     |    a     |     b
# TEST -     |    c     |     d
#
# a = TP (True Positive), b = FP (False Positive)
# c = FN (False Negative), d = TN (True Negative)

# Da unsere Tabelle wieder nicht entsprechend der Vorgabe angeordnet ist, stellen wir um:

# Urin-Glukose als Test: negativ = keine Urin-Glukose = negatives Testergebnis , positiv = Urin-Glukose vorhanden = positives Testergebnis 
dat$U_Glukose_Test <- factor(dat$Glukose_Urin,
                            levels = c("positiv","negativ"),               
                            labels = c("positiv", "negativ"))

tab_test_bsp2 <- table(dat$U_Glukose_Test, dat$Diabetes_Erkrankung,
                  dnn = c("Test", "Erkrankung"))
tab_test_bsp2

## ------------------------------------------------------------
## Berechnung der Maßzahlen für diagnostische Tests "per Hand"
## ------------------------------------------------------------

a <- tab_test_bsp2["positiv","Diabetes"]
b <- tab_test_bsp2["positiv","gesund"]
c <- tab_test_bsp2["negativ","Diabetes"]
d <- tab_test_bsp2["negativ","gesund"]

N   <- a + b + c + d
prev <- (a + c) / N                    # Prävalenz (Anteil Kranker)
acc  <- (a + d) / N                    # Accuracy (Gesamt-Trefferrate)

sens <- a / (a + c)                    # Sensitivität (unter den Kranken: Anteil positiver Test)
spec <- d / (d + b)                    # Spezifität (unter den Gesunden: Anteil negativer Test)
ppv  <- a / (a + b)                    # Positiver Vorhersagewert (unter positiver Test: Anteil krank)
npv  <- d / (d + c)                    # Negativer Vorhersagewert (unter negativer Test: Anteil gesund)

# Ausgabe
list(N=N, Prävalenz=prev, Accuracy=acc,
     Sensitivität=sens, Spezifität=spec, PPV=ppv, NPV=npv)

# Fehlerarten (rein konzeptionell):
# Falsch-positiv (FP=b): gesunde Person wird fälschlich als „krank“ klassifiziert.
# Falsch-negativ (FN=c): kranke Person wird fälschlich als „gesund“ klassifiziert.
# Häufige Bezeichnungen: 
# FP = Fehler 1. Art = α-Fehler
# FN = Fehler 2. Art = β-Fehler


# Visualisierung (beschriftete Kacheln):
mat_df <- data.frame(
  Test = factor(rep(c("positiv","negativ"), each=2), levels=c("positiv","negativ")),
  Disease = factor(rep(c("ja","nein"), times=2), levels=c("ja","nein")),
  Count = c(a,b,c,d),
  Label = c("TP (a)","FP (b)","FN (c)","TN (d)")
)

ggplot(mat_df, aes(Disease, Test, fill=Count)) +
  geom_tile() +
  geom_text(aes(label=paste0(Label,"\n",Count)), color="white", fontface="bold") +
  scale_fill_gradient(low="#6baed6", high="#08306b") +
  scale_y_discrete(limits = rev(levels(mat_df$Test))) +  # Y-Achse umdrehen
  labs(title="2×2-Matrix: Test vs. Realität",
       x="Krankheit", y="Test") +
  theme_minimal()


## ------------------------------------------------------------
## Berechnung der Maßzahlen für diagnostische Tests mit R-Paketen
## ------------------------------------------------------------

# Tabelle: Zeilen = Test (positiv/negativ), Spalten = Erkrankung (ja/nein)
# Hier ist die korrekte Anordnung ganz essentiell!
tab_test_bsp2

# Diagnostische Kennzahlen mit EpiR - sehr umfangreich
epi.tests(tab_test_bsp2, conf.level = 0.95)


## ------------------------------------------------------------
## Aufgabe 3
## ------------------------------------------------------------

# Wir erzeugen eine "Karieserkrankung"
dat$DFT_Erkrankung <- ifelse(is.na(dat$DFT_max14), NA, 
                      ifelse(dat$DFT_max14 < 10, "gesund", "krank"))
# als Faktor mit richtiger Reihenfolge
dat$DFT_Erkrankung <- factor(dat$DFT_Erkrankung, levels = c("krank", "gesund"))
table(dat$DFT_Erkrankung, useNA = "ifany")

# Der genutzte "Test" ist mind. 5 Zahnarztbesuche im letzten Jahr (viel Behandlungsbedarf)
dat$Besuche_Test <- ifelse(is.na(dat$Zahnarztbesuche), NA,
                    ifelse(dat$Zahnarztbesuche < 5, "negativ", "positiv"))
dat$Besuche_Test <- factor(dat$Besuche_Test, levels = c("positiv","negativ"))
table(dat$Besuche_Test, useNA = "ifany")

tab_test_aufg3 <- table(dat$Besuche_Test, dat$DFT_Erkrankung)
tab_test_aufg3
# kein Umstellen nötig (durch passende Vorab-Spezifikation)

# a) Was sind Sensitivität, Spezifität, PPV und NPV des angewendeten Tests?
# b) Stellen Sie sich vor, es ist keine Untersuchung, sondern nur eine Patientenbefragung möglich.
#    Ist in einem solchen Fall der konzipierte Test sinnvoll für die Identifikation von Patienten mit großer Karieslast?
# c) Vergleichen Sie die Ausgaben von epi.tests(tab_test_bsp1, conf.level = 0.95) und epi.tests(tab_test_bsp2, conf.level = 0.95). 
#    Diskutieren Sie, wie die Unterschiede zustande kommen. 
