# source: https://jokergoo.github.io/circlize_book/book/
# https://www.data-to-viz.com/graph/chord.html
# (maybe) circos.ca/documentation/tutorials/ideograms/


library("circlize") # for circular layout
library("RColorBrewer") # for importing colors
library(ComplexHeatmap) # for legend


# ==============================================================


########################################################################
# It splits a given text into two parts. 
# This function is used for formatting long texts >> making 2-line displaying in the plot.
#
########################################################################
split.text.into.two.parts = function(x){
    pos = which(strsplit(x, "")[[1]]=="/")[1]
    if(is.na(pos))
        pos = which(strsplit(x, "")[[1]]==" ")[1]
        if(is.na(pos))  
            pos = nchar(x)/2
    parts = substring(x, c(1,pos), c(pos-1,nchar(x)));
    return(parts)
}



########################################################################
# It retrieves unique values of 'type_source'.
#
########################################################################
retrieve.group.names = function(events.filepath1, events.filepath2, events.filepath3){
    df.events1 = read.csv(file=events.filepath1, sep=";", header=T, check.names=F, stringsAsFactors=F)
    df.events2 = read.csv(file=events.filepath2, sep=";", header=T, check.names=F, stringsAsFactors=F)
    df.events3 = read.csv(file=events.filepath3, sep=";", header=T, check.names=F, stringsAsFactors=F)
    groups = unique(c(df.events1$Group1, df.events1$Group2, df.events2$Group1, df.events2$Group2, df.events3$Group1, df.events3$Group2))
    return(groups)
}



########################################################################
# It prepares the colors list for 'type_source'.
#
########################################################################
create.colors.group.association = function(groups){
    colors = brewer.pal(n = length(groups), name = "RdBu")
    colors = c(colors, "green", "cyan", "gray", "yellow") # extend the color list
    names(colors) = unique(groups)
    return(colors)
}




########################################################################
# Link 1: https://jokergoo.github.io/circlize_book/book/advanced-usage-of-chorddiagram.html#compare-two-chord-diagrams
# For comparability reasons, we need to adjust the segment heights of the second plot based on those of the first plot.
#   Unfortunately, we cannot use the solution proposed in Link1, because there is some overlaps between the first and second columns of our data frame.
#   That is why we need to do a manual calculation of the relative gap.
#
# The idea: we sum up all gap degrees between adjacent segments. If we substract this sum from 360, this gives us the total degree remained for the segments.
#   Let us have a = (the total degree remained for the segments of the first plot)/(the total degree remained for the segments of the second plot)
#   Let us also have b = (the total link weights in the first plot) / (the total link weights in the second plot)
#   Finally, the condition a = b must hold, for comparability reasons.
#
########################################################################
calculate.relative.big.gap = function(padiweb.links.csv.filepath, healthmap.links.csv.filepath, small.gap, big.gap){
    df.links.padiweb = read.csv(file=padiweb.links.csv.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)
    vars1.padiweb = df.links.padiweb[,"Var1"]
    names(vars1.padiweb) = df.links.padiweb[,"Group1"]
    vars2.padiweb = df.links.padiweb[,"Var2"]
    names(vars2.padiweb) = df.links.padiweb[,"Group2"]
    vars.padiweb = c(vars1.padiweb,vars2.padiweb)
    vars.padiweb = vars.padiweb[!duplicated(vars.padiweb)]

    df.links.healthmap = read.csv(file=healthmap.links.csv.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)
    vars1.healthmap = df.links.healthmap[,"Var1"]
    names(vars1.healthmap) = df.links.healthmap[,"Group1"]
    vars2.healthmap = df.links.healthmap[,"Var2"]
    names(vars2.healthmap) = df.links.healthmap[,"Group2"]
    vars.healthmap = c(vars1.healthmap,vars2.healthmap)
    vars.healthmap = vars.healthmap[!duplicated(vars.healthmap)]

    sum.weight.padiweb = sum(df.links.padiweb[,"value"])
    sum.weight.healthmap = sum(df.links.healthmap[,"value"])
    group.freq.padiweb = table(names(vars.padiweb))
    group.freq.healthmap = table(names(vars.healthmap))
    sum.gap.padiweb = sum(group.freq.padiweb - 1)*small.gap + length(group.freq.padiweb)*big.gap
    sum.gap.healthmap = sum(group.freq.healthmap - 1)*small.gap
    percent = sum.weight.healthmap / sum.weight.padiweb
    sum.tracks.padiweb = 360 - sum.gap.padiweb
    sum.tracks.healthmap = sum.tracks.padiweb * percent
    result = (360 - sum.tracks.healthmap - sum.gap.healthmap)/length(group.freq.healthmap)
    return(result)
}



