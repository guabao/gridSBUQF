#!/bin/sh
# A filter that select important rows in original trades file and save them as csv file

process()
{
	cat $1 | awk -F "|" '{print $1,$2,$3,$5,$6}' > $2
}

process $1 $2


