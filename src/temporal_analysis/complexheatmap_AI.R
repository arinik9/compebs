#!/usr/bin/env Rscript


library(ComplexHeatmap) # for legend
library(circlize)



# load the clusters
load.clustering <- function(clustering.filepath) {
    df = read.csv(clustering.filepath, header=F)
    clusters = lapply(df$V1, function(cluster_info) as.integer(unlist(strsplit(cluster_info, ","))))
    return(clusters)
}

# sort the cluster in chronological order
sort.clusters.by.chronological.order <- function(clusters, df) {
    nb.clusters = length(clusters)
    assoc.year.vals = rep("-1", nb.clusters)
    for(j in seq(1,nb.clusters)){
        clu = clusters[[j]]
        df.sub = df[which(df[,"id"] %in% clu),]
        if(nrow(df.sub)>0){
            assoc.year.vals[j] = df.sub[1,"time_interval_no"] #get the time entry of the first element
        }
    }

    # sort in chronological order
    year.vals.in.labels = sapply(assoc.year.vals, function(x) as.integer(unlist(strsplit(x, "_"))[2]))
    names(year.vals.in.labels) = NULL
    time.int.vals.in.labels = sapply(assoc.year.vals, function(x) as.integer(unlist(strsplit(x, "_"))[1]))
    names(time.int.vals.in.labels) = NULL
    sorted.indxs = order(year.vals.in.labels, time.int.vals.in.labels)
    sorted.clusters = clusters[sorted.indxs]
    #print(assoc.year.vals[sorted.indxs])
    return(sorted.clusters)
}

# filter
filter.clustering.by.selected.countries.and.year <- function(clusters, df, countries.of.interest, year.of.interest) {
    new.clusters = list()
    nb.clusters = length(clusters)
    counter = 0
    for(j in seq(1,nb.clusters)){
        clu = clusters[[j]]
        df.sub = df[which(df[,"id"] %in% clu),]
        if(nrow(df.sub)>0){
            country_code = df.sub[1,"loc_country_code"] # get the first one, since all the elements of a cluster must associate with the same country
            is.year.included = TRUE
            if(!is.na(year.of.interest)) 
                is.year.included = any(df.sub[,"year"] == year.of.interest)
            if(country_code %in% countries.of.interest && is.year.included){
                counter = counter + 1
                new.clusters[[counter]] = clu
            }
        }
    }
    return(new.clusters)
}