########################################################################
# It prepares a specific csv file structure for plotting chord diagram, and writes into file.
#
########################################################################
prepare.input.for.chord.diagram = function(events.filepath, events.adjusted.filepath, links.filepath, year.of.interest, countries.of.interest, time.interval.col.name){

    df = read.csv(file=events.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)
    #df[,c(time.interval.col.name)] = df[,c(time.interval.col.name)] + 1 # because it starts from 0
    time_interval_values = sapply(df[,c(time.interval.col.name)], function(x) unlist(strsplit(x, "_"))[1]) # we remove the year value
    max_interval_no = max(as.integer(time_interval_values))

    df[which(df[,"region"] == ""),"region"] = paste0(df[which(df[,"region"] == ""),"country"], "-unknown")
    df[which(df[,"disease subtype"] == ""),"disease subtype"] = paste0(df[which(df[,"disease subtype"] == ""),"disease"], "-unknown")
    df[which(df[,"host subtype"] == ""),"host subtype"] = paste0(df[which(df[,"host subtype"] == ""),"host"], "-unknown")

    # ================================================================

    # ======================================================
    # Filtering data by geographic continents
    # ======================================================

    #some.asian.countries = c("Taiwan","India","China","Viet Nam","South Korea","Japan") # "Philippines","Hong Kong"
    if(length(countries.of.interest)>0){
        indxs = which(df[,"country_code"] %in% countries.of.interest)
        df = df[indxs,]
    }

    #df = df[which(df[,"disease"] == "AI"),]
    df = df[which(grepl("AI", df[,"disease"], fixed = TRUE)),]

    df = df[which(df[,"host"] == "bird"),]
    df = df[order(df[,"country"]),]
    if(!is.na(year.of.interest))
        df = df[which(df[,"year"] == year.of.interest),]

    # ================================================================
    # workaround for disease information
    df[,"disease subtype"] = df[, "disease"]
    df[,"disease"] = "AI"


    # ================================================================

    df1 = df[,c("region","disease subtype","country","disease",time.interval.col.name)]
    names(df1) = c("Var1", "Var2", "Group1", "Group2", time.interval.col.name)
    df2 = df[,c("region","host subtype","country","host", time.interval.col.name)]
    names(df2) = c("Var1", "Var2", "Group1", "Group2", time.interval.col.name)
    df = rbind(df1, df2)

    time.interval.simple.values = sapply(df[,c(time.interval.col.name)], function(x) unlist(strsplit(x, "_"))[1]) # we remove the year value
    year.values = sapply(df[,c(time.interval.col.name)], function(x) unlist(strsplit(x, "_"))[2]) # we remove the time interval value
    df[paste0(time.interval.col.name,"_simple")] = time.interval.simple.values
    df["year"] = year.values
    write.table(df, events.adjusted.filepath, sep=";", row.names=F, col.names=T)

    # ================================================================

    df.without.time = df[,c("Var1", "Var2", "Group1", "Group2")]
    # calculate the frequencies of the rows
    rows.collapsed = sapply(1:nrow(df.without.time), function(i) paste(df.without.time[i,],collapse=";"))
    freq.res = table(rows.collapsed)

    s = names(freq.res)
    s2 = lapply(1:length(s), function(i) c(unlist(strsplit(s[i],";")),freq.res[i]))
    df.links = as.data.frame(do.call(rbind, s2))
    names(df.links) = c("Var1", "Var2", "Group1", "Group2", "value")
    write.table(df.links[,c("Var1", "Var2", "Group1", "Group2", "value")], links.filepath, sep=";", row.names=F, col.names=T)
}







