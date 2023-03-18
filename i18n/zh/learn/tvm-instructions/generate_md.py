import argparse
import csv
import re
import sys

parser = argparse.ArgumentParser(description="Generate TVM instruction reference document")
parser.add_argument("instructions_csv", type=str, help="csv file with the instructions")
parser.add_argument("doc_template", type=str, help="template for the document")
parser.add_argument("out_file", type=str, help="output file")
args = parser.parse_args()

TABLE_HEADER = \
        "| xxxxxxx<br>Opcode " +\
        "| xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br>Fift syntax " +\
        "| xxxxxxxxxxxxxxxxx<br>Stack " +\
        "| xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br>Description " +\
        "| xxxx<br>Gas |\n" +\
        "|:-|:-|:-|:-|:-|"

categories = dict()
cmd_to_name = dict()

with open(args.instructions_csv, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat = row["doc_category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(row)
        if row["name"] != "":
            for s in row["doc_fift"].split("\n"):
                s = s.strip()
                if s != "":
                    s = s.split()[-1]
                    if s not in cmd_to_name:
                        cmd_to_name[s] = row["name"]

def name_to_id(s):
    return "instr-" + s.lower().replace("_", "-").replace("#", "SHARP")

def make_link(text, cmd):
    if cmd not in cmd_to_name:
        return text
    name = cmd_to_name[cmd]
    return "[%s](#%s)" % (text, name_to_id(name))

def gen_links(text):
    return re.sub("`([^ `][^`]* )?([A-Z0-9#-]+)`", lambda m: make_link(m.group(0), m.group(2)), text)

def make_table(cat):
    if cat not in categories:
        print("No such category", cat, file=sys.stderr)
        return ""
    table = [TABLE_HEADER]
    for row in categories[cat]:
        opcode = row["doc_opcode"]
        fift = row["doc_fift"]
        stack = row["doc_stack"]
        desc = row["doc_description"]
        gas = row["doc_gas"]

        if opcode != "":
            opcode = "**`%s`**" % opcode

        if fift != "":
            fift = "<br>".join("`%s`" % s.strip() for s in fift.split("\n"))

        if stack != "":
            stack = "_`%s`_" % stack
            stack = stack.replace("|", "\\|")
            stack = stack.strip()

        desc = desc.replace("|", "\\|")
        desc = desc.replace("\n", "<br>")

        if gas != "":
            gas = gas.replace("|", "\\|")
            gas = "`" + gas + "`"

        desc = gen_links(desc)
        desc = "<div id='%s'>" % name_to_id(row["name"]) + desc

        table.append("| %s | %s | %s | %s | %s |" % (opcode, fift, stack, desc, gas))

    return "\n".join(table)

templ = open(args.doc_template, "r").read()

templ = gen_links(templ)

doc = re.sub("{{ *Table: *([a-zA-Z0-9_-]+) *}}", lambda m: make_table(m.group(1)), templ)
with open(args.out_file, "w") as f:
    print(doc, file=f)
