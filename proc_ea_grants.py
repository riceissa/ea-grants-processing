#!/usr/bin/env python3
# License: CC0

# To get the data, go to
# https://docs.google.com/spreadsheets/d/1iBy--zMyIiTgybYRUQZIm11WKGQZcixaCmIaysRmGvk/edit?usp=sharing
# and export as TSV, saving the file as "ea-grants.tsv". You will want to
# remove the last line, which contains the total amount.

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
        amount_original = float(row['Amount'].replace('£', '').replace(',', ''))
        # Conversion rate from
        # https://www.bloomberg.com/quote/GBPUSD:CUR and archived at
        # http://archive.is/GFfq6
        amount = round(amount_original * 1.3398, 2)
        notes = row['Project'] + " See http://effective-altruism.com/ea/1fc/effective_altruism_grants_project_update/ for more context about the grant program."
        print("    " + ("" if first else ",") + "(" + ",".join([
            mysql_quote("Effective Altruism Grants"),
            mysql_quote(row['Recipient']),
            str(amount),
            "NULL",
            mysql_quote("2017-09-29"),  # donation_date
            mysql_quote("day"),  # donation_date_precision
            mysql_quote("date of donation announcement"),  # donation_date_basis
            mysql_quote(row['Cause']),
            mysql_quote("https://docs.google.com/spreadsheets/d/1iBy--zMyIiTgybYRUQZIm11WKGQZcixaCmIaysRmGvk"),  # url
            mysql_quote(notes),  # notes
            "NULL",  # payment_modality
            "NULL",  # match_eligible
            "NULL",  # goal_amount
            "NULL",  # influencer
            "NULL",  # employer_match
            "NULL",  # matching_employer
            str(amount_original),  # amount_original_currency
            mysql_quote("GBP"),  # original_currency
            mysql_quote("2017-09-29"),  # currency_conversion_date
            mysql_quote("Bloomberg"),  # currency_conversion_basis
        ]) + ")")
        first = False
print(";")