########################################################################
# It reads the csv file, and plots the chord diagram with grouping information.
#
########################################################################
create.chord.diagram = function(events.filepath, links.filepath, output.filepath, colors.for.groups, small.gap, big.gap, year.of.interest, time.interval.col.name){

    df.events = read.csv(file=events.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)
    df.links = read.csv(file=links.filepath, sep=";", header=T, check.names=F, stringsAsFactors=F)


    # --------------------------------------
    # create data frame for circos barplot
    # --------------------------------------

    df1 = df.events[,c("Var1", "Group1", time.interval.col.name)]
    names(df1) = c("Var", "Group", time.interval.col.name)
    df2 = df.events[,c("Var2", "Group2", time.interval.col.name)]
    names(df2) = c("Var", "Group", time.interval.col.name)
    df.time = rbind(df1, df2)

    # calculate the frequencies of the rows
    rows.collapsed = sapply(1:nrow(df.time), function(i) paste(df.time[i,],collapse=";"))
    freq.res = table(rows.collapsed)

    s = names(freq.res)
    s2 = lapply(1:length(s), function(i) c(unlist(strsplit(s[i],";")),freq.res[i]))
    df.time = as.data.frame(do.call(rbind, s2))
    names(df.time) = c("Var", "Group", time.interval.col.name, "value")
    #df.time[,c("week_no_simple")] = as.factor(df.time[,c("week_no_simple")])

    # prepare a matrix, where rows correspond to weeks and columns correspond to sectors

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
        } else if(time.interval.col.name == "month_no"){
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

    freq = table(df.time[,"Var"])
    #print(freq)
    most.freq.sector = names(freq[which.max(freq)])[1]
    most.freq.sector.group = df.time[which(df.time[,"Var"] == most.freq.sector)[1],"Group"]
    #print(most.freq.sector)
    #print(most.freq.sector.group)

    df.time = df.time[order(df.time[,"Group"],df.time[,"Var"]),]
    df.time.unique = unique(df.time[,c("Var","Group")])
    #print(df.time.unique)
    
    sectors = df.time.unique[,"Var"]
    sectors.group = df.time.unique[,"Group"]
    sector.for.y.annot = sectors[which(sectors.group == most.freq.sector.group)[1]]
    #print("!!!")
    #print(sectors)
    #print(sector.for.y.annot)
    nb.sectors = length(sectors)
    barplot.matrix = matrix(0, nb.intervals, nb.sectors)
    rownames(barplot.matrix) = intervals_label
    colnames(barplot.matrix) = sectors

    for(i in 1:nrow(df.time)){
        r = as.character(df.time[i,time.interval.col.name])
        c = as.character(df.time[i,"Var"])
        v = as.numeric(df.time[i,"value"])
        barplot.matrix[r,c] = v
    }
    # normalize the matrix values for circos barplot
    max.value = max(barplot.matrix)
    #barplot.matrix = barplot.matrix/max.value
    nb.bars = nrow(barplot.matrix)
    time_interval_values = sapply(intervals_label, function(x) as.integer(unlist(strsplit(x, "_"))[1])) # we remove the year value

    ########################################

    df1 = df.links[,c("Var1","Group1")]
    df2 = df.links[,c("Var2","Group2")]
    names(df1) = c("Var","Group")
    names(df2) = c("Var","Group")
    df.new = rbind(df1,df2)
    df.group = df.new[which(!duplicated(df.new)),c("Var","Group")]
    df.group = df.group[order(df.group[,"Group"],df.group[,"Var"]),]
    group = structure(df.group$Group, names = df.group$Var)
    #colors = brewer.pal(n = length(unique(df.group$Group)), name = "RdBu")
    #names(colors) = unique(df.group$Group)
    #colors = c("#B2182B", "#D6604D", "#F4A582", "#FDDBC7", "#D1E5F0", "#92C5DE", "#4393C3", "#2166AC")
    #names(colors) = c("Vietnam", "China", "Japan", "India", "South Korea", "Taiwan", "bird", "Avian Influenza")
    grid.col.for.group = colors.for.groups[df.group$Group]
    names(grid.col.for.group) = df.group$Var

    #print(group)


    pdf(output.filepath) 

    #chordDiagram(df.links[,c("Var1","Var2","value")], group = group,  grid.col = grid.col, preAllocateTracks = 2)
    chordDiagram(df.links[,c("Var1","Var2","value")], group = group,  grid.col = grid.col.for.group, preAllocateTracks = list(list(track.height = 0.2), list(track.height = 0.1),list(track.height = 0.05)), annotationTrack = "grid", small.gap = small.gap, big.gap = big.gap)
    circos.track(track.index = 1, panel.fun = function(x, y) {
        circos.text(CELL_META$xcenter, CELL_META$ylim[1], CELL_META$sector.index, col = "black", cex=0.6,
                    # facing = "bending.inside", niceFacing = TRUE,
                    facing = "clockwise", niceFacing = TRUE, adj = c(0, 0.5)
    )

    }, bg.border = NA) # here set bg.border to NA is important
    
    for(s in sectors){
        circos.track(sectors = s, track.index = 2, ylim = c(0, max.value), panel.fun = function(x, y) {
            if(s == most.freq.sector){
                length.out.coef = 1
                if(is.na(year.of.interest))
                    length.out.coef = 3 # in the data, we have 3 diff values: 2019, 2020, 2021
                tick.values = time_interval_values[seq(from=1,to=nb.bars,length.out=12*length.out.coef)]
                tick.pos = seq(from=CELL_META$cell.xlim[1]+0.1, to=CELL_META$cell.xlim[2]-0.1, length.out=nb.bars)[seq(from=1,to=nb.bars,length.out=12*length.out.coef)]
                circos.xaxis(sector.index = s, h="top", labels.cex = 0.25, major.at = tick.pos, labels = tick.values, minor.ticks=0)
            }
            if(s == sector.for.y.annot){
                circos.yaxis(side="left", sector.index = s, labels.cex = 0.5)
            }
            value = barplot.matrix[,s]
            circos.barplot(value, pos = seq(from=CELL_META$cell.xlim[1]+0.1, to=CELL_META$cell.xlim[2]-0.1, length.out=nb.bars), bar_width = 0.02, col = "red", border = "red") # border = NA
        })
    }


    for(i in 1:length(df.group$Group)){
        g = df.group$Group[i]
        highlight.sector(sector.index = df.group$Var[which(df.group$Group == g)], track.index = 3, col = grid.col.for.group[i], text = g, cex = 0.8, text.col = "gray")
    }

    dev.off()

    circos.clear()

}




