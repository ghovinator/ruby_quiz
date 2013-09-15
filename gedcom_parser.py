#! /usr/bin/python
from optparse import OptionParser

def format_data(fileline):
    fileline = fileline.split()
    return int(fileline[0]), fileline[1], ' '.join(fileline[2::])

def is_id(id):
    if id[0] == '@' and id[-1] == '@':
        return True
    return False

def write_xml_line(xmlf, level, tag_or_id, data, single=True):
    if is_id(tag_or_id):
        xmlf.write('%s<indi id=\"%s\">\n' %('\t' * (level + 1),
                                          tag_or_id))
    elif single:
        xmlf.write('%s<%s>%s</%s>\n' %('\t' * (level + 1),
                                       tag_or_id, data, tag_or_id))
    else:
        xmlf.write('%s<%s>\n%s%s\n' %('\t' * (level + 1), tag_or_id,
                                      '\t' * (level + 2), data))
def gedcom_parser(ged_file, xml_file):
    gedf = open(ged_file)
    xmlf = open(xml_file, 'w+')
    xmlf.write('<gedcom>\n')
    lines = gedf.readlines()
    tag_or_id_stack = []
    for i in range(len(lines)):
        level, tag_or_id, data = format_data(lines[i])
        if i:
            prev_level, _, _ = format_data(lines[i - 1])
            if level < prev_level:
                xmlf.write('%s\n' %(tag_or_id_stack.pop()))
        if i < len(lines) - 1:
            next_level, _, _ = format_data(lines[i + 1])
            if level < next_level:
                if is_id(tag_or_id):
                    tag_or_id_stack.append('%s</indi>' %('\t' * (level + 1)))
                else:
                    tag_or_id_stack.append('%s</%s>' %('\t' * (level + 1), tag_or_id))
                single = False
            else:
                single = True
            write_xml_line(xmlf, level, tag_or_id, data, single=single)
    [xmlf.write(leftover+'\n') for leftover in reversed(tag_or_id_stack)]
    xmlf.write('</gedcom>')
    xmlf.close()
    gedf.close()
                    
def main():
    usage = "usage: %prog gedcom-file xml-file"
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) > 1:
        gedcom_file = args[0]
        xml_file = args[1]
        gedcom_parser(gedcom_file, xml_file)
    else:
        print "Please provide a gedcom-file and xml-file"

if __name__ == "__main__":
    main()