# main function
plot.event.evolution.for.platforms <- function(padiweb.event.filepath, promed.event.filepath, empresi.event.filepath, padiweb.clustering.filepath, promed.clustering.filepath, output.filepath, countries.of.interest, year.of.interest, time.interval.col.name){
    
    # ==================================================================================================
    df = read.csv(padiweb.event.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)
    df.padiweb = df[,c("id",time.interval.col.name,"year","loc_country_code")]
    df.padiweb[,"source"] = "padiweb"
    df.padiweb[,"time_interval_no"] = paste0(df.padiweb[,time.interval.col.name], "_", df.padiweb[,"year"])
    #df.padiweb[,"clustering"] = paste0("pw", gsub("c", "",df.padiweb[,"clustering"]))

    df = read.csv(promed.event.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)
    df.promed = df[,c("id",time.interval.col.name,"year","loc_country_code")]
    df.promed[,"source"] = "promed"
    df.promed[,"time_interval_no"] = paste0(df.promed[,time.interval.col.name], "_", df.promed[,"year"])
    #df.promed[,"clustering"] = paste0("pm", gsub("c", "",df.promed[,"clustering"]))

    df = read.csv(empresi.event.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)
    df.empresi = df[,c("id",time.interval.col.name,"year","loc_country_code")]
    df.empresi = df.empresi[which(df.empresi[,"year"] %in% c(2019, 2020, 2021)),]
    df.empresi[,"id"] = seq(1,nrow(df.empresi))
    df.empresi[,"source"] = "empres-i"
    df.empresi[,"time_interval_no"] = paste0(df.empresi[,time.interval.col.name], "_", df.empresi[,"year"])
    #df.empresi[,"clustering"] = paste0("ei", gsub("c", "",df.empresi[,"clustering"]))

    # handle clustering
    clusters.padiweb = load.clustering(padiweb.clustering.filepath)
    clusters.padiweb = filter.clustering.by.selected.countries.and.year(clusters.padiweb, df.padiweb, countries.of.interest, year.of.interest)
    clusters.padiweb = sort.clusters.by.chronological.order(clusters.padiweb, df.padiweb)
    nb.clusters.padiweb = length(clusters.padiweb)
    # --
    clusters.promed = load.clustering(promed.clustering.filepath)
    clusters.promed = filter.clustering.by.selected.countries.and.year(clusters.promed, df.promed, countries.of.interest, year.of.interest)
    clusters.promed = sort.clusters.by.chronological.order(clusters.promed, df.promed)
    nb.clusters.promed = length(clusters.promed)
    # --
    clusters.empresi = lapply(seq(1,nrow(df.empresi)), function(x) x) # each event is in a separate cluster
    clusters.empresi = filter.clustering.by.selected.countries.and.year(clusters.empresi, df.empresi, countries.of.interest, year.of.interest)
    clusters.empresi = sort.clusters.by.chronological.order(clusters.empresi, df.empresi)
    nb.clusters.empresi = length(clusters.empresi)
    # --
    nb.clusters.total = nb.clusters.padiweb + nb.clusters.promed + nb.clusters.empresi

    # ==================================================================================================


    df = rbind(df.padiweb, df.promed, df.empresi)


    if(length(countries.of.interest)>0){
        df = df[which(df[,"loc_country_code"] %in% countries.of.interest),]
    }

    if(!is.na(year.of.interest)){
        df = df[which(df[,"year"] == year.of.interest),]
    }

    df = df[order(df[,"loc_country_code"]),]

    # by default: we prepare the time intervals for the whole data 
    intervals_label = c(paste0(seq(1,52), "_", "2019"), paste0(seq(1,53), "_", "2020"), paste0(seq(1,53), "_", "2021")) # default: by week
    if(time.interval.col.name == "biweek_no"){
        intervals_label = c(paste0(seq(1,26), "_", "2019"), paste0(seq(1,27), "_", "2020"), paste0(seq(1,27), "_", "2021")) # default: by week
    } else if(time.interval.col.name == "month_no"){
        intervals_label = c(paste0(seq(1,12), "_", "2019"), paste0(seq(1,12), "_", "2020"), paste0(seq(1,12), "_", "2021")) # default: by week
    }

    if(!is.na(year.of.interest) && year.of.interest == "2019"){
        intervals_label = paste0(seq(1,52), "_", "2019") # default: by week
        if(time.interval.col.name == "biweek_no"){
            intervals_label = paste0(seq(1,26), "_", "2019")
        } else if(time.interval.col.name == "month_no"){
            intervals_label = paste0(seq(1,12), "_", "2019")
        }
    } else if(!is.na(year.of.interest) && year.of.interest == "2020"){
        intervals_label = paste0(seq(1,53), "_", "2020") # default: by week
        if(time.interval.col.name == "biweek_no"){
            intervals_label = paste0(seq(1,27), "_", "2020")
        } else if(time.interval.col.nameE == "month_no"){
            intervals_label = paste0(seq(1,12), "_", "2020")
        }
    } else if(!is.na(year.of.interest) && year.of.interest == "2021"){
        intervals_label = paste0(seq(1,53), "_", "2021") # default: by week
        if(time.interval.col.name == "biweek_no"){
            intervals_label = paste0(seq(1,27), "_", "2021")
        } else if(time.interval.col.name == "month_no"){
            intervals_label = paste0(seq(1,12), "_", "2021")
        }
    }

    nb.intervals = length(intervals_label)

    nb.intervals = length(intervals_label)
    mat = matrix(0, nb.intervals, nb.clusters.total)
    rownames(mat) = intervals_label
    colnames(mat) = c(paste0("pw", seq(1, nb.clusters.padiweb)), paste0("pm", seq(1, nb.clusters.promed)),  paste0("ei", seq(1, nb.clusters.empresi)))

    country.assoc.padiweb = rep("-1", nb.clusters.padiweb)
    for(j in seq(1,nb.clusters.padiweb)){
        clu = clusters.padiweb[[j]]
        df.sub = df[which((df[,"id"] %in% clu) & (df[,"source"] == "padiweb")),]
        if(nrow(df.sub)>0){
            country.assoc.padiweb[j] = df.sub[1,"loc_country_code"] # get the first one, since all the elements of a cluster must associate with the same country
            for(i in 1:nrow(df.sub)){
                r = paste0(as.character(df.sub[i,"time_interval_no"]))
                c = paste0("pw",j)
                #mat[r,c] = mat[r,c] + 1
                if(mat[r,c] == 0){
                    mat[r,c] = 1
                }
            }
        }
    }

    country.assoc.promed = rep("-1", nb.clusters.promed)
    for(j in seq(1,nb.clusters.promed)){
        clu = clusters.promed[[j]]
        df.sub = df[which((df[,"id"] %in% clu) & (df[,"source"] == "promed")),]
        if(nrow(df.sub)>0){
            country.assoc.promed[j] = df.sub[1,"loc_country_code"] # get the first one, since all the elements of a cluster must associate with the same country
            for(i in 1:nrow(df.sub)){
                r = paste0(as.character(df.sub[i,"time_interval_no"]))
                c = paste0("pm",j)
                #mat[r,c] = mat[r,c] + 1
                if(mat[r,c] == 0){
                    mat[r,c] = 1
                }
            }
        }
    }

    country.assoc.empresi = rep("-1", nb.clusters.empresi)
    for(j in seq(1,nb.clusters.empresi)){
        clu = clusters.empresi[[j]]
        df.sub = df[which((df[,"id"] %in% clu) & (df[,"source"] == "empres-i")),]
        if(nrow(df.sub)>0){
            country.assoc.empresi[j] = df.sub[1,"loc_country_code"] # get the first one, since all the elements of a cluster must associate with the same country
            for(i in 1:nrow(df.sub)){
                r = paste0(as.character(df.sub[i,"time_interval_no"]))
                c = paste0("ei",j)
                #mat[r,c] = mat[r,c] + 1
                if(mat[r,c] == 0){
                    mat[r,c] = 1
                }
            }
        }
    }

    country.assoc = c(country.assoc.padiweb, country.assoc.promed, country.assoc.empresi)

    padiweb.columns.indexs = which(startsWith(colnames(mat), "pw"))
    for(i in padiweb.columns.indexs){
        zero.indexs = which(mat[,i] == 0)
        mat[zero.indexs,i] = -1
    }

    promed.columns.indexs = which(startsWith(colnames(mat), "pm"))
    for(i in promed.columns.indexs){
        zero.indexs = which(mat[,i] == 0)
        mat[zero.indexs,i] = -2
    }

    empresi.columns.indexs = which(startsWith(colnames(mat), "ei"))
    for(i in empresi.columns.indexs){
        zero.indexs = which(mat[,i] == 0)
        mat[zero.indexs,i] = -3
    }

    col_fun = colorRamp2(c(-3, -2, -1, max(mat)), c("lightyellow1", "#F0F0F0", "snow1", "rosybrown3"))

    #print(output.filepath)
    pdf(file=output.filepath, width=35, height=14, compress=FALSE)


    column_orders = seq(1, length(colnames(mat))) # order(as.numeric(gsub("pm", "", gsub("pw", "", colnames(mat)))))
    row_orders = seq(1, length(intervals_label))

    plot <- Heatmap(mat, name = "frequencies", col = col_fun, column_split = country.assoc, column_gap = unit(5, "mm"), column_order = column_orders, row_order = row_orders, show_row_dend = FALSE, show_column_dend = FALSE, column_title_rot = 90, show_column_names=FALSE, show_heatmap_legend = FALSE)
    print(plot)
    dev.off()

}

