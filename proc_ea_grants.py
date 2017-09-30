#!/usr/bin/env python3
# License: CC0

# To get the data, go to
# https://docs.google.com/spreadsheets/d/1iBy--zMyIiTgybYRUQZIm11WKGQZcixaCmIaysRmGvk/edit?usp=sharing
# and export as TSV, saving the file as "ea-grants.tsv".

import csv
import logging


logging.basicConfig(level=logging.DEBUG)


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source.
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


print("""insert into donations(donor, donee, amount, fraction, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url, notes,
    payment_modality, match_eligible, goal_amount, influencer, employer_match,
    matching_employer, amount_original_currency, original_currency,
    currency_conversion_date, currency_conversion_basis) values""")

with open("ea-grants.tsv", newline='') as f:
    reader = csv.DictReader(f, delimiter="\t")
    first = True
    for row in reader:
        print("    " + ("" if first else ",") + "(" + ",".join([
            mysql_quote("Centre for Effective Altruism"),
            mysql_quote(row['Recipient']),
            "NULL",
            "NULL",
            "NULL",  # donation_date
            "NULL",  # donation_date_precision
            "NULL",  # donation_date_basis
            mysql_quote(row['Cause']),
            "NULL",  # url
            mysql_quote(row['Project']),  # notes
            "NULL",  # payment_modality
            "NULL",  # match_eligible
            "NULL",  # goal_amount
            "NULL",  # influencer
            "NULL",  # employer_match
            "NULL",  # matching_employer
            row['Amount'].replace('£', '') \
                         .replace(',', ''),  # amount_original_currency
            mysql_quote("GBP"),  # original_currency
            "NULL",  # currency_conversion_date
            "NULL",  # currency_conversion_basis
        ]) + ")")
        first = False
print(";")
