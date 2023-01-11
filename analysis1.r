df1 <- read.csv('~/PPL_work/alignment/emo_survey/data_analysis_etc/data/generated/aestheticRatings_v2.csv')
df2 <- read.csv('~/PPL_work/alignment/emo_survey/data_analysis_etc/data/generated/longdata_v4.csv')

lm1 <- lm("rating~model*gender", df1) 

Mode <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}

genders1 <- aggregate(df1$gender, list(df1$participantID), Mode)
genders2 <- aggregate(df2$gender, list(df2$participantID), Mode)
genders <- rbind(genders1, genders2)

ages1 <- aggregate(df1$age, list(df1$participantID), Mode)
ages2 <- aggregate(df2$age, list(df2$participantID), Mode) 
ages <- rbind(ages1, ages2)

print (mean(ages$x))
print (sd(ages$x))

print (anova(aov(lm1)))