# ==================================================================================================












##COUNTRIES.OF.INTEREST = NA
#COUNTRIES.OF.INTEREST = c("CHN", "VNM", "KOR") # >> ASIA
## COUNTRIES.OF.INTEREST = c("TWN","IND","CHN","VNM","KOR","JAP") # "PHL","HKG" >> ASIA
## COUNTRIES.OF.INTEREST = c("DNK","POL","CHE","ROU","GBR","DEU","BGR","NLD","FRA","ESP","ITA") # >> EUROPE
#YEAR.OF.INTEREST = NA
##YEAR.OF.INTEREST = "2021"
##TIME.INTERVAL.COL.NAME = "week_no"
#TIME.INTERVAL.COL.NAME = "biweek_no"
##TIME.INTERVAL.COL.NAME = "month_no"

#csv.folder = "/home/nejat/eclipse/tetis/compebs/in/events"
#out.folder = "/home/nejat/eclipse/tetis/compebs/out/heatmap"


#output.filepath = file.path(out.folder, "empresi_padiweb_promed_heatmap.pdf")
#padiweb.event.filepath = file.path(csv.folder, "padiweb", "event_candidates.csv")
#promed.event.filepath = file.path(csv.folder, "promed", "event_candidates.csv")
#empresi.event.filepath = file.path(csv.folder, "empres-i", "events.csv")
#padiweb.clustering.filepath = file.path(csv.folder, "padiweb", "event-clustering.txt")
#promed.clustering.filepath = file.path(csv.folder, "promed", "event-clustering.txt")



