rm(list = ls())

library(dplyr)
library(ggplot2)


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


# Vorbereiten der Daten
# ---------------------
df1 <- dat %>%
        mutate(sex = as.factor(Geschlecht)) # Variable 'Geschlecht' in Faktor umwandeln, als 'sex' speichern

# sturer t-Test und reporting
# ---------------------------
t.test(Zahnzahl_max28 ~ sex, data = df1) # t-Test: mittlere Zahnzahl zwischen Geschlechtern vergleichen

# t.test(Zahnzahl_max28 ~ sex, data = df1, var.equal = TRUE) # t-Test für homogene Varianzen

t.test(Zahnzahl_max28 ~ sex, data = df1, alternative = "greater") # einseitig testen

df1 %>%
  group_by(sex) %>%                                # Nach Geschlecht gruppieren
  summarise(
    mean   = mean(Zahnzahl_max28, na.rm = TRUE),          # Mittelwert
    sd     = sd(Zahnzahl_max28, na.rm = TRUE))            # Standardabweichung

# Cohen's d
n1 <- sum(df1$sex == 0) # Gruppengröße
n2 <- sum(df1$sex == 1)

m1 <- mean(df1$Zahnzahl_max28[df1$sex == 0]) # Mittelwerte
m2 <- mean(df1$Zahnzahl_max28[df1$sex == 1])

s1 <- sd(df1$Zahnzahl_max28[df1$sex == 0]) # Standardabweichung
s2 <- sd(df1$Zahnzahl_max28[df1$sex == 1])

s_pooled <- sqrt(((n1 - 1) * s1^2 + (n2 - 1) * s2^2) / (n1 + n2 - 2)) # gepoolte Standardabweichung

(m1 - m2) / s_pooled # d


# wir gucken genauer hin
# ----------------------

# Stichprobe
table(df1$sex, useNA = "always")
table(df1$Zahnzahl_max28, df1$sex, useNA = "always")

# Konfidenzintervalle
df1 %>%
  group_by(Geschlecht) %>%                                # Nach Geschlecht gruppieren
  summarise(
    mean   = mean(Zahnzahl_max28, na.rm = TRUE),          # Mittelwert
    sd     = sd(Zahnzahl_max28, na.rm = TRUE),            # Standardabweichung
    n      = sum(!is.na(Zahnzahl_max28)),                 # Stichprobengröße, brauchen wir für CI
    se     = sd / sqrt(n),                                # Standardfehler, brauchen wir für CI
    ci_low = mean - qt(0.975, df = n - 1) * se,           # Untere Grenze 95%-CI
    ci_up  = mean + qt(0.975, df = n - 1) * se            # Obere Grenze 95%-CI
  )

# boxplot
ggplot(df1, aes(x = sex, y = Zahnzahl_max28)) +
  geom_boxplot() +
  geom_jitter() + # Punkte leicht gestreut
  labs(x = "Geschlecht", y = "Zahnzahl (max 28)")

# Verteilung
ggplot(df1, aes(x = Zahnzahl_max28)) +
  geom_histogram(bins = 29) +
  facet_wrap(~ sex)

# zahnlose Teilnehmende entfernen
df2 <- df1 %>%
        filter(Zahnzahl_max28 != 0)

t.test(Zahnzahl_max28 ~ sex, data = df2) # t-Test: mittlere Zahnzahl zwischen Geschlechtern vergleichen

# wir testen nicht-parametrisch
# -----------------------------

wilcox.test(Zahnzahl_max28 ~ Geschlecht, data = df1) # Wilcoxon-Rangsummentest (Mann–Whitney-U-Test)

wilcox.test(Zahnzahl_max28 ~ Geschlecht, data = df1, alternative = "greater")

df1 %>%
  group_by(Geschlecht) %>%                        # nach Geschlecht gruppieren
  summarise(
    mdn = median(Zahnzahl_max28, na.rm = TRUE)    # Median berechnen
  )

# wir stratifizieren für Alter
# ----------------------------

ggplot(df1, aes(x = Alter_gerundet, y = Zahnzahl_max28, color = sex)) +
  geom_jitter(alpha = 0.4, width = 0.2) + # Punkte gestreut
  geom_smooth(method = "loess", se = TRUE, alpha = 0.25, linewidth = 1.2) + # geglättete Trendlinie pro Geschlecht
  labs(x = "Alter", y = "Zahnzahl (max 28)") +
  theme_minimal(base_size = 14)

median(df1$Alter_gerundet) # Median zu Einteilung der Altersgruppen

# neuer df für Altergruppen
df3 <- df1 %>%
          mutate(age = ifelse(Alter_gerundet > 50, 1, 0)) # neue Variable

# t-test für Alter ≤ 50
t.test(Zahnzahl_max28 ~ sex, data = subset(df3, age == 0))

# t-test für Alter > 50
t.test(Zahnzahl_max28 ~ sex, data = subset(df3, age == 1))

# was wäre wenn... (bitte zu Hause nicht nachmachen)
# -----------------------------------------------

median(df1$Zahnzahl_max28)

df4 <- df1 %>%
          mutate(zahn = ifelse(Zahnzahl_max28 > 21, 1, 0)) # neue Variable, Achtung: Skalenniveau wird reduziert

chisq.test(table(df4$zahn, df4$sex), correct = FALSE)



