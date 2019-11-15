import redis
import argparse
import time
import xlsxwriter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python lead exporter. Exports your scraped leads to a handy excel file")
    parser.add_argument("--excel-filename", help="Take a wild stab in the dark :-)")
    parser.add_argument("--run-id", help="The run id to export. If not set the latest run-id is used.")
    parser.add_argument("--list-run-ids", help="Returns a list of run-ids.")
    parser.add_argument("--latest-run-id", help="Returns the latest run-id.")
    args = parser.parse_args()

    if not args.excel_filename:
        excel_filename = time.strftime("%Y%m%d-%H%M%S") + '.xlsx'
    else:
        excel_filename = args.excel_filename

    print("Exporting to %s" % excel_filename)
    workbook = xlsxwriter.Workbook('./exports/%s' % excel_filename)
    worksheet = workbook.add_worksheet("Leads")
    #worksheet.write('A1', 'Hello world')
    

    r = redis.StrictRedis(host='localhost', port=6379, db=1,charset="utf-8", decode_responses=True)
    keys = []
    for key in r.scan_iter("lead:*"):
        lead = r.hgetall(key)
        for k in lead.keys():
            if k not in keys:
                keys.append(k)
    
    for k in keys:
        worksheet.write(str(chr(keys.index(k) + 97)).upper() + '1', k)

    row = 2
    for key in r.scan_iter("lead:*"):
        lead = r.hgetall(key)
        for k in lead.keys():
            worksheet.write(str(chr(keys.index(k) + 97)).upper() + str(row), lead[k])
        row = row +1
        
    workbook.close()