# main function
plot.chord.diagram.for.platforms <- function(padiweb.events.filepath, promed.events.filepath, empresi.events.filepath, out.folder, countries.of.interest, year.of.interest, time.interval.col.name){

    out.padiweb.folder = file.path(out.folder, "padiweb")
    if(!dir.exists(out.padiweb.folder))
        dir.create(out.padiweb.folder, recursive=T)

    out.promed.folder = file.path(out.folder, "promed")
    if(!dir.exists(out.promed.folder))
        dir.create(out.promed.folder, recursive=T)

    out.empresi.folder = file.path(out.folder, "empres-i")
    if(!dir.exists(out.empresi.folder))
        dir.create(out.empresi.folder, recursive=T)

    out.padiweb.promed.folder = file.path(out.folder, "padiweb_vs_promed")
    if(!dir.exists(out.padiweb.promed.folder))
        dir.create(out.padiweb.promed.folder, recursive=T)

    out.padiweb.empresi.folder = file.path(out.folder, "padiweb_vs_empres-i")
    if(!dir.exists(out.padiweb.empresi.folder))
        dir.create(out.padiweb.empresi.folder, recursive=T)

    out.promed.empresi.folder = file.path(out.folder, "promed_vs_empres-i")
    if(!dir.exists(out.promed.empresi.folder))
        dir.create(out.promed.empresi.folder, recursive=T)

    padiweb.events.adjusted.filepath = file.path(out.padiweb.folder, paste0("padiweb_events_adjusted_",year.of.interest,".csv"))
    padiweb.links.filepath = file.path(out.padiweb.folder, paste0("padiweb_links_",year.of.interest,".csv"))
    
    promed.events.adjusted.filepath = file.path(out.promed.folder, paste0("promed_events_adjusted_",year.of.interest,".csv"))
    promed.links.filepath = file.path(out.promed.folder, paste0("promed_links_",year.of.interest,".csv"))

    empresi.events.adjusted.filepath = file.path(out.empresi.folder, paste0("empres-i_events_adjusted_",year.of.interest,".csv"))
    empresi.links.filepath = file.path(out.empresi.folder, paste0("empres-i_links_",year.of.interest,".csv"))



    prepare.input.for.chord.diagram(padiweb.events.filepath, padiweb.events.adjusted.filepath, padiweb.links.filepath, year.of.interest, countries.of.interest, time.interval.col.name) # it creates 'padiweb.links.filepath'

    prepare.input.for.chord.diagram(promed.events.filepath, promed.events.adjusted.filepath, promed.links.filepath, year.of.interest, countries.of.interest, time.interval.col.name) # it creates 'promed.links.filepath'

    prepare.input.for.chord.diagram(empresi.events.filepath, empresi.events.adjusted.filepath, empresi.links.filepath, year.of.interest, countries.of.interest, time.interval.col.name) # it creates 'empresi.links.filepath'

    groups = retrieve.group.names(padiweb.events.adjusted.filepath, promed.events.adjusted.filepath, empresi.events.adjusted.filepath)
    colors.for.group = create.colors.group.association(groups)


    # ==============
    # padiweb only
    # ==============
    padiweb.output.filepath = file.path(out.padiweb.folder, paste0("padiweb_events_",year.of.interest,".pdf"))
    small.gap = 0.5
    big.gap = 4 # I know that there are a lot of entries for padiweb, so I put a small value of 'big.gap' for this plot
    create.chord.diagram(padiweb.events.adjusted.filepath, padiweb.links.filepath, padiweb.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)


    # ==============
    # promed only
    # ==============
    promed.output.filepath = file.path(out.promed.folder, paste0("promed_events_",year.of.interest,".pdf"))
    small.gap = 0.5
    big.gap = 4
    create.chord.diagram(promed.events.adjusted.filepath, promed.links.filepath, promed.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)



    # ==============
    # Empres-i only
    # ==============
    empresi.output.filepath = file.path(out.empresi.folder, paste0("empres-i_events_",year.of.interest,".pdf"))
    small.gap = 0.5
    big.gap = 4
    create.chord.diagram(empresi.events.adjusted.filepath, empresi.links.filepath, empresi.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)


    # ==============
    # padiweb vs promed
    # ==============
    padiweb.output.filepath = file.path(out.padiweb.promed.folder, paste0("padiweb_events_",year.of.interest,".pdf"))
    small.gap = 0.5
    big.gap = 4 # I know that there are a lot of entries for padiweb, so I put a small value of 'big.gap' for this plot
    create.chord.diagram(padiweb.events.adjusted.filepath, padiweb.links.filepath, padiweb.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)

    promed.output.filepath = file.path(out.padiweb.promed.folder, paste0("promed_events_",year.of.interest,".pdf"))
    ## For comparability reasons, we need to calculate the relative gap, which becomes 'big.gap' in the second plot
    ##   Note that, small.gap should be the same for both cases
    rel.gap = calculate.relative.big.gap(padiweb.links.filepath, promed.links.filepath, small.gap, big.gap)
    big.gap = rel.gap
    if(big.gap>0)
        create.chord.diagram(promed.events.adjusted.filepath, promed.links.filepath, promed.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)



    # ==============
    # empres-i vs padiweb
    # ==============
    empresi.output.filepath = file.path(out.padiweb.empresi.folder, paste0("empres-i_events_",year.of.interest,".pdf"))
    small.gap = 0.5
    big.gap = 4
    create.chord.diagram(empresi.events.adjusted.filepath, empresi.links.filepath, empresi.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)

    padiweb.output.filepath = file.path(out.padiweb.empresi.folder, paste0("padiweb_events_",year.of.interest,".pdf"))
    ## For comparability reasons, we need to calculate the relative gap, which becomes 'big.gap' in the second plot
    ##   Note that, small.gap should be the same for both cases
    rel.gap = calculate.relative.big.gap(empresi.links.filepath, padiweb.links.filepath, small.gap, big.gap)
    big.gap = rel.gap
    if(big.gap>0)
        create.chord.diagram(padiweb.events.adjusted.filepath, padiweb.links.filepath, padiweb.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)



    # ==============
    # empres-i vs promed
    # ==============
    empresi.output.filepath = file.path(out.promed.empresi.folder, paste0("empres-i_events_",year.of.interest,".pdf"))
    small.gap = 0.5
    big.gap = 4
    create.chord.diagram(empresi.events.adjusted.filepath, empresi.links.filepath, empresi.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)

    promed.output.filepath = file.path(out.promed.empresi.folder, paste0("promed_events_",year.of.interest,".pdf"))
    ## For comparability reasons, we need to calculate the relative gap, which becomes 'big.gap' in the second plot
    ##   Note that, small.gap should be the same for both cases
    rel.gap = calculate.relative.big.gap(empresi.links.filepath, promed.links.filepath, small.gap, big.gap)
    big.gap = rel.gap
    if(big.gap>0)
        create.chord.diagram(promed.events.adjusted.filepath, promed.links.filepath, promed.output.filepath, colors.for.group, small.gap, big.gap, year.of.interest, time.interval.col.name)

}







