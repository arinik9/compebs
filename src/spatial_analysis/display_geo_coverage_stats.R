

df1 = read.csv("/home/nejat/eclipse/tetis/compebs/out/spatial_analysis/spatiotemporal_representativeness/padiweb_vs_empres-i/Z=country_T=month_no/final_temporal_geo_coverage_platform=padiweb_vs_empres-i_country_month_no.csv", sep=";")
df1 = df1[!is.null(df1[,"temporal_geo_coverage"]),]


df2 = read.csv("/home/nejat/eclipse/tetis/compebs/out/spatial_analysis/spatiotemporal_representativeness/promed_vs_empres-i/Z=country_T=month_no/final_temporal_geo_coverage_platform=promed_vs_empres-i_country_month_no.csv", sep=";")
df2 = df2[!is.null(df2[,"temporal_geo_coverage"]),]


#print("------- 1 vs 1 -------")
#
#indxs.score1.df1 = which(df1[,"temporal_geo_coverage"] == 1)
#print(length(indxs.score1.df1))
#
#indxs.score1.df2 = which(df2[,"temporal_geo_coverage"] == 1)
#print(length(indxs.score1.df2))
#
#common.indxs = intersect(indxs.score1.df1, indxs.score1.df2)
#print(df1[common.indxs,"geonameId"])
#print(length(common.indxs))



print("------- sup0 of padiweb vs sup0 of promed -------")

indxs.score1.df1 = which(df1[,"temporal_geo_coverage"] > 0)
print(length(indxs.score1.df1))

indxs.score1.df2 = which(df2[,"temporal_geo_coverage"] > 0)
print(length(indxs.score1.df2))

common.indxs = intersect(indxs.score1.df1, indxs.score1.df2)
print(df1[common.indxs,"geonameId"])
print(length(common.indxs))



print("------- only padiweb has 1 -------")

diff.indxs = setdiff(indxs.score1.df1, indxs.score1.df2)
print(df1[diff.indxs,"geonameId"])
print(length(diff.indxs))

print("------- only promed has 1 -------")

diff.indxs = setdiff(indxs.score1.df2, indxs.score1.df1)
print(df1[diff.indxs,"geonameId"])
print(length(diff.indxs))


print("------- 0 vs 0 -------")

indxs.score0.df1 = which(df1[,"temporal_geo_coverage"] == 0)
indxs.score0.df2 = which(df2[,"temporal_geo_coverage"] == 0)

common.indxs = intersect(indxs.score0.df1, indxs.score0.df2)
print(df1[common.indxs,"geonameId"])
print(length(common.indxs))



# ========================================================================

indxs.score.sup0.df1 = which(df1[,"temporal_geo_coverage"] > 0)
print(length(indxs.score.sup0.df1))

indxs.score.sup0.df2 = which(df2[,"temporal_geo_coverage"] > 0)
print(length(indxs.score.sup0.df1))


print("------- sup0 of padiweb vs 0 of promed -------")

common.indxs = intersect(indxs.score.sup0.df1, indxs.score0.df2)
print(df1[common.indxs,"geonameId"])
print(length(common.indxs))


print("------- sup0 of promed vs 0 of padiweb -------")

common.indxs = intersect(indxs.score.sup0.df2, indxs.score0.df1)
print(df1[common.indxs,"geonameId"])
print(length(common.indxs))
