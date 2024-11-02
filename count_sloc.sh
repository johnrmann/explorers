find ./ -not -path "./.git/*" -type f -exec wc -l {} + |
    awk '{print tolower($0)}' |
    sed -e '$ d' | 
    sed -e "s#/.*/##g" |
    sed -e "s/\./ \./g" |
    awk '
        { if ( NF <= 2 ) { count["none"] += $1 } else { count[$NF] += $1 } }
        { next }
        END { for (group in count) printf("%d%s%s\n", count[group], OFS, group) }
    ' |
    sort -n