## filtering
#year.of.interest = "2020"
##year.of.interest = NA
#countries.of.interest = c("TW","IN","CH","VN","KR","JP")
##countries.of.interest = c("TW","CH","VN")
#time.interval.col.name = "week_no"
##time.interval.col.name = "month_no"
#
#
#csv.folder = "/home/nejat/eclipse/tetis/compebs/in/events"
#out.folder = "/home/nejat/eclipse/tetis/compebs/out/circos"
#
#padiweb.events.filepath = file.path(csv.folder, "padiweb", "events_simplified.csv")
#promed.events.filepath = file.path(csv.folder, "promed", "events_simplified.csv")
#empresi.events.filepath = file.path(csv.folder, "empres-i", "events_simplified.csv")
#
#plot.chord.diagram.for.platforms(padiweb.events.filepath, promed.events.filepath, empresi.events.filepath, out.folder, countries.of.interest, year.of.interest, time.interval.col.name)


args = commandArgs(trailingOnly=TRUE)

#print(length(args))
if (length(args)==0) {
  stop("Seven arguments must be supplied .n", call.=FALSE)
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


#args1: padiweb.event.filepath
#args2: promed.event.filepath
#args3: empresi.event.filepath
#args4: output.folder
#args5: countries.of.interest
#args6: year.of.interest
#args7: time.interval.col.name


countries.of.interest = unlist(strsplit(args[5], ","))
year.of.interest = args[6]
if(year.of.interest == "-1"){
    year.of.interest = NA
}
#print(countries.of.interest)
#print(args[7])
plot.chord.diagram.for.platforms(args[1], args[2], args[3], args[4], countries.of.interest, year.of.interest, args[7])

# Rscript complexheatmap_AI.R "/home/nejat/eclipse/tetis/compebs/in/events/padiweb/events_simplified.csv" "/home/nejat/eclipse/tetis/compebs/in/events/promed/events_simplified.csv" "/home/nejat/eclipse/tetis/compebs/in/events/empres-i/events_simplified.csv" "/home/nejat/eclipse/tetis/compebs/out/circos" "CHN,VNM,KOR" "-1" "biweek_no"