args = commandArgs(trailingOnly=TRUE)

#print(length(args))
if (length(args)==0) {
  stop("Nine arguments must be supplied .n", call.=FALSE)
} 

if(!dir.exists(args[6]))
    dir.create(args[6], recursive=T)

if (!file.exists(args[1])) {
  stop("PADI-Web event file cannot be open .n", call.=FALSE)
} 

if (!file.exists(args[2])) {
  stop("ProMED event file cannot be open .n", call.=FALSE)
}

if (!file.exists(args[3])) {
  stop("Empres-i event file cannot be open .n", call.=FALSE)
}

if (!file.exists(args[4])) {
  stop("PADI-Web event clustering file cannot be open .n", call.=FALSE)
}

if (!file.exists(args[5])) {
  stop("ProMED event clustering file cannot be open .n", call.=FALSE)
}

#args1: padiweb.event.filepath
#args2: promed.event.filepath
#args3: empresi.event.filepath
#args4: padiweb.clustering.filepath
#args5: promed.clustering.filepath
#args6: output.folder
#args7: countries.of.interest
#args8: year.of.interest
#args9: time.interval.col.name

output.filepath = file.path(args[6], "empresi_padiweb_promed_heatmap.pdf")
countries.of.interest = unlist(strsplit(args[7], ","))
year.of.interest = args[8]
if(year.of.interest == "-1"){
    year.of.interest = NA
}
#print(countries.of.interest)
#print(args[9])
plot.event.evolution.for.platforms(args[1], args[2], args[3], args[4], args[5], output.filepath, countries.of.interest, year.of.interest, args[9])

# Rscript complexheatmap_AI.R "/home/nejat/eclipse/tetis/compebs/in/events/padiweb/event_candidates.csv" "/home/nejat/eclipse/tetis/compebs/in/events/promed/event_candidates.csv" "/home/nejat/eclipse/tetis/compebs/in/events/empres-i/events.csv" "/home/nejat/eclipse/tetis/compebs/in/events/padiweb/event-clustering.txt" "/home/nejat/eclipse/tetis/compebs/in/events/promed/event-clustering.txt" "/home/nejat/eclipse/tetis/compebs/out/heatmap" "CHN,VNM,KOR" "-1" "biweek_no"


